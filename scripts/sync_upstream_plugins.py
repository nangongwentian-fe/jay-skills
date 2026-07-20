#!/usr/bin/env python3
"""Check and synchronize vendored Codex plugin skills from upstream Git repositories."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
from datetime import date
from pathlib import Path, PurePosixPath
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGINS_ROOT = REPO_ROOT / "plugins"
UPSTREAM_FILE = "upstream.json"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


class SyncError(RuntimeError):
    """Raised when an upstream source cannot be synchronized safely."""


def run(command: list[str], *, cwd: Path | None = None) -> str:
    result = subprocess.run(
        command,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise SyncError(f"Command failed ({' '.join(command)}): {detail}")
    return result.stdout.strip()


def relative_parts(value: str) -> tuple[str, ...]:
    path = PurePosixPath(value)
    if not value or path.is_absolute() or ".." in path.parts or path == PurePosixPath("."):
        raise SyncError(f"Path must be a non-empty relative POSIX path: {value!r}")
    return path.parts


def path_inside(base: Path, value: str) -> Path:
    candidate = base.joinpath(*relative_parts(value))
    resolved_base = base.resolve()
    resolved_candidate = candidate.resolve(strict=False)
    if resolved_candidate != resolved_base and resolved_base not in resolved_candidate.parents:
        raise SyncError(f"Path escapes its root: {value!r}")
    return candidate


def reject_symlinks(path: Path) -> None:
    if path.is_symlink():
        raise SyncError(f"Symlinks are not allowed in synchronized paths: {path}")
    if path.is_dir():
        for child in path.rglob("*"):
            if child.is_symlink():
                raise SyncError(f"Symlinks are not allowed in synchronized paths: {child}")


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SyncError(f"Cannot read JSON file {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SyncError(f"Expected a JSON object in {path}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def load_configs(selected: set[str] | None = None) -> list[tuple[Path, dict[str, Any]]]:
    configs: list[tuple[Path, dict[str, Any]]] = []
    for config_path in sorted(PLUGINS_ROOT.glob(f"*/{UPSTREAM_FILE}")):
        plugin_root = config_path.parent
        if selected and plugin_root.name not in selected:
            continue
        config = read_json(config_path)
        validate_config(plugin_root, config)
        configs.append((plugin_root, config))

    found = {plugin_root.name for plugin_root, _ in configs}
    missing = (selected or set()) - found
    if missing:
        raise SyncError(f"Unknown or unconfigured plugin(s): {', '.join(sorted(missing))}")
    if not configs:
        raise SyncError("No upstream plugin configurations found")
    return configs


def validate_config(plugin_root: Path, config: dict[str, Any]) -> None:
    if config.get("schemaVersion") != 1:
        raise SyncError(f"{plugin_root.name}: schemaVersion must be 1")
    if not isinstance(config.get("repository"), str) or not config["repository"].startswith(
        "https://github.com/"
    ):
        raise SyncError(f"{plugin_root.name}: repository must be an HTTPS GitHub URL")
    if not isinstance(config.get("ref"), str) or not config["ref"]:
        raise SyncError(f"{plugin_root.name}: ref is required")
    if not isinstance(config.get("commit"), str) or not SHA_RE.fullmatch(config["commit"]):
        raise SyncError(f"{plugin_root.name}: commit must be a full lowercase Git SHA")

    copies = config.get("copies")
    if not isinstance(copies, list) or not copies:
        raise SyncError(f"{plugin_root.name}: copies must be a non-empty array")
    targets: set[str] = set()
    for item in copies:
        if not isinstance(item, dict) or not isinstance(item.get("source"), str) or not isinstance(
            item.get("target"), str
        ):
            raise SyncError(f"{plugin_root.name}: every copy needs source and target strings")
        relative_parts(item["source"])
        relative_parts(item["target"])
        if item["target"] in targets:
            raise SyncError(f"{plugin_root.name}: duplicate copy target {item['target']!r}")
        targets.add(item["target"])

    patches = config.get("patches", [])
    if not isinstance(patches, list) or not all(isinstance(item, str) for item in patches):
        raise SyncError(f"{plugin_root.name}: patches must be an array of paths")
    for patch in patches:
        patch_path = path_inside(plugin_root, patch)
        if not patch_path.is_file():
            raise SyncError(f"{plugin_root.name}: patch does not exist: {patch}")


def remote_sha(config: dict[str, Any]) -> str:
    output = run(
        [
            "git",
            "ls-remote",
            "--exit-code",
            config["repository"],
            f"refs/heads/{config['ref']}",
        ]
    )
    sha = output.split(maxsplit=1)[0] if output else ""
    if not SHA_RE.fullmatch(sha):
        raise SyncError(f"Unexpected ls-remote output for {config['repository']}: {output!r}")
    return sha


def clone_upstream(config: dict[str, Any], destination: Path) -> str:
    run(
        [
            "git",
            "clone",
            "--quiet",
            "--depth",
            "1",
            "--single-branch",
            "--branch",
            config["ref"],
            config["repository"],
            str(destination),
        ]
    )
    sha = run(["git", "rev-parse", "HEAD"], cwd=destination)
    if not SHA_RE.fullmatch(sha):
        raise SyncError(f"Unexpected cloned Git SHA: {sha!r}")
    return sha


def copy_path(source: Path, destination: Path) -> None:
    reject_symlinks(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        shutil.copytree(source, destination)
    elif source.is_file():
        shutil.copy2(source, destination)
    else:
        raise SyncError(f"Upstream copy source does not exist: {source}")


def remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def prepare_snapshot(
    checkout_root: Path,
    staging_root: Path,
    plugin_root: Path,
    config: dict[str, Any],
) -> None:
    for item in config["copies"]:
        source = path_inside(checkout_root, item["source"])
        target = path_inside(staging_root, item["target"])
        copy_path(source, target)

    patches = config.get("patches", [])
    if patches:
        run(["git", "init", "--quiet"], cwd=staging_root)
        for patch in patches:
            patch_path = path_inside(plugin_root, patch).resolve()
            run(["git", "apply", "--check", str(patch_path)], cwd=staging_root)
            run(["git", "apply", str(patch_path)], cwd=staging_root)
        shutil.rmtree(staging_root / ".git")


def install_snapshot(staging_root: Path, plugin_root: Path, config: dict[str, Any]) -> None:
    for item in config["copies"]:
        source = path_inside(staging_root, item["target"])
        destination = path_inside(plugin_root, item["target"])
        remove_path(destination)
        copy_path(source, destination)


def update_manifest_version(plugin_root: Path, sha: str) -> None:
    manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    manifest = read_json(manifest_path)
    version = manifest.get("version")
    if not isinstance(version, str) or not version:
        raise SyncError(f"{plugin_root.name}: plugin version is missing")
    base_version = version.split("+", 1)[0]
    manifest["version"] = f"{base_version}+codex.upstream-{sha[:12]}"
    write_json(manifest_path, manifest)


def update_upstream_doc(plugin_root: Path, sha: str, synced_on: str) -> None:
    doc_path = plugin_root / "UPSTREAM.md"
    try:
        text = doc_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SyncError(f"{plugin_root.name}: cannot read UPSTREAM.md: {exc}") from exc

    text, sha_count = re.subn(
        r"\| 上游提交 \| `[^`]+` \|",
        f"| 上游提交 | `{sha}` |",
        text,
        count=1,
    )
    text, date_count = re.subn(
        r"\| 同步日期 \| [^|]+ \|",
        f"| 同步日期 | {synced_on} |",
        text,
        count=1,
    )
    if sha_count != 1 or date_count != 1:
        raise SyncError(f"{plugin_root.name}: UPSTREAM.md is missing its SHA or date row")
    doc_path.write_text(text, encoding="utf-8", newline="\n")


def synchronize_plugin(
    plugin_root: Path,
    config: dict[str, Any],
    *,
    force: bool = False,
) -> bool:
    latest = remote_sha(config)
    current = config["commit"]
    if latest == current and not force:
        print(f"UP-TO-DATE {plugin_root.name} {current}")
        return False

    with tempfile.TemporaryDirectory(prefix=f"sync-{plugin_root.name}-") as temp_value:
        temp_root = Path(temp_value)
        checkout_root = temp_root / "upstream"
        staging_root = temp_root / "staging"
        staging_root.mkdir()
        cloned_sha = clone_upstream(config, checkout_root)
        prepare_snapshot(checkout_root, staging_root, plugin_root, config)
        install_snapshot(staging_root, plugin_root, config)

    synced_on = date.today().isoformat()
    config["commit"] = cloned_sha
    config["syncedAt"] = synced_on
    write_json(plugin_root / UPSTREAM_FILE, config)
    update_upstream_doc(plugin_root, cloned_sha, synced_on)
    update_manifest_version(plugin_root, cloned_sha)
    print(f"UPDATED {plugin_root.name} {current} -> {cloned_sha}")
    return True


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("check", "sync"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument(
            "--plugin",
            action="append",
            help="Plugin name to process; repeat to select more than one",
        )
    subparsers.choices["sync"].add_argument(
        "--force",
        action="store_true",
        help="Rebuild even when the recorded SHA is current",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    selected = set(args.plugin) if args.plugin else None
    try:
        configs = load_configs(selected)
        if args.command == "check":
            outdated = 0
            for plugin_root, config in configs:
                latest = remote_sha(config)
                if latest == config["commit"]:
                    print(f"UP-TO-DATE {plugin_root.name} {latest}")
                else:
                    outdated += 1
                    print(f"OUTDATED {plugin_root.name} {config['commit']} -> {latest}")
            print(f"SUMMARY checked={len(configs)} outdated={outdated}")
        else:
            updated = sum(
                synchronize_plugin(plugin_root, config, force=args.force)
                for plugin_root, config in configs
            )
            print(f"SUMMARY checked={len(configs)} updated={updated}")
    except SyncError as exc:
        print(f"ERROR {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

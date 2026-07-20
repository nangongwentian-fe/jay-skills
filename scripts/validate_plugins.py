#!/usr/bin/env python3
"""Validate repo-local Codex marketplace plugins without external dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE_PATH = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
INSTALL_POLICIES = {"NOT_AVAILABLE", "AVAILABLE", "INSTALLED_BY_DEFAULT"}
AUTH_POLICIES = {"ON_INSTALL", "ON_USE"}


class ValidationError(RuntimeError):
    """Raised when repository plugin metadata is invalid."""


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"Cannot read JSON file {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationError(f"Expected a JSON object in {path}")
    return value


def require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{label} must be a non-empty string")
    return value


def parse_skill_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if len(lines) < 4 or lines[0].strip() != "---":
        raise ValidationError(f"{path}: missing YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValidationError(f"{path}: unterminated YAML frontmatter") from exc

    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" not in line or line[:1].isspace():
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"\'')
    for key in ("name", "description"):
        require_string(fields.get(key), f"{path}: frontmatter {key}")
    return fields


def validate_manifest(plugin_root: Path, expected_name: str) -> dict[str, Any]:
    manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    manifest = read_json(manifest_path)
    if manifest.get("name") != expected_name or plugin_root.name != expected_name:
        raise ValidationError(f"{expected_name}: folder, marketplace, and manifest names differ")
    require_string(manifest.get("description"), f"{expected_name}: description")
    version = require_string(manifest.get("version"), f"{expected_name}: version")
    if not SEMVER_RE.fullmatch(version):
        raise ValidationError(f"{expected_name}: invalid semantic version {version!r}")
    author = manifest.get("author")
    if not isinstance(author, dict):
        raise ValidationError(f"{expected_name}: author must be an object")
    require_string(author.get("name"), f"{expected_name}: author.name")
    if manifest.get("skills") != "./skills/":
        raise ValidationError(f"{expected_name}: skills must be './skills/'")

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        raise ValidationError(f"{expected_name}: interface must be an object")
    for key in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
        require_string(interface.get(key), f"{expected_name}: interface.{key}")
    if not isinstance(interface.get("capabilities"), list) or not all(
        isinstance(item, str) for item in interface["capabilities"]
    ):
        raise ValidationError(f"{expected_name}: interface.capabilities must be a string array")
    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3 or not all(
        isinstance(item, str) and 0 < len(item) <= 128 for item in prompts
    ):
        raise ValidationError(f"{expected_name}: interface.defaultPrompt must contain 1-3 prompts")
    return manifest


def validate_upstream(plugin_root: Path, manifest: dict[str, Any]) -> None:
    config_path = plugin_root / "upstream.json"
    config = read_json(config_path)
    sha = require_string(config.get("commit"), f"{plugin_root.name}: upstream commit")
    if not SHA_RE.fullmatch(sha):
        raise ValidationError(f"{plugin_root.name}: upstream commit must be a full Git SHA")
    if config.get("schemaVersion") != 1:
        raise ValidationError(f"{plugin_root.name}: upstream schemaVersion must be 1")
    if not isinstance(config.get("copies"), list) or not config["copies"]:
        raise ValidationError(f"{plugin_root.name}: upstream copies must not be empty")
    if not isinstance(config.get("patches", []), list):
        raise ValidationError(f"{plugin_root.name}: upstream patches must be an array")
    for patch in config.get("patches", []):
        if not isinstance(patch, str) or not (plugin_root / patch).is_file():
            raise ValidationError(f"{plugin_root.name}: missing upstream patch {patch!r}")

    version = require_string(manifest.get("version"), f"{plugin_root.name}: version")
    expected_suffix = f"+codex.upstream-{sha[:12]}"
    if not version.endswith(expected_suffix):
        raise ValidationError(
            f"{plugin_root.name}: version must end with {expected_suffix!r}, got {version!r}"
        )
    upstream_text = (plugin_root / "UPSTREAM.md").read_text(encoding="utf-8")
    if f"`{sha}`" not in upstream_text:
        raise ValidationError(f"{plugin_root.name}: UPSTREAM.md does not contain configured SHA")


def validate_plugin_files(plugin_root: Path) -> int:
    for path in plugin_root.rglob("*"):
        if path.is_symlink():
            raise ValidationError(f"{plugin_root.name}: symlink is not allowed: {path}")

    skill_files = sorted((plugin_root / "skills").glob("*/SKILL.md"))
    if not skill_files:
        raise ValidationError(f"{plugin_root.name}: no skills/*/SKILL.md files found")
    names: set[str] = set()
    for skill_file in skill_files:
        fields = parse_skill_frontmatter(skill_file)
        if fields["name"] in names:
            raise ValidationError(f"{plugin_root.name}: duplicate skill name {fields['name']!r}")
        names.add(fields["name"])

    for python_file in plugin_root.rglob("*.py"):
        try:
            compile(python_file.read_text(encoding="utf-8"), str(python_file), "exec")
        except SyntaxError as exc:
            raise ValidationError(f"{python_file}: invalid Python syntax: {exc}") from exc
    return len(skill_files)


def validate_repository() -> list[tuple[str, int]]:
    marketplace = read_json(MARKETPLACE_PATH)
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        raise ValidationError("marketplace plugins must be a non-empty array")

    seen: set[str] = set()
    results: list[tuple[str, int]] = []
    for entry in plugins:
        if not isinstance(entry, dict):
            raise ValidationError("marketplace plugin entry must be an object")
        name = require_string(entry.get("name"), "marketplace plugin name")
        if name in seen:
            raise ValidationError(f"duplicate marketplace plugin {name!r}")
        seen.add(name)
        source = entry.get("source")
        if not isinstance(source, dict) or source.get("source") != "local":
            raise ValidationError(f"{name}: marketplace source must be local")
        if source.get("path") != f"./plugins/{name}":
            raise ValidationError(f"{name}: unexpected marketplace source path")
        policy = entry.get("policy")
        if not isinstance(policy, dict):
            raise ValidationError(f"{name}: marketplace policy must be an object")
        if policy.get("installation") not in INSTALL_POLICIES:
            raise ValidationError(f"{name}: invalid installation policy")
        if policy.get("authentication") not in AUTH_POLICIES:
            raise ValidationError(f"{name}: invalid authentication policy")
        require_string(entry.get("category"), f"{name}: marketplace category")

        plugin_root = REPO_ROOT / "plugins" / name
        manifest = validate_manifest(plugin_root, name)
        validate_upstream(plugin_root, manifest)
        results.append((name, validate_plugin_files(plugin_root)))
    return results


def main() -> int:
    try:
        results = validate_repository()
    except (OSError, ValidationError) as exc:
        print(f"ERROR {exc}")
        return 1
    for name, skill_count in results:
        print(f"PASS {name} skills={skill_count}")
    print(f"SUMMARY plugins={len(results)} skills={sum(count for _, count in results)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

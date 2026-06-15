#!/usr/bin/env python3
"""Scan and move predefined WeChat/WPS storage targets to macOS Trash."""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


HOME = Path.home()


@dataclasses.dataclass(frozen=True)
class Item:
    id: str
    app: str
    label: str
    risk: str
    paths: tuple[Path, ...]
    impact: str


def du_kib(path: Path) -> int:
    if not path.exists():
        return 0
    try:
        out = subprocess.check_output(
            ["du", "-sk", str(path)],
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return int(out.split()[0])
    except Exception:
        return 0


def size_text(kib: int) -> str:
    value = float(kib)
    for unit in ("KiB", "MiB", "GiB", "TiB"):
        if value < 1024 or unit == "TiB":
            if unit == "KiB":
                return f"{int(value)} {unit}"
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{kib} KiB"


def static_items() -> list[Item]:
    wechat = HOME / "Library/Containers/com.tencent.xinWeChat/Data"
    wps = HOME / "Library/Containers/com.kingsoft.wpsoffice.mac/Data"
    wps_helper = HOME / "Library/Containers/cn.wps.wpslaunchhelper/Data"
    return [
        Item(
            "wechat-temp",
            "WeChat",
            "temporary downloads",
            "low",
            (wechat / "tmp",),
            "Removes temporary downloads and transient files.",
        ),
        Item(
            "wechat-mini-program-cache",
            "WeChat",
            "mini-program cache",
            "low",
            (wechat / ".wxapplet",),
            "Mini-program data is recreated as needed.",
        ),
        Item(
            "wechat-plugin-cache",
            "WeChat",
            "plugin cache",
            "medium",
            (wechat / "Documents/app_data/xplugin",),
            "Plugins may redownload on first use.",
        ),
        Item(
            "wechat-web-runtime-cache",
            "WeChat",
            "web runtime cache",
            "medium",
            (wechat / "Documents/app_data/radium",),
            "Web runtime data may be rebuilt or redownloaded.",
        ),
        Item(
            "wechat-logs",
            "WeChat",
            "logs",
            "low",
            (wechat / "Documents/app_data/log",),
            "Removes diagnostic logs.",
        ),
        Item(
            "wps-addons",
            "WPS",
            "plugin packages",
            "medium",
            (wps / ".kingsoft/wps/addons",),
            "WPS plugins may redownload on first use.",
        ),
        Item(
            "wps-cloud-filecache",
            "WPS",
            "cloud document local cache",
            "medium",
            (
                wps
                / "Library/Application Support/Kingsoft/WPS Cloud Files/userdata/qing/filecache",
            ),
            "Local cloud-document cache is removed; confirm cloud sync first.",
        ),
        Item(
            "wps-online-fonts",
            "WPS",
            "online font cache",
            "low",
            (wps / ".kingsoft/office6/data/fonts",),
            "Online fonts may redownload when documents need them.",
        ),
        Item(
            "wps-launchhelper-logs",
            "WPS",
            "launch helper logs",
            "low",
            (wps_helper / "Library/Application Support/Kingsoft/office6/log",),
            "Removes WPS launch helper logs.",
        ),
        Item(
            "wps-office-logs",
            "WPS",
            "office logs",
            "low",
            (wps / "Library/Application Support/Kingsoft/office6/log",),
            "Removes WPS diagnostic logs.",
        ),
    ]


def discover_chat_items() -> list[Item]:
    root = (
        HOME
        / "Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files"
    )
    if not root.exists():
        return []

    items: list[Item] = []
    for account in sorted(root.iterdir()):
        if not account.is_dir() or not account.name.startswith("wxid_"):
            continue
        items.append(
            Item(
                f"wechat-chat-account:{account.name}",
                "WeChat",
                f"local chat account {account.name}",
                "high",
                (account,),
                "Removes local chat history, databases, attachments, emojis, videos, and search data for this Mac account.",
            )
        )
        items.append(
            Item(
                f"wechat-chat-media:{account.name}",
                "WeChat",
                f"chat media for {account.name}",
                "medium",
                (
                    account / "msg/attach",
                    account / "msg/video",
                    account / "msg/file",
                    account / "cache",
                    account / "business/emoticon",
                ),
                "Removes local chat files, images, videos, emojis, and previews while leaving databases in place.",
            )
        )
        items.append(
            Item(
                f"wechat-chat-db:{account.name}",
                "WeChat",
                f"chat databases for {account.name}",
                "high",
                (account / "db_storage",),
                "Removes local message databases and search/history state.",
            )
        )
    return items


def discover_items() -> list[Item]:
    return static_items() + discover_chat_items()


def item_record(item: Item) -> dict[str, object]:
    paths = [p for p in item.paths if p.exists()]
    kib = sum(du_kib(p) for p in paths)
    return {
        "id": item.id,
        "app": item.app,
        "label": item.label,
        "risk": item.risk,
        "size_kib": kib,
        "size": size_text(kib),
        "exists": bool(paths),
        "paths": [str(p) for p in paths],
        "impact": item.impact,
    }


def scan(args: argparse.Namespace) -> int:
    rows = [item_record(item) for item in discover_items()]
    if not args.include_missing:
        rows = [row for row in rows if row["exists"]]
    rows.sort(key=lambda row: int(row["size_kib"]), reverse=True)

    if args.format == "json":
        print(json.dumps(rows, indent=2, ensure_ascii=False))
        return 0

    print("| id | app | risk | size | label | impact |")
    print("| --- | --- | --- | ---: | --- | --- |")
    for row in rows:
        print(
            f"| `{row['id']}` | {row['app']} | {row['risk']} | {row['size']} | "
            f"{row['label']} | {row['impact']} |"
        )
    if rows:
        total = sum(int(row["size_kib"]) for row in rows)
        print(f"\nTotal existing target size: {size_text(total)}")
    else:
        print("\nNo existing cleanup targets found.")
    return 0


def stop_apps() -> None:
    for app in ("WeChat", "WPS Office", "wpsoffice"):
        subprocess.run(
            ["osascript", "-e", f'tell application "{app}" to quit'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    subprocess.run(
        ["launchctl", "bootout", f"gui/{os.getuid()}/cn.wps.wpslaunchhelper"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    subprocess.run(
        ["pkill", "-f", "WPSFinderMenu|wpslaunchhelper|cn.wps.wpslaunchhelper"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    time.sleep(1)


def selected_paths(ids: list[str]) -> tuple[list[Item], list[Path]]:
    by_id = {item.id: item for item in discover_items()}
    missing_ids = [item_id for item_id in ids if item_id not in by_id]
    if missing_ids:
        raise SystemExit(f"Unknown item id(s): {', '.join(missing_ids)}")

    items = [by_id[item_id] for item_id in ids]
    paths = [p for item in items for p in item.paths if p.exists()]
    resolved = [(p, p.resolve(strict=False)) for p in paths]
    keep: list[Path] = []
    for path, real in resolved:
        parent_selected = False
        for other, other_real in resolved:
            if other == path:
                continue
            try:
                real.relative_to(other_real)
                parent_selected = True
                break
            except ValueError:
                pass
        if not parent_selected and path not in keep:
            keep.append(path)
    return items, keep


def trash_destination(backup: Path, src: Path) -> Path:
    try:
        rel = src.relative_to(HOME)
    except ValueError:
        raise SystemExit(f"Refusing to move path outside HOME: {src}")
    dest = backup / rel
    if not dest.exists():
        return dest
    index = 1
    while True:
        candidate = dest.with_name(f"{dest.name}~{index}")
        if not candidate.exists():
            return candidate
        index += 1


def move_to_trash(args: argparse.Namespace) -> int:
    items, paths = selected_paths(args.ids)
    total_kib = sum(du_kib(path) for path in paths)
    if not paths:
        print("No existing paths for selected item IDs.")
        return 0

    if not args.execute:
        print("Dry run. Add --execute to move these paths to Trash.")
        for path in paths:
            print(f"{size_text(du_kib(path))}\t{path}")
        print(f"Total selected: {size_text(total_kib)}")
        print("Selected IDs:")
        for item in items:
            print(f"- {item.id}: {item.impact}")
        return 0

    if args.stop_apps:
        stop_apps()

    stamp = time.strftime("%Y%m%d-%H%M%S")
    backup = Path(args.backup_dir).expanduser() if args.backup_dir else HOME / ".Trash" / f"app-cleanup-{stamp}"
    backup.mkdir(parents=True, exist_ok=True)

    moved: list[tuple[Path, Path, int]] = []
    for src in paths:
        kib = du_kib(src)
        dest = trash_destination(backup, src)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dest))
        moved.append((src, dest, kib))

    for src, dest, kib in moved:
        print(f"moved\t{size_text(kib)}\t{src}\t{dest}")
    print(f"backup\t{backup}")
    print(f"total\t{size_text(total_kib)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    scan_parser = sub.add_parser("scan", help="List known cleanup targets.")
    scan_parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    scan_parser.add_argument("--include-missing", action="store_true")
    scan_parser.set_defaults(func=scan)

    move_parser = sub.add_parser("move-to-trash", help="Move selected targets to Trash.")
    move_parser.add_argument("--ids", nargs="+", required=True)
    move_parser.add_argument("--execute", action="store_true")
    move_parser.add_argument("--stop-apps", action="store_true")
    move_parser.add_argument("--backup-dir")
    move_parser.set_defaults(func=move_to_trash)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

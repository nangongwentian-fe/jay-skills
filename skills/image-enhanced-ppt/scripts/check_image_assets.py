#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

try:
    from PIL import Image, ImageStat
except ImportError as exc:
    raise SystemExit("Pillow is required: python3 -m pip install pillow") from exc


NAMED_RATIOS = {
    "16:9": 16 / 9,
    "4:3": 4 / 3,
    "1:1": 1,
}

COMPONENT_KINDS = {"flow-line", "flow-node", "marker", "icon-asset"}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Validate image assets referenced by a PPT asset manifest."
    )
    parser.add_argument("--manifest", "--input", dest="manifest", required=True)
    parser.add_argument("--report", required=False)
    parser.add_argument("--base-dir", required=False)
    parser.add_argument("--ratio-tolerance", type=float, default=0.04)
    parser.add_argument("--min-width", type=int, default=1000)
    parser.add_argument("--min-height", type=int, default=560)
    return parser.parse_args()


def is_nonblank(image):
    stat = ImageStat.Stat(image.convert("RGB"))
    return sum(stat.var) > 5


def resolve_assets(spec):
    if isinstance(spec, list):
        return spec
    if isinstance(spec, dict):
        return spec.get("assets", [])
    return []


def parse_ratio(value):
    if value in NAMED_RATIOS:
        return NAMED_RATIOS[value]
    if not isinstance(value, str) or ":" not in value:
        return None
    left, right = value.split(":", 1)
    try:
        width = float(left)
        height = float(right)
    except ValueError:
        return None
    if width <= 0 or height <= 0:
        return None
    return width / height


def main():
    args = parse_args()
    manifest_path = Path(args.manifest).expanduser().resolve()
    base_dir = Path(args.base_dir).expanduser().resolve() if args.base_dir else manifest_path.parent
    spec = json.loads(manifest_path.read_text(encoding="utf-8"))
    assets = resolve_assets(spec)

    records = []
    issues = []
    warnings = []

    if not assets:
        issues.append("no assets found; expected a JSON array or an object with an assets array")

    for asset in assets:
        asset_id = asset.get("id", "<missing-id>")
        asset_path_value = asset.get("path")
        record = {
            "id": asset_id,
            "kind": asset.get("kind"),
            "declaredAspectRatio": asset.get("aspectRatio"),
        }

        if not asset_path_value:
            record["exists"] = False
            issues.append(f"{asset_id} has no path")
            records.append(record)
            continue

        asset_path = (base_dir / asset_path_value).resolve()
        record["path"] = str(asset_path)

        if not asset_path.exists():
            record["exists"] = False
            issues.append(f"{asset_id} file does not exist: {asset_path}")
            records.append(record)
            continue

        try:
            image = Image.open(asset_path)
            image.load()
        except Exception as exc:
            record["exists"] = True
            record["readable"] = False
            issues.append(f"{asset_id} cannot be opened as an image: {exc}")
            records.append(record)
            continue

        width, height = image.size
        actual_ratio = width / height
        brightness = sum(ImageStat.Stat(image.convert("RGB")).mean) / 3
        min_width = int(asset.get("minWidth", args.min_width))
        min_height = int(asset.get("minHeight", args.min_height))
        nonblank = is_nonblank(image)

        record.update(
            {
                "exists": True,
                "readable": True,
                "width": width,
                "height": height,
                "actualAspectRatio": round(actual_ratio, 4),
                "brightness": round(brightness, 1),
                "nonblank": nonblank,
                "minWidth": min_width,
                "minHeight": min_height,
            }
        )

        expected_ratio = parse_ratio(asset.get("aspectRatio"))
        if not expected_ratio:
            issues.append(f"{asset_id} has unsupported aspectRatio: {asset.get('aspectRatio')}")
        elif abs(actual_ratio - expected_ratio) > args.ratio_tolerance:
            issues.append(
                f"{asset_id} aspect ratio mismatch: actual {actual_ratio:.3f}, expected {expected_ratio:.3f}"
            )

        if width < min_width or height < min_height:
            issues.append(
                f"{asset_id} resolution too small: {width}x{height}, expected at least {min_width}x{min_height}"
            )
        if not nonblank:
            issues.append(f"{asset_id} appears blank")
        if brightness < 18 or brightness > 238:
            issues.append(f"{asset_id} brightness is risky: {brightness:.1f}")
        if asset.get("kind") in COMPONENT_KINDS:
            if not asset.get("componentFamily"):
                warnings.append(f"{asset_id} component asset has no componentFamily")
            if not asset.get("reuseScope"):
                warnings.append(f"{asset_id} component asset has no reuseScope")
            if asset.get("semanticContent") not in (None, "none"):
                warnings.append(f"{asset_id} component asset may carry semantic content")
            if not asset.get("nativePptOwns"):
                warnings.append(f"{asset_id} component asset should declare nativePptOwns")

        records.append(record)

    report = {
        "pass": len(issues) == 0,
        "manifest": str(manifest_path),
        "baseDir": str(base_dir),
        "assetCount": len(records),
        "assets": records,
        "issues": issues,
        "warnings": warnings,
        "manualChecks": [
            "no readable fake text",
            "no logos or watermarks unless explicitly licensed",
            "safe zone is clean enough for native PPT text",
            "crop works in the intended slide placement",
        ],
    }

    output = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        report_path = Path(args.report).expanduser().resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(output + "\n", encoding="utf-8")
    print(output)

    if issues:
        raise SystemExit(2)


if __name__ == "__main__":
    main()

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sync = load_module("sync_upstream_plugins", REPO_ROOT / "scripts" / "sync_upstream_plugins.py")
validate = load_module("validate_plugins", REPO_ROOT / "scripts" / "validate_plugins.py")


class PathSafetyTests(unittest.TestCase):
    def test_rejects_parent_traversal(self):
        with self.assertRaises(sync.SyncError):
            sync.relative_parts("../outside")

    def test_rejects_absolute_path(self):
        with self.assertRaises(sync.SyncError):
            sync.relative_parts("/outside")

    def test_accepts_nested_relative_path(self):
        self.assertEqual(sync.relative_parts("skills/demo"), ("skills", "demo"))


class SnapshotTests(unittest.TestCase):
    def test_prepares_snapshot_and_applies_patch(self):
        with tempfile.TemporaryDirectory() as temp_value:
            root = Path(temp_value)
            checkout = root / "checkout"
            staging = root / "staging"
            plugin = root / "plugin"
            (checkout / "skills" / "demo").mkdir(parents=True)
            (checkout / "skills" / "demo" / "value.txt").write_text(
                "before\n", encoding="utf-8"
            )
            (plugin / "patches").mkdir(parents=True)
            patch = plugin / "patches" / "change.patch"
            patch.write_text(
                """diff --git a/skills/demo/value.txt b/skills/demo/value.txt
--- a/skills/demo/value.txt
+++ b/skills/demo/value.txt
@@ -1 +1 @@
-before
+after
""",
                encoding="utf-8",
            )
            staging.mkdir()
            config = {
                "copies": [{"source": "skills/demo", "target": "skills/demo"}],
                "patches": ["patches/change.patch"],
            }

            sync.prepare_snapshot(checkout, staging, plugin, config)

            self.assertEqual(
                (staging / "skills" / "demo" / "value.txt").read_text(encoding="utf-8"),
                "after\n",
            )
            self.assertFalse((staging / ".git").exists())


class ValidationTests(unittest.TestCase):
    def test_parses_quoted_skill_frontmatter(self):
        with tempfile.TemporaryDirectory() as temp_value:
            path = Path(temp_value) / "SKILL.md"
            path.write_text(
                '---\nname: "demo"\ndescription: "Demo skill"\n---\n\n# Demo\n',
                encoding="utf-8",
            )
            self.assertEqual(validate.parse_skill_frontmatter(path)["name"], "demo")

    def test_rejects_unsupported_skill_frontmatter(self):
        with tempfile.TemporaryDirectory() as temp_value:
            path = Path(temp_value) / "SKILL.md"
            path.write_text(
                "---\nname: demo\ndescription: Demo skill\ndisable-model-invocation: true\n---\n",
                encoding="utf-8",
            )
            with self.assertRaises(validate.ValidationError):
                validate.parse_skill_frontmatter(path)

    def test_repository_is_valid(self):
        results = validate.validate_repository()
        self.assertEqual([name for name, _ in results], [
            "taste-skill",
            "code-honor-skill",
            "andrej-karpathy-skills",
            "emilkowalski-skills",
        ])
        self.assertEqual(sum(count for _, count in results), 21)


if __name__ == "__main__":
    unittest.main()

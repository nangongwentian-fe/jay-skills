#!/usr/bin/env python3
"""Lightweight lint for goal-loop-builder output artifacts."""

from __future__ import annotations

import re
import sys
from pathlib import Path


GOAL_MARKERS = [
    ("verification", [r"Verification[:：]", r"验证[:：]"]),
    ("constraints", [r"Constraints[:：]", r"约束[:：]"]),
    ("boundaries", [r"Boundaries[:：]", r"边界[:：]"]),
    ("iteration policy", [r"Iteration policy[:：]", r"迭代策略[:：]"]),
    ("stop when", [r"Stop when[:：]", r"完成条件[:：]", r"停止条件[:：]"]),
    ("pause if", [r"Pause if[:：]", r"暂停条件[:：]", r"阻塞条件[:：]"]),
]

LOOP_MARKERS = [
    ("trigger or interval", [r"^/loop\b", r"Interval[:：]", r"Trigger[:：]", r"间隔[:：]", r"触发[:：]", r"bare `/loop`", r"每\s*\d+\s*(分钟|小时|天)"]),
    ("observation signal", [r"Observe[:：]", r"Observation[:：]", r"Inspect[:：]", r"Check\b", r"Poll\b", r"观察[:：]", r"检查[:：]", r"读取[:：]"]),
    ("reporting", [r"Report\b", r"Notify\b", r"Append\b", r"Write\b", r"报告[:：]", r"汇报[:：]", r"记录[:：]", r"通知[:：]"]),
    ("stop or escalation", [r"Stop\b", r"Escalate\b", r"Alert\b", r"Pause\b", r"停止", r"升级", r"告警", r"暂停"]),
]

PLACEHOLDER_PATTERNS = [
    r"\[[^\]]+\]",
    r"<[^>\n]+>",
    r"\bTODO\b",
    r"\bTBD\b",
    r"待补充",
    r"待定",
]

DANGEROUS_VAGUE_PATTERNS = [
    r"make sure it works",
    r"edit anything",
    r"change whatever",
    r"keep trying",
    r"until it (looks|seems|feels) good",
    r"随便改",
    r"随意修改",
    r"一直尝试",
    r"直到满意",
    r"看起来不错就行",
    r"感觉可以",
]

EVIDENCE_PATTERNS = [
    r"\b(run|start|open|test|build|lint|typecheck|inspect|capture|screenshot|log|artifact|file|url|api|browser|simulator|pr|ci)\b",
    r"(运行|启动|打开|测试|构建|检查|验证|读取|截图|日志|产物|文件|链接|接口|API|浏览器|模拟器|证据|PR|CI)",
]


def has_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE) for pattern in patterns)


def marker_content(text: str, patterns: list[str]) -> str | None:
    for pattern in patterns:
        match = re.search(rf"^\s*{pattern}\s*(.+)$", text, flags=re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1).strip()
    return None


def looks_like_loop(text: str, source: Path) -> bool:
    if re.search(r"^\s*/loop\b", text, flags=re.MULTILINE):
        return True
    if source.name == "loop.md":
        return True
    return "bare `/loop`" in text or ".claude/loop.md" in text


def lint_goal(text: str, source: str) -> list[str]:
    errors: list[str] = []
    goal_line = next((line.strip() for line in text.splitlines() if line.strip().startswith("/goal")), "")
    if not goal_line:
        errors.append(f"{source}: missing `/goal` command")
    elif len(goal_line.removeprefix("/goal").strip()) < 20:
        errors.append(f"{source}: /goal outcome is too short to be actionable")

    for name, patterns in GOAL_MARKERS:
        if not has_any(text, patterns):
            errors.append(f"{source}: missing goal marker `{name}`")

    verification = marker_content(text, GOAL_MARKERS[0][1])
    if verification and not has_any(verification, EVIDENCE_PATTERNS):
        errors.append(f"{source}: verification should name concrete evidence")

    for name, patterns in GOAL_MARKERS:
        content = marker_content(text, patterns)
        if content and len(content) < 12:
            errors.append(f"{source}: `{name}` content is too thin")
    return errors


def lint_loop(text: str, source: str) -> list[str]:
    errors: list[str] = []
    for name, patterns in LOOP_MARKERS:
        if not has_any(text, patterns):
            errors.append(f"{source}: missing loop marker `{name}`")
    return errors


def lint_text(text: str, source_path: Path) -> list[str]:
    source = str(source_path)
    errors: list[str] = []

    if re.search(r"^\s*/目标\b", text, flags=re.MULTILINE):
        errors.append(f"{source}: use `/goal`, not `/目标`, as the executable command")

    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            errors.append(f"{source}: unresolved placeholder matched `{pattern}`")

    for pattern in DANGEROUS_VAGUE_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            errors.append(f"{source}: dangerous vague instruction matched `{pattern}`")

    is_goal = re.search(r"^\s*/goal\b", text, flags=re.MULTILINE) is not None
    is_loop = looks_like_loop(text, source_path)

    if is_goal:
        errors.extend(lint_goal(text, source))
    if is_loop:
        errors.extend(lint_loop(text, source))
    if not is_goal and not is_loop:
        errors.append(f"{source}: cannot determine artifact type; expected `/goal`, `/loop`, or loop.md")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: lint_goal_loop.py <file> [<file> ...]", file=sys.stderr)
        return 2

    errors: list[str] = []
    for raw_path in argv[1:]:
        path = Path(raw_path)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"{path}: cannot read file: {exc}")
            continue
        errors.extend(lint_text(text, path))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("Goal/loop lint passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

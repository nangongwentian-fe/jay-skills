#!/usr/bin/env python3
"""Lightweight lint for goal-loop-builder output artifacts."""

from __future__ import annotations

import re
import sys
from pathlib import Path


GOAL_COMMAND_MAX_CHARS = 350

GOAL_CONTRACT_MARKERS = [
    ("outcome", [r"^##\s+Outcome\b", r"^##\s+目标\b", r"Outcome[:：]", r"目标[:：]"]),
    ("inspect first", [r"^##\s+Inspect First\b", r"^##\s+先检查\b", r"Inspect First[:：]", r"先检查[:：]"]),
    ("verification", [r"^##\s+Verification\b", r"^##\s+验证\b", r"Verification[:：]", r"验证[:：]"]),
    ("constraints", [r"^##\s+Constraints\b", r"^##\s+约束\b", r"Constraints[:：]", r"约束[:：]"]),
    ("boundaries", [r"^##\s+Boundaries\b", r"^##\s+边界\b", r"Boundaries[:：]", r"边界[:：]"]),
    ("iteration policy", [r"^##\s+Iteration Policy\b", r"^##\s+迭代策略\b", r"Iteration policy[:：]", r"迭代策略[:：]"]),
    ("stop when", [r"^##\s+Stop When\b", r"^##\s+完成条件\b", r"^##\s+停止条件\b", r"Stop when[:：]", r"完成条件[:：]", r"停止条件[:：]"]),
    ("pause if", [r"^##\s+Pause If\b", r"^##\s+暂停条件\b", r"^##\s+阻塞条件\b", r"Pause if[:：]", r"暂停条件[:：]", r"阻塞条件[:：]"]),
    ("progress log", [r"^##\s+Progress Log\b", r"^##\s+进度记录\b", r"Progress Log[:：]", r"进度记录[:：]"]),
]

LOOP_MARKERS = [
    ("trigger or interval", [r"^/loop\b", r"Interval[:：]", r"Trigger[:：]", r"间隔[:：]", r"触发[:：]", r"bare `/loop`", r"每\s*\d+\s*(分钟|小时|天)"]),
    ("observation signal", [r"Observe[:：]", r"Observation[:：]", r"Inspect[:：]", r"Check\b", r"Poll\b", r"观察[:：]", r"检查[:：]", r"读取[:：]"]),
    ("reporting", [r"Report\b", r"Notify\b", r"Append\b", r"Write\b", r"报告[:：]", r"汇报[:：]", r"记录[:：]", r"通知[:：]"]),
    ("stop or escalation", [r"Stop\b", r"Escalate\b", r"Alert\b", r"Pause\b", r"停止", r"升级", r"告警", r"暂停"]),
]

PLACEHOLDER_PATTERNS = [
    r"\[(?:TODO|TBD|待补充|待定|goal|目标|path|file|command|cmd|具体|填写|补充|your|repo|project)[^\]]*\]",
    r"<(?:path|file|repo|url|command|target|goal|project|branch|task-slug)[^>\n]*>",
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

AT_MD_REF = re.compile(r"@(?P<path>(?:~|/|\.{1,2}/)?[^\s`'\"\)]+\.md)", re.IGNORECASE)


def has_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE) for pattern in patterns)


def section_content(text: str, patterns: list[str]) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
        if not match:
            continue
        start = match.end()
        next_heading = re.search(r"^##\s+", text[start:], flags=re.MULTILINE)
        end = start + next_heading.start() if next_heading else len(text)
        content = text[start:end].strip(" :：\n")
        return content
    return None


def goal_command_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip().startswith("/goal")]


def goal_ref_paths(text: str, source_path: Path) -> list[Path]:
    paths: list[Path] = []
    for match in AT_MD_REF.finditer(text):
        raw = match.group("path")
        path = Path(raw).expanduser()
        if not path.is_absolute():
            path = (source_path.parent / path).resolve()
        if path not in paths:
            paths.append(path)
    return paths


def looks_like_loop(text: str, source: Path) -> bool:
    if re.search(r"^\s*/loop\b", text, flags=re.MULTILINE):
        return True
    if source.name == "loop.md":
        return True
    return "bare `/loop`" in text or ".claude/loop.md" in text


def looks_like_goal_contract(text: str, source: Path) -> bool:
    return source.name == "goal.md" or source.name.endswith(".goal.md") or "# Goal Run Contract" in text


def lint_goal_contract(text: str, source: str) -> list[str]:
    errors: list[str] = []
    for name, patterns in GOAL_CONTRACT_MARKERS:
        if not has_any(text, patterns):
            errors.append(f"{source}: missing goal contract marker `{name}`")

    verification = section_content(text, GOAL_CONTRACT_MARKERS[2][1])
    if verification and not has_any(verification, EVIDENCE_PATTERNS):
        errors.append(f"{source}: verification should name concrete evidence")

    for name, patterns in GOAL_CONTRACT_MARKERS:
        content = section_content(text, patterns)
        if content is not None and len(content) < 12:
            errors.append(f"{source}: `{name}` content is too thin")
    return errors


def lint_goal_prompt(text: str, source_path: Path) -> list[str]:
    source = str(source_path)
    errors: list[str] = []
    commands = goal_command_lines(text)
    if not commands:
        return [f"{source}: missing `/goal` command"]

    for command in commands:
        if len(command) > GOAL_COMMAND_MAX_CHARS:
            errors.append(f"{source}: /goal command is too long; reference a Markdown contract instead")
        if not AT_MD_REF.search(command):
            errors.append(f"{source}: /goal command should reference a Markdown file with @path")

    refs = goal_ref_paths("\n".join(commands), source_path)
    if not refs:
        return errors

    for ref in refs:
        if not ref.exists():
            errors.append(f"{source}: referenced Markdown contract does not exist: {ref}")
            continue
        try:
            contract_text = ref.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"{source}: cannot read referenced Markdown contract {ref}: {exc}")
            continue
        errors.extend(lint_goal_contract(contract_text, str(ref)))
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

    is_goal_prompt = re.search(r"^\s*/goal\b", text, flags=re.MULTILINE) is not None
    is_goal_contract = looks_like_goal_contract(text, source_path)
    is_loop = looks_like_loop(text, source_path)

    if is_goal_prompt:
        errors.extend(lint_goal_prompt(text, source_path))
    elif is_goal_contract:
        errors.extend(lint_goal_contract(text, source))

    if is_loop:
        errors.extend(lint_loop(text, source))

    if not is_goal_prompt and not is_goal_contract and not is_loop:
        errors.append(f"{source}: cannot determine artifact type; expected `/goal`, goal.md, `/loop`, or loop.md")

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

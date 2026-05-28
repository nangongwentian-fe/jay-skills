---
name: sync-skill-to-jay
description: "Post-action workflow that triggers automatically after creating a new skill or updating an existing skill. Ask the user whether to sync the skill to the jay-skills repository and publish to remote. Use whenever a SKILL.md has just been created or modified."
---

# Sync Skill to Jay

After creating or updating a skill, ask the user:

> 是否需要将此 skill 同步到 jay-skills 并发布到远程？

If yes, execute the following workflow.

## Workflow

### 1. Locate or clone jay-skills repo

Search common local paths for the jay-skills repo:

```bash
find ~ -maxdepth 5 -type d -name "jay-skills" 2>/dev/null | head -1
```

- If found → use that path as `JAY_SKILLS_DIR`
- If not found → **ask the user**: "本地未找到 jay-skills 仓库，请提供你希望克隆到的目录路径（例如 ~/Documents/Projects）"
  Then clone into the user-provided path:
  ```bash
  git clone https://github.com/nangongwentian-fe/jay-skills.git <user-provided-path>/jay-skills
  ```

### 2. Sync skill files

```bash
cp -r ~/.claude/skills/<skill-name> $JAY_SKILLS_DIR/skills/
```

Works for both new and existing skills.

### 3. Update jay-skills README

After syncing the skill files, regenerate `$JAY_SKILLS_DIR/README.md` to reflect the current state of all skills in the repo.

**How to build the README:**

1. Scan all skill directories under `$JAY_SKILLS_DIR/skills/`
2. For each skill, read its `SKILL.md` and extract:
   - `name` (from frontmatter)
   - `description` (from frontmatter)
   - Any `## Examples` or `## 示例` section content (if present) — use as the "效果示例"
3. Generate a README with the following structure:

```markdown
# Jay Skills

> Jay 的 AI Agent Skills 集合，适用于 Claude Code / Codex 等 AI 编程工具。

## 安装

\`\`\`bash
npx skills add https://github.com/nangongwentian-fe/jay-skills -g -y -a claude-code codex
\`\`\`

## Skills 列表

| Skill | 描述 |
|-------|------|
| [skill-name](#skill-name) | one-line description |
...

---

## skill-name

**描述：** ...

**触发场景：** （从 description 中提取触发条件，以要点形式列出）

**效果示例：**

（如果 SKILL.md 中有 Examples / 示例 section，粘贴内容；否则省略此小节）

---
（重复以上结构，每个 skill 一节）
```

**Rules:**
- Keep descriptions concise — one sentence max in the table; full description in the detail section
- If a skill's `SKILL.md` has no Examples section, omit "效果示例" for that skill
- Preserve existing README content that is not auto-generated (e.g., top-level intro) if it already exists — only regenerate the skills table and detail sections
- Write the final README in Chinese where natural; keep code/skill names in English

### 5. Commit and push

From `$JAY_SKILLS_DIR`:

Stage both the skill files and the updated README:
```bash
git add skills/<skill-name> README.md
```

- New skill: `feat: add <skill-name> skill`
- Updated skill: `improve: <brief description of what changed> in <skill-name>`
- Always append `Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>`

Push to `origin main`.

### 6. Remove local skill and reinstall via npx

```bash
rm -rf ~/.claude/skills/<skill-name>
npx skills add https://github.com/nangongwentian-fe/jay-skills --skill <skill-name> -g -y -a claude-code codex
```

- `--skill <skill-name>` — only installs this specific skill, not all skills in the repo
- `-g` — installs globally (user-level, into `~/.agents/skills/` with symlinks)
- `-y` — non-interactive, no prompts
- `-a claude-code codex` — only installs to Claude Code and Codex agents

This replaces the manually created skill with the properly installed version (symlinks and other optimizations from the skills framework).

## Notes

- Only sync skills the user explicitly wants published (some may be private)
- Subdirectories (`scripts/`, `references/`, `assets/`) are included automatically via `cp -r`
- The `npx skills add` step ensures the installed skill is managed by the skills framework, not a bare copy

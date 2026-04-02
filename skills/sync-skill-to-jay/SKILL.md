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

### 3. Commit and push

From `$JAY_SKILLS_DIR`:

- New skill: `feat: add <skill-name> skill`
- Updated skill: `improve: <brief description of what changed> in <skill-name>`
- Always append `Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>`

Push to `origin main`.

### 4. Remove local skill and reinstall via npx

```bash
rm -rf ~/.claude/skills/<skill-name>
npx skills add https://github.com/nangongwentian-fe/jay-skills
```

This replaces the manually created skill with the properly installed version (symlinks and other optimizations from the skills framework).

## Notes

- Only sync skills the user explicitly wants published (some may be private)
- Subdirectories (`scripts/`, `references/`, `assets/`) are included automatically via `cp -r`
- The `npx skills add` step ensures the installed skill is managed by the skills framework, not a bare copy

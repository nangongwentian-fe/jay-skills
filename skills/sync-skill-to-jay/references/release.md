# Publish and install selected skills

Use after the requested source changes, validation and release authorization are concrete.

## Branch and commit

Inspect current branch/upstream, recent commits, remotes and the remote default branch. The release branch must match the default branch consumed by installation (`main` for jay-skills). If it does not, obtain explicit switch or merge direction before committing; do not silently publish a different branch and install stale code.

Stage only the reviewed selected skills and their directly affected docs, evals or required package metadata. Inspect the complete index so previously staged user changes are not swept into the commit. Preserve unrelated dirty work.

Use coherent Conventional Commits with Chinese subjects and outcome-focused body bullets unless the user requests another language. Do not add model-specific coauthor trailers, amend, rebase or rewrite history without authorization. Follow the repository's current plugin-release convention when plugin publication is part of the request; a local edit does not itself require a version bump.

## Push and verify

Push through the configured upstream and verify that the configured remote-tracking branch points exactly to the new commit.

Complete release authorization includes one bounded SSH fallback if HTTPS fails solely because credentials are unavailable: verify the existing GitHub SSH identity, push once through the equivalent SSH URL without changing `origin`, then fetch the configured remote to refresh its tracking reference. Stop for a new decision on identity mismatch, new credential setup, remote changes or non-authentication failure. Never expose credentials in output.

## Install the verified release

Only after remote verification:

```text
npx skills add nangongwentian-fe/jay-skills --skill <skill-name> --global --yes
```

Install only selected skills. Do not pass `--agent` or require/create Codex- or Claude-specific links; the canonical target is `~/.agents/skills/<skill-name>`.

Compare the installed `SKILL.md`, complete file set and contents to the published repository version, ignoring only line-ending differences. Installer exit status alone is insufficient. An unrelated adapter warning is non-blocking when the canonical content matches; missing or mismatched content is a failure even after exit 0.

If publication succeeds but installation fails, report the published commit and exact local state. Do not roll back remote history or alter an explicit project source.

## Report

Return changed skills, validation, commit/branch/push result, installation and content verification, and meaningful conflicts or unrelated work remaining. Distinguish a verified remote release from any separately authorized local installation.

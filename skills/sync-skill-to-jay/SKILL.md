---
name: sync-skill-to-jay
description: "Publish selected jay-skills changes and reinstall the published version when requested. Use for the authorized source-to-release workflow."
---

# Sync Skill to Jay

Use `jay-skills/skills/<skill-name>` as the publishable source of truth. Installed copies under `~/.agents/skills` are derived artifacts, not replacements for an existing repository source.

## Scope and authorization

Identify the selected skills, repository, branch and requested actions. Reuse explicit authorization already given for commit, push and installation; do not ask again merely because this skill is activated.

If publication or installation is not yet authorized, first prepare the scoped source changes, validation and reviewable diff that the task permits. Then ask once for the missing actions, naming the repository, skills, publish branch, Git push and global installation. Do not publish private or local-only skills by implication.

A local validation or installation request does not require publication. For an explicitly authorized local install, derive the selected installation from the validated repository source, verify the complete file set and record that it is an unpublished local version. Do not claim it matches a remote release. The release workflow below continues to install from the verified remote default branch.

## Source integrity

- Verify the local checkout remote is `nangongwentian-fe/jay-skills` and each selected path stays inside its `skills/` directory.
- Edit the existing repository source. Import a new external skill only when its target does not exist, retaining known provenance without inventing missing upstream details.
- If an installed copy differs, inspect the meaningful diff and port only intended changes; never recursively overwrite an existing repository target from it.
- Preserve unrelated staged, unstaged and untracked work. Resolve overlapping changes that prevent an honest commit boundary; ordinary unrelated dirty files do not require stopping.

## Validation and release

Validate selected skills with the active Skill Creator's `quick_validate.py`, check changed resources with appropriate parsers or focused tests, and inspect the diff for scope and sensitive data. Update the affected README entries and existing evals when behavior changes. Do not run unrelated suites by default.

For an authorized release, read [release.md](references/release.md). Complete publication and canonical content verification before claiming success; report partial success accurately when installation fails after publication.

No force push, history rewrite, remote change, new credentials, unrelated skill publication or arbitrary cleanup is authorized by this workflow.

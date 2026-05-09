---
name: progressive-disclosure-docs
description: Design, create, split, or revise Markdown/project documentation using progressive disclosure so agents and humans can find the right level of detail without context bloat. Use when writing docs, README files, runbooks, architecture notes, deployment guides, troubleshooting docs, rules, skills, or when deciding whether content belongs in an existing document or should become a new document.
---

# Progressive Disclosure Docs

Use this skill to make documentation easy for both humans and agents to discover, load, and act on. Preserve the target document's language and style unless the user asks to change it.

## Core Rule

Structure documentation like Agent Skills:

| Layer | Purpose | Document Equivalent |
| ---- | ------- | ------------------- |
| Discovery | Decide whether to read | Filename, title, summary, table of contents |
| Activation | Complete the common task | Scope, decision rules, shortest working path |
| Execution | Handle details only when needed | Commands, config blocks, examples, troubleshooting |
| References | Keep depth available without clutter | Links to topic docs, appendices, source docs |

Never expand an existing document just because it is nearby. Put content where a future reader would naturally look for it.

## Workflow

1. Inspect existing docs before editing.
   - Check filenames, headings, and current scope.
   - Identify the intended reader and task for each candidate doc.

2. Classify the new content.
   - Deployment flow
   - Business logic or domain behavior
   - Architecture or infrastructure
   - Troubleshooting evidence
   - Coding or documentation rules
   - Reference material or examples

3. Choose placement.
   - Update an existing doc only when the new content directly supports that doc's primary topic.
   - Create a new topic doc when the content introduces a second theme, a different reader, or a reusable decision model.
   - Keep the original doc as a navigation point when it only needs to mention the new topic.

4. Write from shallow to deep.
   - Start with what the doc is for and when to use it.
   - Put the common path before edge cases.
   - Put long commands, full configs, historical evidence, and rare cases after the main path.
   - Link to deeper docs instead of embedding unrelated detail.

5. Verify structure.
   - The title matches the content.
   - Each section belongs under the title.
   - A future reader can find the doc by filename.
   - Removing a section would not reveal that it belongs in another doc.

## Split Or Keep

| Signal | Action |
| ------ | ------ |
| A section introduces a new topic | Create a new doc and link to it |
| One doc serves different reader intents | Split by task or audience |
| Config or logs dominate a process doc | Move details to a topic doc or appendix |
| The filename no longer predicts the content | Rename or split |
| The user corrects document placement | Record the rule and update the structure |
| The content is a short note directly supporting the doc | Keep it in the existing doc |

## Document Shape

Prefer this shape for topic docs:

```markdown
# Clear Topic Name

One short paragraph: what this doc covers and when to use it.

## Summary

Key decisions or current facts.

## Common Path

The shortest safe workflow.

## Details

Config, commands, examples, or deeper explanation.

## Verification

How to know it worked.

## Related Docs

Links to adjacent topics.
```

For rule docs, use:

```markdown
# Rule Name

## Core Principles
## Classification Rules
## Checklist
## Examples
## References
```

Do not force these templates when the repo already has a stronger local convention.

## Anti-Patterns

Avoid:

- Adding architecture rules to deployment docs.
- Adding one-off troubleshooting transcripts to top-level docs.
- Creating `notes.md`, `misc.md`, `temp.md`, or other vague filenames.
- Hiding key decisions under historical logs.
- Duplicating the same rule across multiple docs.
- Treating a long README as the only place every detail must live.

## File Naming

- Use lowercase English filenames with hyphens for Markdown docs: `artemis-video-gateway.md`.
- Use a Chinese or project-native title when that helps readers.
- Make the filename describe the stable topic, not the date or temporary task.
- If a doc is environment-specific, include that in the filename only when it changes the content meaning.

## Output Expectations

When editing docs:

- State which doc was created or updated.
- Mention if content was moved out of an inappropriate doc.
- Keep unrelated docs untouched.
- Run a lightweight validation such as `git diff --check` when working in a git repo.


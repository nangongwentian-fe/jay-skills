---
name: codex-imagegen
description: "Generate or edit images via Codex CLI when no native tool is available, or recover outputs from an existing CLI image run."
---

# Codex ImageGen Bridge

Use this bridge when the host lacks a native image tool and the user requests raster-image generation or editing. For a new generation/edit request, use a suitable native tool directly when available. Recovery of an existing CLI invocation still uses this skill and its invocation-specific evidence; it does not authorize generating a replacement image. SVG edits, HTML layouts and ordinary diagrams do not need this bridge.

## Common path

1. Check that Codex CLI is available and that its current environment supports image generation. Inspect current help or official guidance when a flag or capability is uncertain; a feature listing is not proof of authentication.
2. Choose a task-owned workspace and exact output paths. Send the user's subject, use case and real constraints without filling in an exhaustive prompt template. For editing, make the referenced image available and have Codex inspect it first.
3. Ask Codex to use its image-generation tool and return the actual generated file path, copying the result to the agreed output only when permitted. Preserve the configured model, authentication, proxy and permission settings.

```text
codex exec --json --skip-git-repo-check --ephemeral -C <task-workspace> -o <task-message-file> -
```

Pass the prompt through stdin or safe argument handling. The message file contains text, not the image. Do not disable safeguards or silently switch to an API-key workflow.

4. Inspect this invocation's result and verify the image exists at the reported or agreed path. Open it to check the requested content and show it to the user. If the path is missing, use evidence tied to this invocation; never select the newest image from a shared directory, which may belong to another task.
5. Keep final assets in the requested project/output location and clean task-owned temporary messages and inputs that are no longer needed.

For transparency, batches or a failed invocation, read [advanced.md](references/advanced.md). Do not infer successful generation from a zero exit code or a textual claim alone.

---
name: "codex-imagegen"
description: "Generate AI images (photos, illustrations, concept art, product shots, game assets, UI mockups, posters, textures, sprites, stickers) by delegating to Codex CLI's built-in image_gen tool. Use this skill whenever the user asks to generate, create, or make any AI-generated bitmap image in Claude Code — including requests like 'generate an image', 'create a photo of', 'make an illustration', 'design a poster', 'draw a picture', 'generate a product shot', 'create concept art', 'make a logo', 'create a thumbnail', 'generate a hero image', or any visual asset request that needs AI image generation rather than code-based SVG/HTML. Also trigger when the user says '生成图片', '画一张图', '做个海报', '生成一张照片', '帮我画', '生成插画'. Do NOT trigger for editing existing SVG/vector files, creating HTML/CSS layouts, or generating diagrams/flowcharts (those are better handled by code or other tools)."
---

# Codex ImageGen Bridge

Generate AI images from Claude Code by delegating to Codex CLI's built-in `image_gen.imagegen` tool (powered by OpenAI gpt-image-2). This avoids the need for a separate `OPENAI_API_KEY` — Codex uses its own authentication.

## How it works

Claude Code has no built-in image generation tool, but Codex CLI does. This skill bridges the gap:

```
Claude Code  →  codex exec (Bash)  →  Codex's image_gen.imagegen  →  image file  →  Claude Code reads it
```

## Prerequisites

Before generating, verify Codex is ready:

```bash
codex --version 2>/dev/null
```

If Codex is not installed, tell the user to install it:
```bash
npm install -g @openai/codex
```

Then check authentication:
```bash
codex features list 2>/dev/null | grep image_generation
```

If not authenticated, the user needs to run `codex login` interactively.

## Core command pattern

```bash
codex exec \
  --json \
  --skip-git-repo-check \
  --ephemeral \
  -o /tmp/codex-imagegen-lastmsg.txt \
  "<prompt instructions>"
```

Flags explained:
- `--json` — output JSONL event stream (structured, parseable)
- `--skip-git-repo-check` — allow running outside a git repo
- `--ephemeral` — don't persist the session (stateless, clean)
- `-o <file>` — write Codex's final text message to a file

## Image generation workflow

### Step 1: Compose the prompt for Codex

The prompt sent to `codex exec` should explicitly instruct Codex to use its `image_gen.imagegen` tool. Codex is smart but may default to writing code if the prompt is ambiguous.

Template:

```
Use the image_gen.imagegen tool to generate <description of image>.
After generation, copy the result image to <output_path>.
```

Key rules for the prompt:
- Always mention `image_gen.imagegen` by name — this prevents Codex from writing Python to create the image manually
- Always specify a concrete output path for Codex to copy the image to (e.g., `/tmp/codex-output.png`)
- Include style, composition, lighting, and constraint details directly in the prompt
- For text in images, spell out the exact text and ask for verbatim rendering

### Step 2: Run the command

```bash
codex exec --json --skip-git-repo-check --ephemeral \
  -o /tmp/codex-imagegen-lastmsg.txt \
  "Use the image_gen.imagegen tool to generate a photorealistic image of <description>. After generation, copy the result to /tmp/my-image.png"
```

Timeout: image generation typically takes 15–60 seconds. Set Bash timeout to 180000ms (3 minutes) to be safe.

### Step 3: Verify and retrieve

After `codex exec` completes:

1. Check if the output file exists:
   ```bash
   ls -lh /tmp/my-image.png
   ```

2. If the file doesn't exist at the specified path, check Codex's default output directory:
   ```bash
   ls -lt ~/.codex/generated_images/ | head -5
   ```
   Then find and copy the most recent image:
   ```bash
   find ~/.codex/generated_images/ -name "ig_*.png" -mmin -5 -type f | sort | tail -1
   ```

3. Read the image to show the user:
   ```
   Read: /tmp/my-image.png
   ```

## Proxy handling

If the user's environment uses a proxy (common in China), prepend proxy environment variables:

```bash
HTTP_PROXY=http://127.0.0.1:7897 \
HTTPS_PROXY=http://127.0.0.1:7897 \
ALL_PROXY=http://127.0.0.1:7897 \
codex exec --json --skip-git-repo-check --ephemeral \
  "..."
```

Check for proxy by looking at shell environment:
```bash
echo $HTTP_PROXY $HTTPS_PROXY $ALL_PROXY
```

If any proxy variable is set, inherit it. If the user has a proxy wrapper function for codex (check `which codex` or `type codex`), the proxy may already be handled.

## Prompt engineering

Structure the image prompt for best results:

```
Use the image_gen.imagegen tool to generate an image with these specifications:

Use case: <product-mockup | photorealistic-natural | illustration-story | ui-mockup | ads-marketing | logo-brand | stylized-concept | etc.>
Primary request: <what the user wants>
Style/medium: <photography | illustration | 3D render | watercolor | etc.>
Composition/framing: <wide shot | close-up | top-down | centered | etc.>
Lighting/mood: <natural light | studio | dramatic | warm golden hour | etc.>
Color palette: <any color preferences>
Constraints: <no text | no watermark | specific aspect ratio | etc.>
Avoid: <things to exclude>

After generation, copy the result to <output_path>.
```

Only include fields that are relevant. A simple request like "generate a cat photo" doesn't need all fields — just add enough detail to get a good result.

### Prompt tips
- Be specific about the subject and setting
- Include intended use (landing page hero, app icon, social media post) to set the right polish level
- For photorealism, use camera language: "85mm lens", "shallow depth of field", "soft studio lighting"
- For text in images, quote the exact string and spell out tricky words letter-by-letter
- Always include "no watermark" unless one is desired

## Transparent background images

For images that need transparency (logos, stickers, sprites, cutouts):

1. First try the chroma-key approach — ask Codex to generate on a solid color background:
   ```
   Use image_gen.imagegen to generate <subject> on a perfectly flat solid #00ff00
   chroma-key background. The background must be one uniform color with no shadows,
   gradients, texture, or lighting variation. Keep the subject fully separated
   from the background with crisp edges. After generation, copy to /tmp/subject-green.png
   ```

2. Then remove the background locally using Codex's bundled helper:
   ```bash
   python "${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/scripts/remove_chroma_key.py" \
     --input /tmp/subject-green.png \
     --out /tmp/subject-transparent.png \
     --auto-key border \
     --soft-matte \
     --despill
   ```
   This requires Pillow. On macOS with system Python (PEP 668), use a temp venv:
   ```bash
   python3 -m venv /tmp/pillow-env && /tmp/pillow-env/bin/pip install pillow
   /tmp/pillow-env/bin/python "${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/scripts/remove_chroma_key.py" \
     --input /tmp/subject-green.png --out /tmp/subject-transparent.png \
     --auto-key border --soft-matte --despill
   ```

3. If chroma-key removal produces poor results (hair, fur, glass, smoke), inform the user that true native transparency requires Codex's CLI fallback with `gpt-image-1.5`, which needs `OPENAI_API_KEY` set separately.

## Image editing

To edit an existing image, first copy it to a path Codex can access, then instruct Codex:

```
Use image_gen.imagegen to edit the image. The image to edit is at /tmp/source-image.png.
Edit instructions: <what to change>.
Keep everything else unchanged.
After editing, copy the result to /tmp/edited-image.png.
```

For Codex to "see" a local image, you may need to instruct it to use `view_image` first:

```
First use view_image to look at /tmp/source-image.png, then use image_gen.imagegen
to edit it: <edit instructions>. Copy the result to /tmp/edited-image.png.
```

## Batch generation

For multiple images or variants, include all requests in a single prompt:

```
Generate the following images using image_gen.imagegen (one call per image):

1. A sunset landscape — save to /tmp/batch/sunset.png
2. A mountain lake — save to /tmp/batch/lake.png  
3. A forest path — save to /tmp/batch/forest.png

Create the /tmp/batch/ directory first.
```

## Parsing JSONL output

The `codex exec --json` output is a JSONL stream. Useful event types:

- `thread.started` — session began
- `item.completed` with `type: "command_execution"` — a shell command ran (look for `cp` commands to find the output path)
- `item.completed` with `type: "agent_message"` — Codex's text response
- `turn.completed` — includes token usage

The `image_gen` tool call itself is invisible in JSONL — it happens server-side. But the image file is written to `~/.codex/generated_images/<session-id>/ig_*.png` and Codex will `cp` it if instructed.

## Error handling

| Symptom | Cause | Fix |
|---------|-------|-----|
| `codex: command not found` | Codex not installed | `npm install -g @openai/codex` |
| Empty agent message, no image file | Auth expired or network issue | User runs `codex login` |
| Codex writes Python instead of using image_gen | Prompt didn't mention the tool | Explicitly say "use image_gen.imagegen tool" |
| Image in `~/.codex/generated_images/` but not at target path | Codex didn't cp | Manually find and copy the latest image |
| Timeout | Slow network or large image | Increase Bash timeout to 300000ms |
| Proxy errors | Network blocked | Set HTTP_PROXY/HTTPS_PROXY env vars |

## Output file management

- Default Codex output: `~/.codex/generated_images/<session-id>/ig_<hash>.png`
- Recommended target for temp/preview: `/tmp/codex-imagegen/`
- For project assets: copy into the project directory with a descriptive filename
- Don't leave project-referenced images only in `~/.codex/` — always copy to the project

## Limitations

- Image generation uses Codex's OpenAI quota (tied to the user's Codex/OpenAI account)
- No fine-grained control over image dimensions from Claude Code (Codex defaults to auto/1024x1024)
- The `image_gen` tool call is opaque — you can't see the exact API parameters in JSONL
- Editing requires Codex to "view" the image first, which adds a step
- Each `codex exec` call is ephemeral — no conversation history between calls

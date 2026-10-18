# Image bridge: advanced requests and failures

Read only the section relevant to the current request. Verify model and tool capabilities from current official guidance rather than relying on fixed model names or historical limitations.

## Transparency and editing

Prefer the tool's documented native support for transparent backgrounds when available. If the requested output is unsupported, explain the limitation before choosing a workflow that needs new credentials, dependencies or changes the requested treatment of the image. Do not silently substitute another model or a chroma-key pipeline.

For edits, inspect the source, pass the exact reference through the tool's supported mechanism and preserve the requested scope. A text path without an accessible reference is not proof the tool saw the image.

## Multiple outputs

Give each requested image an explicit destination and map returned assets to their request. Run independently only when the host permits it. Report partial success per image and retry only failures; protect completed assets and existing user files.

## Failures

- Missing CLI: report the missing dependency; install only when authorized.
- Authentication or capability error: report the actual error and use the supported recovery path. Do not infer authentication failure merely from a missing output.
- Network/proxy error: inherit the configured environment and inspect only necessary non-secret diagnostics. Do not invent a proxy address or print credential-bearing environment values.
- Timeout: inspect the running invocation and any completed output before retrying to avoid duplicate generations and quota use. Use bounded waits appropriate to the host.
- Missing output path: inspect this invocation's messages and returned paths. Ask for or report the missing evidence if the asset cannot be tied to this request; do not take the newest file in a shared cache.

Distinguish requested dimensions and formats from verified output properties. Do not promise capability, quota, latency or JSONL details that the installed version has not established.

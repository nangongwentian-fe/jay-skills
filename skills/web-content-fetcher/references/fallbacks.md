# Public-page extraction fallbacks

Use only after a direct read fails or clearly omits required body content. These are optional external services, not guaranteed capabilities or mandatory steps. Check their current documentation when their behavior matters.

| Service | Public URL pattern |
| --- | --- |
| Jina Reader | `https://r.jina.ai/<public-https-url>` |
| Defuddle | `https://defuddle.md/<public-https-url>` |

Use a configured extraction service first when available. Otherwise choose one relevant fallback and inspect its result; do not automatically invoke both. Prefer a browser when the page requires interaction that extraction cannot perform.

Sending a URL to either service discloses it to that provider. Never send authenticated, private, internal or credential-bearing URLs. These paths do not authorize bypassing a paywall or access control. If they fail, disclose the missing content and use only clearly attributed public alternatives.

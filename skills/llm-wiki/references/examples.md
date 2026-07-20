# LLM Wiki PowerShell Examples

Use these examples without printing the token.

## Health and authentication

```powershell
$base = 'http://127.0.0.1:19828/api/v1'
$health = Invoke-RestMethod -Uri "$base/health"
$health

$headers = @{
  Authorization = "Bearer $env:LLM_WIKI_API_TOKEN"
}
```

Do not run the protected examples when the environment variable is empty unless the app explicitly allows unauthenticated access.

## Search and read

```powershell
$body = @{ query = 'context engineering'; topK = 5; includeContent = $false } |
  ConvertTo-Json

$hits = Invoke-RestMethod -Method Post -Headers $headers `
  -ContentType 'application/json' -Body $body `
  -Uri "$base/projects/current/search"

$path = [uri]::EscapeDataString('wiki/concepts/context-engineering.md')
$page = Invoke-RestMethod -Headers $headers `
  -Uri "$base/projects/current/files/content?path=$path"
```

## Reviews

```powershell
$reviews = Invoke-RestMethod -Headers $headers `
  -Uri "$base/projects/current/reviews?status=unresolved&limit=20"
```

## Agent chat and cancellation

```powershell
$chatBody = @{
  message = 'Summarize the current evidence and cite Wiki pages.'
  persistSession = $true
  tools = @{ wiki = $true; web = $false; anytxt = $false }
} | ConvertTo-Json -Depth 5

$chat = Invoke-RestMethod -Method Post -Headers $headers `
  -ContentType 'application/json' -Body $chatBody `
  -Uri "$base/projects/current/chat"

$session = [uri]::EscapeDataString($chat.sessionId)
Invoke-RestMethod -Method Post -Headers $headers `
  -Uri "$base/projects/current/chat/$session/cancel"
```

## Fixed-project filesystem fallback

```powershell
$root = if ($env:JAY_LLM_WIKI_ROOT) {
  $env:JAY_LLM_WIKI_ROOT
} else {
  'E:\Code\Personal\jay-llm-wiki'
}

rg -n -i 'context engineering|上下文工程' "$root/wiki"
Get-Content -Raw -Encoding UTF8 "$root/wiki/concepts/context-engineering.md"
```

Use filesystem writes only when the active workflow explicitly authorizes Wiki maintenance.


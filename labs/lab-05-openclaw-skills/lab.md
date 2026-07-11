# Lab 5 — OpenClaw Skills

Extend your agent with pre-built skills. Skills add specialised capabilities — weather, diagrams, browser automation, and more — without writing any code.

**Lab environment:** Hostinger VPS (from Lab 1) **or** Docker Desktop (Windows 10/11, macOS 12+, Ubuntu 22.04+)  
**Prerequisite:** Lab 4 completed — agent responding via Telegram or WhatsApp with Ollama model working.  
**Estimated time:** 20 minutes

> **Docker Desktop users:** Prefix every `openclaw` command with `docker exec -it openclaw`.  
> Example: `docker exec -it openclaw openclaw skills list`

---

## Step 1 — List Available Skills

```bash
# VPS
openclaw skills list

# Docker Desktop
docker exec -it openclaw openclaw skills list
```

Skills have two statuses:
- `✓ ready` — works immediately, no extra setup needed
- `△ needs setup` — requires a CLI tool or API key installed first

Confirm that `weather`, `diagram-maker`, and `browser-automation` all show `✓ ready` before continuing.

---

## Step 2 — Test the Weather Skill

In your Telegram or WhatsApp chat, send:

```
What is the weather in Singapore today?
```

**Pass:** Agent replies with current temperature and conditions.  
**Fail:** "Something went wrong" → model (Ollama) is not running. Run `docker restart openclaw` and retry.

---

## Step 3 — Test the Diagram Maker Skill

In your chat, send:

```
Draw a diagram showing how Docker containers work
```

**Pass:** Agent replies with an SVG or HTML diagram showing Docker concepts.  
**Fail:** Agent replies with text only → send the same message again with "as a diagram" appended.

---

## Step 4 — Test the Browser Automation Skill

In your chat, send:

```
Go to https://news.ycombinator.com and tell me the title of the first story
```

**Pass:** Agent fetches the page and returns the story title.  
**Fail:** Agent says it cannot browse → confirm browser plugin is loaded: `docker exec -it openclaw openclaw plugins inspect browser`

---

## Step 5 — Check Skill Status

```bash
# VPS
openclaw skills check

# Docker Desktop
docker exec -it openclaw openclaw skills check
```

**Pass:** All `✓ ready` skills show no missing requirements.  
**Fail:** A skill shows missing dependency → that skill needs additional CLI setup (not required for this lab).

---

## Step 6 — Install a Skill from ClawHub

Skills not yet installed can be added by name:

```bash
# VPS
openclaw skills install clawhub:healthcheck

# Docker Desktop
docker exec -it openclaw openclaw skills install clawhub:healthcheck
```

Expected output:
```
Installing healthcheck...
✓ Skill installed.
```

Then verify it is ready:

```bash
# VPS
openclaw skills check

# Docker Desktop
docker exec -it openclaw openclaw skills check
```

---

## Step 7 — Test the Healthcheck Skill

In your chat, send:

```
Run a security healthcheck on this OpenClaw instance
```

**Pass:** Agent returns a security audit report with pass/fail items.

---

## Step 8 — Update All Skills

```bash
# VPS
openclaw skills update

# Docker Desktop
docker exec -it openclaw openclaw skills update
```

Updates all installed skills to the latest version.

---

## Ready Skills Reference

Skills marked `✓ ready` require no extra setup:

| Skill | What it does | Test message |
|-------|-------------|--------------|
| `weather` | Current weather and forecasts | `What is the weather in Singapore today?` |
| `diagram-maker` | Generate SVG/HTML diagrams | `Draw a diagram showing how Docker works` |
| `browser-automation` | Multi-step browser control | `Go to https://news.ycombinator.com and get the first story title` |
| `clawhub` | Search and install new skills | `Search ClawHub for skills related to email` |
| `healthcheck` | Audit OpenClaw host security | `Run a security healthcheck` |
| `notion` | Read and write Notion pages | `List my Notion pages` (requires Notion access) |
| `spike` | Run throwaway prototypes | `Prototype a Python script that sorts a list` |

---

## Verification

| Check | Expected |
|-------|----------|
| `openclaw skills list` | `weather`, `diagram-maker`, `browser-automation` show `✓ ready` |
| `openclaw skills check` | No missing requirements for ready skills |
| Chat: `What is the weather in Singapore today?` | Agent returns current weather |
| Chat: `Draw a diagram showing how Docker works` | Agent returns a diagram |
| Chat: `Go to https://news.ycombinator.com and get the first story title` | Agent returns story title |
| `openclaw skills install clawhub:healthcheck` | `✓ Skill installed` |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Skill shows `✓ ready` but agent does not respond | Restart: `docker restart openclaw` then retry |
| Skill install returns 404 | Use exact name from `openclaw skills list` — do not guess |
| `needs setup` skill not working | That skill requires a CLI tool or API key — check `openclaw skills check` for details |
| Weather skill returns no data | Try a different city name or check internet connectivity |
| Diagram not displayed in Telegram | Telegram may not render SVG — ask the agent to "show as an image" instead |

---

## Reference

- ClawHub marketplace: https://clawhub.ai
- Skills docs: https://docs.openclaw.ai/skills

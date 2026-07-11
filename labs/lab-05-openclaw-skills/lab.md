# Lab 5 — OpenClaw Skills

Extend your agent with pre-built skills. Skills add specialised capabilities — weather, diagrams, health checks, and more — without writing any code.

**Lab environment:** Hostinger VPS (from Lab 1) **or** Docker Desktop (Windows 10/11, macOS 12+, Ubuntu 22.04+)  
**Prerequisite:** Lab 4 completed — agent responding via Telegram or WhatsApp.  
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
- `✓ ready` — works immediately, no extra setup
- `△ needs setup` — requires a CLI tool or API key installed first

---

## Step 2 — Test the Weather Skill (Ready, No Setup)

The `weather` skill is bundled and ready. Test it in Telegram or WhatsApp:

```
What is the weather in Singapore today?
```

Expected: Agent fetches and returns the current weather for Singapore.

---

## Step 3 — Test the Diagram Maker Skill (Ready, No Setup)

In your chat, send:

```
Draw a diagram showing how Docker containers and images relate to each other
```

Expected: Agent generates and displays an SVG diagram.

---

## Step 4 — Test the Browser Automation Skill (Ready, No Setup)

In your chat, send:

```
Go to https://news.ycombinator.com and click on the first story link
```

Expected: Agent uses the browser tool with multi-step automation to navigate and return content.

---

## Step 5 — Check Skill Status

```bash
# VPS
openclaw skills check

# Docker Desktop
docker exec -it openclaw openclaw skills check
```

Shows which skills are ready and which require additional setup (CLI tools or API keys).

---

## Step 6 — Install a Skill from ClawHub

Skills listed as `openclaw-extra` or not yet installed can be added from ClawHub:

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

---

## Step 7 — Update All Skills

```bash
# VPS
openclaw skills update

# Docker Desktop
docker exec -it openclaw openclaw skills update
```

Updates all installed skills to the latest version.

---

## Ready Skills Reference

Skills marked `✓ ready` require no extra setup and work immediately in this lab:

| Skill | What it does |
|-------|-------------|
| `weather` | Current weather and forecasts |
| `diagram-maker` | Generate SVG/HTML diagrams |
| `browser-automation` | Multi-step browser control |
| `clawhub` | Search and install new skills |
| `healthcheck` | Audit OpenClaw host security |
| `notion` | Read and write Notion pages |
| `spike` | Run throwaway prototypes |

---

## Verification

| Check | Expected |
|-------|----------|
| `openclaw skills list` | Skills shown with `✓ ready` or `△ needs setup` |
| `openclaw skills check` | Ready skills show no missing requirements |
| Chat: weather question | Agent returns current weather |
| Chat: diagram request | Agent returns a diagram |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Skill install returns 404 | Check exact skill name: `openclaw skills list` and use name from the table |
| Skill shows `✓ ready` but chat does not respond | Send `openclaw skills check` — may need restart: `docker restart openclaw` |
| `needs setup` skill not working | That skill requires a CLI tool or API key — check `openclaw skills check` for details |
| Docker: skill installed but not active | Restart: `docker restart openclaw` |

---

## Reference

- ClawHub marketplace: https://clawhub.ai
- Skills docs: https://docs.openclaw.ai/skills

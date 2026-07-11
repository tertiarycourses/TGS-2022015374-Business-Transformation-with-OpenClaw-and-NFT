# Lab 5 — OpenClaw Skills

Extend your agent with pre-built skills from the ClawHub marketplace. Skills add specialised capabilities without writing any code.

**Lab environment:** Hostinger VPS (from Lab 1) **or** Docker Desktop (Windows 10/11, macOS 12+, Ubuntu 22.04+)  
**Prerequisite:** Lab 4 completed — browser and search tools working.  
**Estimated time:** 20 minutes

> **Docker Desktop users:** Prefix every `openclaw` command with `docker exec -it openclaw`.  
> Example: `docker exec -it openclaw openclaw skills list`

---

## Step 1 — Browse the ClawHub Marketplace

Visit https://clawhub.ai to see all available skills.

Or search from the CLI:

```bash
# VPS
openclaw skills search research

# Docker Desktop
docker exec -it openclaw openclaw skills search research
```

---

## Step 2 — List Available Skills

```bash
# VPS
openclaw skills list

# Docker Desktop
docker exec -it openclaw openclaw skills list
```

Shows all skills — ready, needs setup, and available to install.

---

## Step 3 — Install a Skill from ClawHub

```bash
# VPS
openclaw skills install @openclaw/web-research

# Docker Desktop
docker exec -it openclaw openclaw skills install @openclaw/web-research
```

Expected output:
```
Installing @openclaw/web-research...
✓ Skill installed.
```

---

## Step 4 — Install a Second Skill

```bash
# VPS
openclaw skills install @openclaw/daily-briefing

# Docker Desktop
docker exec -it openclaw openclaw skills install @openclaw/daily-briefing
```

---

## Step 5 — Check Skill Status

```bash
# VPS
openclaw skills check

# Docker Desktop
docker exec -it openclaw openclaw skills check
```

Shows which skills are ready and which need additional setup.

---

## Step 6 — Test a Skill via Chat

In your Telegram or WhatsApp chat, send:

```
/web-research What is OpenClaw?
```

Expected: Agent performs a web search with citations and returns a researched answer.

---

## Step 7 — Update Skills

```bash
# VPS
openclaw skills update

# Docker Desktop
docker exec -it openclaw openclaw skills update
```

Updates all installed ClawHub skills to the latest version.

---

## Verification

| Check | Expected |
|-------|----------|
| `openclaw skills list` | Installed skills shown as `ready` |
| `openclaw skills check` | No missing requirements |
| Chat: `/web-research What is OpenClaw?` | Agent returns researched answer with sources |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Skill not found on ClawHub | Check the exact name: `openclaw skills search <keyword>` |
| Skill installs but command not working in chat | Run `openclaw skills check` — may need additional setup |
| `skills install` fails | Check internet connection — downloads from ClawHub |
| Docker: skill installed but not active | Restart: `docker restart openclaw` |

---

## Reference

- ClawHub marketplace: https://clawhub.ai
- Skills docs: https://docs.openclaw.ai/skills

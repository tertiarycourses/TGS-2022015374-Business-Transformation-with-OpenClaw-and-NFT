# Lab 5 — OpenClaw Skills

Extend your agent with pre-built skills from the ClawHub marketplace. Skills add specialised capabilities — research, coding helpers, schedulers, and more — without writing any code.

**Lab environment:** Hostinger VPS (from Lab 1) **or** Local machine with Docker Desktop

**Prerequisite:** Lab 4 completed — tools (AgentMail, Agent Browser, Firecrawl) active.
**Estimated time:** 20 minutes

---

## Step 1 — Visit the ClawHub Marketplace

Browse available skills at:

**https://clawhub.ai/**

Each skill page shows:
- What the skill does
- Commands it adds to your agent
- Install command

---

## Step 2 — Browse Skills from the CLI

```bash
openclaw skills list --available
```

Expected output (sample):
```
SKILL              DESCRIPTION                        AUTHOR
web-research       Deep web research with citations   ClawHub
code-review        Review code and suggest fixes      ClawHub
daily-briefing     Morning summary delivered at 8am   ClawHub
stock-tracker      Real-time stock price alerts       ClawHub
```

---

## Step 3 — Install a Skill from ClawHub

Use the `npx clawhub@latest install` command with the skill name from the marketplace:

```bash
npx clawhub@latest install web-research
```

Expected output:
```
Installing web-research skill...
✓ Skill installed: web-research
New command available: /web-research
```

**Docker users — run inside the container:**
```bash
docker exec openclaw npx clawhub@latest install web-research
```

---

## Step 4 — Install a Second Skill

```bash
npx clawhub@latest install daily-briefing
```

Expected output:
```
✓ Skill installed: daily-briefing
New command available: /daily-briefing
```

---

## Step 5 — List Installed Skills

```bash
openclaw skills list
```

Expected output:
```
SKILL              STATUS     COMMANDS
web-research       active     /web-research
daily-briefing     active     /daily-briefing
```

---

## Step 6 — Test a Skill via Chat

In your Telegram or WhatsApp chat, send:

```
/web-research What is OpenClaw?
```

Expected: Agent performs a web search with citations and returns a researched answer.

---

## Step 7 — Update a Skill

```bash
npx clawhub@latest update web-research
```

Expected:
```
✓ web-research updated to v1.x.x
```

---

## Step 8 — Remove a Skill

```bash
openclaw skills remove daily-briefing
```

Expected:
```
✓ daily-briefing removed.
```

---

## Verification

| Check | Expected |
|-------|----------|
| `openclaw skills list` | `web-research` shown as `active` |
| Chat: `/web-research What is OpenClaw?` | Agent returns researched answer with sources |
| `openclaw skills list --available` | Marketplace list printed |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `npx: command not found` | Install Node.js: `apt install nodejs npm -y` (VPS) or `docker exec openclaw apt install nodejs npm -y` |
| Skill installs but command not found in chat | Restart gateway: `openclaw gateway restart` |
| ClawHub site not loading | Check your internet connection on the VPS |
| Skill causes agent errors | Remove and reinstall: `openclaw skills remove SKILL && npx clawhub@latest install SKILL` |

---

## Reference

- ClawHub marketplace: https://clawhub.ai
- Skills docs: https://docs.openclaw.ai/skills

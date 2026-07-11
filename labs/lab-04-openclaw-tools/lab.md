# Lab 4 — OpenClaw Tools

Enable and test the three core OpenClaw tools: AgentMail (email agent), Agent Browser (web browsing), and Firecrawl (web scraping).

**Lab environment:** Hostinger VPS (from Lab 1) **or** Local machine with Docker Desktop (Windows 10/11, macOS 12+, Ubuntu 22.04+)

**Prerequisite:** Lab 3 completed — at least one channel (Telegram or WhatsApp) active.
**Estimated time:** 30 minutes

---

## Tool A — AgentMail

AgentMail gives your agent a real email inbox to send and receive emails.

### Step A1 — Create an AgentMail Account

Visit https://agentmail.to and sign up for a free account.

### Step A2 — Get Your API Key

In the AgentMail dashboard → **API Keys** → **Create key**.

Copy your API key.

### Step A3 — Add AgentMail to OpenClaw

```bash
openclaw tools add agentmail \
  --api-key YOUR_AGENTMAIL_API_KEY
```

Expected output:
```
✓ AgentMail tool added.
Inbox: agent@agentmail.to
```

### Step A4 — Test AgentMail via Chat

In your Telegram (or WhatsApp) chat with the agent, send:

```
Check my email
```

Expected: Agent replies listing recent emails in the AgentMail inbox.

---

## Tool B — Agent Browser

Agent Browser lets your agent browse web pages and interact with them.

### Step B1 — Enable Agent Browser

Agent Browser is available at https://agent-browser.dev (powered by Vercel Labs).

```bash
openclaw tools add agent-browser \
  --api-key YOUR_AGENT_BROWSER_API_KEY
```

Expected output:
```
✓ Agent Browser tool added.
```

### Step B2 — Test Agent Browser via Chat

In your chat, send:

```
Browse https://news.ycombinator.com and summarise the top 5 stories
```

Expected: Agent fetches the page and replies with a summary of the top stories.

---

## Tool C — Firecrawl

Firecrawl converts entire websites into clean, structured markdown for the agent to read.

### Step C1 — Create a Firecrawl Account

Visit https://www.firecrawl.dev and sign up for a free account.

### Step C2 — Get Your Firecrawl API Key

In the Firecrawl dashboard → **API Keys** → copy your key (starts with `fc-`).

### Step C3 — Add Firecrawl to OpenClaw

```bash
openclaw tools add firecrawl \
  --api-key YOUR_FIRECRAWL_API_KEY
```

Expected output:
```
✓ Firecrawl tool added.
```

### Step C4 — Test Firecrawl via Chat

In your chat, send:

```
Scrape https://docs.openclaw.ai and give me a summary
```

Expected: Agent returns a clean summary of the OpenClaw documentation page.

---

## List All Active Tools

```bash
openclaw tools list
```

Expected output:
```
TOOL             STATUS    PROVIDER
agentmail        enabled   agentmail.to
agent-browser    enabled   agent-browser.dev
firecrawl        enabled   firecrawl.dev
```

---

## Verification

| Check | Expected |
|-------|----------|
| `openclaw tools list` | All three tools shown as `enabled` |
| Chat: `Check my email` | Email inbox summary in chat |
| Chat: `Browse https://...` | Agent returns page summary |
| Chat: `Scrape https://...` | Agent returns scraped markdown summary |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Invalid API key` for AgentMail | Re-copy the key from the dashboard — check for extra spaces |
| Agent Browser returns "access denied" | Confirm your API key is valid at https://agent-browser.dev |
| Firecrawl returns empty content | The target URL may block crawlers — try a different URL |
| `openclaw tools list` shows tool as `disabled` | Run `openclaw tools enable TOOLNAME` |

---

## Reference

- Tools: https://docs.openclaw.ai/tools
- AgentMail: https://agentmail.to
- Agent Browser: https://agent-browser.dev
- Firecrawl: https://www.firecrawl.dev

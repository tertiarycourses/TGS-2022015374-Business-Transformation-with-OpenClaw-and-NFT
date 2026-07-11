# Lab 4 — OpenClaw Tools

Enable and test the built-in browser tool and install Firecrawl for web scraping.

**Lab environment:** Hostinger VPS (from Lab 1) **or** Docker Desktop (Windows 10/11, macOS 12+, Ubuntu 22.04+)  
**Prerequisite:** Lab 3 completed — at least one channel (Telegram or WhatsApp) active.  
**Estimated time:** 30 minutes

> **Docker Desktop users:** Prefix every `openclaw` command with `docker exec -it openclaw`.  
> Example: `docker exec -it openclaw openclaw plugins list`

---

## Tool A — Agent Browser (Built-in, No Setup)

The browser plugin is already installed and enabled in OpenClaw. No configuration needed.

### Step A1 — Confirm Browser Plugin is Enabled

```bash
# VPS
openclaw plugins inspect browser

# Docker Desktop
docker exec -it openclaw openclaw plugins inspect browser
```

Expected output includes:
```
Status: loaded
id: browser
```

### Step A2 — Test Browser via Chat

In your Telegram or WhatsApp chat with the agent, send:

```
Browse https://news.ycombinator.com and summarise the top 3 stories
```

Expected: Agent fetches the page and replies with a summary.

---

## Tool B — Web Search (DuckDuckGo)

The DuckDuckGo search plugin is bundled but disabled by default. Enable it for free web search.

### Step B1 — Enable DuckDuckGo Search

```bash
# VPS
openclaw plugins enable duckduckgo

# Docker Desktop
docker exec -it openclaw openclaw plugins enable duckduckgo
```

Expected output:
```
Plugin duckduckgo enabled.
```

### Step B2 — Test Web Search via Chat

In your chat, send:

```
Search the web: what is the weather in Singapore today?
```

Expected: Agent searches and returns current results.

---

## Tool C — Firecrawl (Web Scraping)

Firecrawl converts websites into clean structured text for the agent to read.

### Step C1 — Create a Firecrawl Account

Visit https://www.firecrawl.dev and sign up for a free account.

### Step C2 — Get Your Firecrawl API Key

Firecrawl dashboard → **API Keys** → copy your key (starts with `fc-`).

### Step C3 — Install the Firecrawl Plugin

```bash
# VPS
openclaw plugins install clawhub:@openclaw/firecrawl-plugin

# Docker Desktop
docker exec -it openclaw openclaw plugins install clawhub:@openclaw/firecrawl-plugin
```

Expected output:
```
Installing @openclaw/firecrawl-plugin...
✓ Plugin installed.
```

### Step C4 — Configure the Firecrawl API Key

```bash
# VPS
openclaw configure --section plugins

# Docker Desktop
docker exec -it openclaw openclaw configure --section plugins
```

Follow the prompts to enter your Firecrawl API key.

### Step C5 — Test Firecrawl via Chat

In your chat, send:

```
Scrape https://docs.openclaw.ai and give me a summary
```

Expected: Agent returns a clean summary of the page.

---

## List All Plugins

```bash
# VPS
openclaw plugins list

# Docker Desktop
docker exec -it openclaw openclaw plugins list
```

---

## Verification

| Check | Expected |
|-------|----------|
| `openclaw plugins inspect browser` | Status: loaded |
| `openclaw plugins inspect duckduckgo` | Status: loaded |
| `openclaw plugins inspect firecrawl-plugin` | Status: loaded |
| Chat: `Browse https://...` | Agent returns page summary |
| Chat: `Search the web: ...` | Agent returns search results |
| Chat: `Scrape https://...` | Agent returns scraped content |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Browser returns empty result | Check the URL is publicly accessible |
| DuckDuckGo returns no results | Try a different search query |
| Firecrawl install fails | Check internet connection — plugin downloads from ClawHub |
| Firecrawl key rejected | Key must start with `fc-` — re-copy from firecrawl.dev dashboard |
| Plugin enabled but agent not using it | Restart gateway: `docker restart openclaw` |

---

## Reference

- Plugins: https://docs.openclaw.ai/plugins
- Firecrawl: https://www.firecrawl.dev
- ClawHub: https://clawhub.ai

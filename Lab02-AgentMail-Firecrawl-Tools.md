# Lab 2 — AgentMail, Firecrawl & Other Tools

## Objective
Extend OpenClaw with third-party tools so your agent can scrape websites
(Firecrawl), send/receive email (AgentMail), and call other integrations.

## Prerequisites
- Lab 1 completed (OpenClaw running, model connected, at least one channel live)
- Free accounts at:
  - <https://www.firecrawl.dev/>
  - <https://agentmail.to/>
- API keys from each

## Estimated Time
~45 minutes

---

## Step 1 — Inspect Built-in Tools

```bash
openclaw tools list
```

You should see categories like:
- `group:fs` — file read/write/edit
- `group:web` — `web_search`, `web_fetch`, `browser`
- `group:runtime` — `exec`, sandboxed Python
- `group:media` — image/video/TTS

![](screenshots/lab2-01-tools-list.png)

---

## Step 2 — Enable Firecrawl

Firecrawl gives the agent reliable, JS-rendered web scraping.

1. Sign up at <https://www.firecrawl.dev/> → **Dashboard → API Keys** → copy `fc-...`.
2. Register the key:
   ```bash
   export FIRECRAWL_API_KEY="fc-..."
   openclaw tools enable firecrawl --api-key "$FIRECRAWL_API_KEY"
   ```
3. Confirm:
   ```bash
   openclaw tools status firecrawl
   ```

![](screenshots/lab2-02-firecrawl-key.png)

### Smoke test
In Telegram or WhatsApp, send:
> Use Firecrawl to summarize https://docs.openclaw.ai/install in 5 bullets.

---

## Step 3 — Enable AgentMail

AgentMail gives the agent its own inbox/outbox.

1. Sign up at <https://agentmail.to/> → create an inbox → copy the API key
   and the inbox address (e.g. `bot@yourname.agentmail.to`).
2. Register:
   ```bash
   export AGENTMAIL_API_KEY="..."
   openclaw tools enable agentmail \
     --api-key "$AGENTMAIL_API_KEY" \
     --inbox bot@yourname.agentmail.to
   ```
3. Confirm:
   ```bash
   openclaw tools status agentmail
   ```

![](screenshots/lab2-03-agentmail.png)

### Smoke test
> Send an email from my AgentMail inbox to `<your-personal-email>` with subject
> "Hello from OpenClaw" and a friendly one-paragraph body.

Check your personal inbox. Reply to it and ask the agent:
> Check my AgentMail inbox and summarize the latest reply.

---

## Step 4 — Tool Profiles & Allow/Deny Lists

Tool profiles control which tools an agent may invoke per channel/context.

```bash
# Use the preset "messaging" profile for Telegram
openclaw channel set telegram --profile messaging

# Use full tools when chatting from CLI
openclaw channel set cli --profile full
```

Custom allow/deny:
```bash
# Block shell exec on the WhatsApp channel
openclaw channel set whatsapp --deny exec

# Allow only web tools on a public channel
openclaw channel set telegram --allow group:web
```

Verify:
```bash
openclaw channel show telegram
```

---

## Step 5 — Add One More Integration (Choose Your Own)

Pick one from the docs at <https://docs.openclaw.ai/tools> and enable it.
Suggested options:
- `slack` — post to a Slack workspace
- `notion` — read/write Notion pages
- `github` — open issues / PRs
- `google-drive` — list / fetch files

```bash
openclaw tools enable <tool-name> --api-key <KEY>
```

---

## Verification

- `openclaw tools list --enabled` shows **firecrawl** and **agentmail**.
- The agent can scrape a URL on demand via Telegram.
- The agent can send an email via AgentMail.
- A `--deny exec` channel refuses shell-exec requests.

---

## Troubleshooting

| Symptom | Fix |
|--------|-----|
| `tool 'firecrawl' not found` | Update OpenClaw: `npm install -g openclaw@latest`. |
| `401 Unauthorized` from Firecrawl | Re-copy key; check for trailing whitespace. |
| AgentMail send returns 403 | Confirm the inbox is verified in the AgentMail dashboard. |

---

## Exercise

1. Build a "morning brief" prompt that uses **Firecrawl** to fetch the front page
   of <https://news.ycombinator.com/> and **AgentMail** to email you the top 5 stories.
2. Define a custom tool profile `research` that allows only `firecrawl`,
   `web_search`, and `browser` (no `exec`, no `fs.write`). Apply it to the
   Telegram channel.

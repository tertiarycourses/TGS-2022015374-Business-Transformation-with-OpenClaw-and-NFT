# Lab 4 — OpenClaw Commands & Slash Commands

## Objective
Master the everyday **CLI commands** (`openclaw config`, `model`, `doctor`,
`gateway`, `channel`, `tools`, `skills`) and the **in-chat slash commands**
that students will use throughout the course.

## Prerequisites
- Labs 1–3 completed

## Estimated Time
~30 minutes

References:
- <https://docs.openclaw.ai/channels>
- <https://docs.openclaw.ai/tools>
- <https://docs.openclaw.ai/providers>

---

## Part A — CLI Commands

### `openclaw config`
```bash
openclaw config list                    # show all settings
openclaw config get model               # get one setting
openclaw config set model openai/gpt-4o # set one setting
openclaw config edit                    # open the config file in $EDITOR
```

### `openclaw model`
```bash
openclaw model list      # all available models
openclaw model current   # what's selected
openclaw model use deepseek/deepseek-chat
openclaw model test      # send a tiny test prompt
```

### `openclaw doctor`
```bash
openclaw doctor          # health check: Node, daemon, providers, channels
openclaw doctor --fix    # auto-fix common issues
```

![](screenshots/lab4-01-doctor.png)

### `openclaw gateway`
The gateway is the long-running daemon that hosts channels and tools.
```bash
openclaw gateway status
openclaw gateway start
openclaw gateway stop
openclaw gateway restart
openclaw gateway logs --tail 50
openclaw gateway install     # install daemon (LaunchAgent / systemd / Task)
openclaw gateway uninstall
```

### `openclaw channel`
```bash
openclaw channel list
openclaw channel add telegram --token <TOKEN>
openclaw channel start whatsapp
openclaw channel show telegram
openclaw channel set telegram --profile messaging
openclaw channel remove telegram
```

### `openclaw tools`
```bash
openclaw tools list
openclaw tools list --enabled
openclaw tools enable firecrawl --api-key <KEY>
openclaw tools disable exec
openclaw tools status agentmail
```

### `openclaw skills`
```bash
openclaw skills list
openclaw skills add self-improvement --source skills.sh
openclaw skills remove self-improvement
openclaw skills update
```

---

## Part B — In-Chat Slash Commands

These work inside any channel (Telegram, WhatsApp, CLI chat).

| Slash Command | Purpose |
|---|---|
| `/help` | List all available slash commands |
| `/model <name>` | Switch model for this conversation |
| `/skill <name> [args]` | Run an installed skill |
| `/tools` | List tools the agent may use here |
| `/clear` | Clear conversation history |
| `/memory` | View / edit agent memory for this user |
| `/whoami` | Show user, channel, profile, current model |
| `/stop` | Cancel the current generation |

![](screenshots/lab4-02-slash-help.png)

---

## Hands-On

1. From CLI, run `openclaw doctor`. Fix any warnings.
2. From Telegram, send:
   - `/whoami`
   - `/model deepseek/deepseek-chat` then ask a question
   - `/tools`
   - `/clear`
3. Tail the logs in another terminal:
   ```bash
   openclaw gateway logs --follow
   ```
   Send a message in chat and observe the corresponding log lines.

---

## Verification

- You can switch model from chat **and** from CLI.
- You can read live gateway logs while chatting.
- `/help` lists at least the commands above.

---

## Troubleshooting

| Symptom | Fix |
|--------|-----|
| `/skill foo` says "unknown skill" | `openclaw skills list` — install if missing. |
| Gateway logs empty | Ensure gateway is running: `openclaw gateway status`. |
| `/model` change doesn't persist | `/model` is per-conversation; use `openclaw model use ...` for global default. |

---

## Exercise

Make a one-page **cheat sheet** (markdown) of the 10 commands you'd use most
day-to-day. Save it to `~/.openclaw/notes/cheatsheet.md`.

# Lab 7 — Uninstall OpenClaw

## Objective
Cleanly remove OpenClaw from your machine — daemon, CLI, config, channel
sessions — and revoke any external credentials so nothing is left dangling.

## Prerequisites
- An existing OpenClaw install from Labs 1–6

## Estimated Time
~15 minutes

---

## Step 1 — Back Up What You Want to Keep

Before deleting, save anything worth keeping:

```bash
mkdir -p ~/openclaw-backup-$(date +%F)
cp -R ~/.openclaw/notes      ~/openclaw-backup-$(date +%F)/ 2>/dev/null || true
cp -R ~/.openclaw/journal    ~/openclaw-backup-$(date +%F)/ 2>/dev/null || true
cp    ~/.openclaw/config.toml ~/openclaw-backup-$(date +%F)/ 2>/dev/null || true
```

---

## Step 2 — Stop the Gateway and Uninstall the Daemon

```bash
openclaw gateway stop
openclaw gateway uninstall
```

This removes:
- macOS LaunchAgent (`~/Library/LaunchAgents/ai.openclaw.gateway.plist`)
- Linux systemd user unit (`~/.config/systemd/user/openclaw-gateway.service`)
- Windows Scheduled Task `OpenClawGateway`

Verify:
```bash
openclaw gateway status     # should say: not installed
```

---

## Step 3 — Disconnect Channels

```bash
openclaw channel remove telegram
openclaw channel remove whatsapp
```

WhatsApp will also unlink the device from your phone (you can confirm in
**WhatsApp → Linked Devices**).

In Telegram, **delete the bot** from BotFather if you no longer need it:
- Open BotFather → `/mybots` → select bot → **Delete Bot**.

---

## Step 4 — Uninstall the CLI

Pick the method matching how you installed in Lab 1.

### npm install
```bash
npm uninstall -g openclaw
```

### Installer script (macOS / Linux)
```bash
~/.openclaw/uninstall.sh
```

### Installer script (Windows PowerShell, run as Administrator)
```powershell
iwr -useb https://openclaw.ai/uninstall.ps1 | iex
```

### From source
```bash
pnpm unlink --global openclaw
rm -rf ~/code/openclaw   # wherever you cloned it
```

Verify:
```bash
which openclaw           # should print nothing
openclaw --version       # should error: command not found
```

---

## Step 5 — Remove Config & State

> ⚠️ This deletes WhatsApp pairing, cron jobs, audit logs, and everything else.

```bash
# macOS / Linux
rm -rf ~/.openclaw
rm -rf ~/.config/openclaw

# Windows (PowerShell)
Remove-Item -Recurse -Force "$env:USERPROFILE\.openclaw"
Remove-Item -Recurse -Force "$env:APPDATA\openclaw"
```

---

## Step 6 — Revoke External Credentials

Each of the following dashboards has its own key list — visit and revoke
keys you generated for OpenClaw:

| Service | Where to revoke |
|---|---|
| OpenAI | <https://platform.openai.com/api-keys> |
| DeepSeek | <https://platform.deepseek.com/api_keys> |
| MiniMax | <https://www.minimaxi.com/> dashboard |
| Firecrawl | <https://www.firecrawl.dev/> → API Keys |
| AgentMail | <https://agentmail.to/> → Inbox settings |
| Telegram | BotFather → `/revoke` (rotates token) or `Delete Bot` |

Also unset env vars:
```bash
# macOS / Linux — edit ~/.zshrc or ~/.bashrc and remove the export lines
# Windows
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY",$null,"User")
```

![](screenshots/lab7-01-revoke-keys.png)

---

## Verification

- `which openclaw` returns nothing.
- `~/.openclaw/` no longer exists.
- WhatsApp Linked Devices no longer shows OpenClaw.
- All provider dashboards show the revoked keys as **inactive**.
- No OpenClaw entries in `crontab -l` or system service manager.

---

## Troubleshooting

| Symptom | Fix |
|--------|-----|
| `openclaw: command not found` but `which openclaw` finds it | Stale shell hash: `hash -r` (bash) or restart terminal. |
| Daemon keeps restarting | You skipped Step 2; run `openclaw gateway uninstall` before removing the binary. |
| Permission denied removing `~/.openclaw` | `sudo rm -rf ~/.openclaw`. |

---

## Exercise

Re-run **Lab 1** from scratch on a clean machine (or the same one after this
lab) and time how long the full setup takes you. Aim for under 20 minutes —
this confirms you've internalized the workflow.

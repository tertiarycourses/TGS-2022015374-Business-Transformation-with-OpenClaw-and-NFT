# Lab 3 — OpenClaw Channel

Connect OpenClaw to messaging channels so users can chat with your agent. This lab covers Telegram (via BotFather) and WhatsApp (QR pairing).

**Lab environment:** Hostinger VPS (from Lab 1) or Docker Desktop (Windows 10/11, macOS 12+, Ubuntu 22.04+)  
**Prerequisite:** Lab 2 completed — model provider configured and `openclaw models status` showing connected.  
**Estimated time:** 30 minutes

> **Docker Desktop users:** Prefix every `openclaw` command with `docker exec -it openclaw`.  
> Example: `docker exec -it openclaw openclaw channels add`

---

## Part A — Telegram

### Step A1 — Create a Bot via BotFather

1. Open Telegram and search for `@BotFather`
2. Send the command: `/newbot`
3. BotFather asks: **What is the name of your bot?**  
   Enter a display name, e.g. `Alfred Agent`
4. BotFather asks: **What username for your bot?**  
   Enter a unique username ending in `bot`, e.g. `alfred_agent_bot`
5. BotFather replies with your **bot token**:

```
Done! Use this token to access the HTTP API:
7123456789:AAGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Copy this token — you need it in the next step.

---

### Step A2 — Register the Bot Token with OpenClaw

**Option 1 — Interactive wizard (recommended):**

```bash
# VPS
openclaw channels add

# Docker Desktop
docker exec -it openclaw openclaw channels add
```

The wizard will ask you to select a channel — choose **Telegram** and paste your bot token when prompted.

**Option 2 — Non-interactive (one command):**

```bash
# VPS
openclaw channels add --channel telegram --token YOUR_BOT_TOKEN

# Docker Desktop
docker exec -it openclaw openclaw channels add --channel telegram --token YOUR_BOT_TOKEN
```

Expected output:
```
✓ Telegram channel added.
Bot username: @alfred_agent_bot
```

---

### Step A3 — Check Channel Status

```bash
# VPS
openclaw channels status

# Docker Desktop
docker exec -it openclaw openclaw channels status
```

Expected output:
```
CHANNEL     STATUS    ACCOUNT
telegram    running   @alfred_agent_bot
```

---

### Step A4 — Test the Telegram Channel

1. Open Telegram
2. Search for your bot (e.g. `@alfred_agent_bot`)
3. Send: `Hello`

Expected: The agent replies with a greeting.

---

## Part B — WhatsApp

### Step B1 — Add the WhatsApp Channel

```bash
# VPS
openclaw channels add --channel whatsapp

# Docker Desktop
docker exec -it openclaw openclaw channels add --channel whatsapp
```

---

### Step B2 — Link Your WhatsApp Account (QR Pairing)

```bash
# VPS
openclaw channels login --channel whatsapp

# Docker Desktop
docker exec -it openclaw openclaw channels login --channel whatsapp
```

OpenClaw prints a QR code in the terminal.

On your phone:
1. Open WhatsApp
2. Tap **Settings** → **Linked Devices** → **Link a Device**
3. Scan the QR code shown in your terminal

Expected terminal output after scanning:
```
✓ WhatsApp paired successfully.
Phone: +65xxxxxxxx
```

---

### Step B3 — Check Channel Status

```bash
# VPS
openclaw channels status

# Docker Desktop
docker exec -it openclaw openclaw channels status
```

Expected output:
```
CHANNEL     STATUS    ACCOUNT
telegram    running   @alfred_agent_bot
whatsapp    running   +65xxxxxxxx
```

---

### Step B4 — Test the WhatsApp Channel

Send a WhatsApp message to your linked number from another device.

Message: `Hello`

Expected: Agent replies in the same WhatsApp chat.

---

## List All Configured Channels

```bash
# VPS
openclaw channels list

# Docker Desktop
docker exec -it openclaw openclaw channels list
```

---

## Verification

| Check | Expected |
|-------|----------|
| `openclaw channels list` | telegram and whatsapp listed |
| `openclaw channels status` | Both channels showing `running` |
| Telegram message `Hello` | Agent replies in Telegram |
| WhatsApp message `Hello` | Agent replies in WhatsApp |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| BotFather says "username already taken" | Choose a different username — must be unique globally |
| `openclaw channel add` not found | Use `channels` (plural) — `openclaw channels add` |
| Telegram bot does not reply | Run `openclaw channels status` — confirm status is `running` |
| QR code expires before scanning | Re-run `openclaw channels login --channel whatsapp` for a new QR |
| WhatsApp says "Linked device limit reached" | Phone → Settings → Linked Devices → remove an old device |
| Docker: command not found | Add `docker exec -it openclaw` before every `openclaw` command |

---

## Reference

- Channels: https://docs.openclaw.ai/channels
- Telegram BotFather: https://t.me/BotFather

# Lab 3 — OpenClaw Channel

Connect OpenClaw to messaging channels so users can chat with your agent. This lab covers Telegram (via BotFather) and WhatsApp (QR pairing).

**Lab environment:** Hostinger VPS (from Lab 1) or Local machine (Windows 10/11, macOS 12+, Ubuntu 22.04+)

**Prerequisite:** Lab 2 completed — a model provider configured and `openclaw model test` passing.
**Estimated time:** 30 minutes

---

## Part A — Telegram

### Step A1 — Create a Bot via BotFather

1. Open Telegram and search for `@BotFather`
2. Send the command:

```
/newbot
```

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

```bash
openclaw channel add telegram \
  --token YOUR_BOT_TOKEN
```

Expected output:
```
✓ Telegram channel added.
Bot username: @alfred_agent_bot
```

---

### Step A3 — Start the Telegram Channel

```bash
openclaw channel start telegram
```

Expected output:
```
✓ Telegram channel started.
Listening for messages...
```

---

### Step A4 — Test the Telegram Channel

1. Open Telegram
2. Search for your bot (`@alfred_agent_bot`)
3. Send: `Hello`

Expected: The agent replies with a greeting.

---

## Part B — WhatsApp

### Step B1 — Start WhatsApp Pairing

```bash
openclaw channel add whatsapp
```

OpenClaw prints a QR code in the terminal.

---

### Step B2 — Scan the QR Code

On your phone:

1. Open WhatsApp
2. Tap **Settings** → **Linked Devices** → **Link a Device**
3. Scan the QR code displayed in your terminal

Expected terminal output after scanning:
```
✓ WhatsApp paired successfully.
Phone: +65xxxxxxxx
```

---

### Step B3 — Start the WhatsApp Channel

```bash
openclaw channel start whatsapp
```

Expected output:
```
✓ WhatsApp channel started.
Listening for messages...
```

---

### Step B4 — Test the WhatsApp Channel

Send a WhatsApp message to your own linked number (from another device or using the WhatsApp app on your phone).

Message: `Hello`

Expected: Agent replies in the same WhatsApp chat.

---

## Check All Active Channels

```bash
openclaw channel list
```

Expected output:
```
CHANNEL     STATUS    SINCE
telegram    running   0h 5m
whatsapp    running   0h 2m
```

---

## Verification

| Check | Expected |
|-------|----------|
| `openclaw channel list` | Both `telegram` and `whatsapp` shown as `running` |
| Telegram message `Hello` | Agent replies in Telegram |
| WhatsApp message `Hello` | Agent replies in WhatsApp |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| BotFather says "username already taken" | Choose a different username (must be unique globally) |
| Telegram bot does not reply | Run `openclaw channel start telegram` and check `openclaw gateway status` |
| QR code expires before scanning | Run `openclaw channel add whatsapp` again to generate a new QR |
| WhatsApp says "Linked device limit reached" | On phone: Settings → Linked Devices → remove an old device first |

---

## Reference

- Channels: https://docs.openclaw.ai/channels
- Telegram BotFather: https://t.me/BotFather

# Lab 1 — Step-by-Step OpenClaw Setup

## Objective
Install OpenClaw on a local machine **or** a VPS, connect a model provider,
register your first skill, and wire up Telegram + WhatsApp channels so you can
chat with your agent.

## Prerequisites
- Admin / sudo rights on your computer
- Internet access
- Telegram account + a phone running WhatsApp
- One LLM provider API key (OpenAI, DeepSeek, or MiniMax)

## Estimated Time
~60 minutes

---

## Step 1 — Install Node.js (24 LTS recommended; 22.16+ minimum)

OpenClaw runs on Node.js. Install it first, then verify.

### Windows
Download the **Node 24 LTS** Windows Installer from
<https://nodejs.org/> and run the `.msi`. WSL2 is recommended for stability.

```powershell
node -v
npm -v
```

### macOS
```bash
brew install node@24
node -v && npm -v
```

### Linux (Ubuntu / Debian)
```bash
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt-get install -y nodejs
node -v && npm -v
```

![](screenshots/01-node-version.png)

---

## Step 2 — Install OpenClaw

You have **three** install paths. Pick one.

### Option A — npm (recommended, cross-platform)

After installing Node.js (Step 1), run:
```bash
npm install -g openclaw@latest
openclaw onboard
```

### Option B — Installer Script (fallback if the npm method fails)

**macOS / Linux / WSL2:**
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Windows (PowerShell, run as Administrator):**
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

### Option C — From Source (advanced)
```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install && pnpm build && pnpm ui:build
pnpm link --global
openclaw onboard --install-daemon
```

![](screenshots/02-install-success.png)

---

## Step 3 — Install on a VPS

Pick **one** of the following.

### 3A. Hostinger VPS (Ubuntu 22.04 KVM)

1. Buy/launch a KVM VPS from <https://www.hostinger.com?REFERRALCODE=FEGANGCHQ20C> (use this link for a 20% discount).
2. SSH in:
   ```bash
   ssh root@<your-vps-ip>
   ```
3. Install Node 24:
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_24.x | bash -
   apt-get install -y nodejs
   ```
4. Install OpenClaw:
   ```bash
   npm install -g openclaw@latest
   openclaw onboard
   ```
5. Run as a systemd user service so it survives logout:
   ```bash
   openclaw gateway install
   openclaw gateway start
   ```

![](screenshots/03-hostinger-ssh.png)

### 3B. exe.dev sandbox (https://exe.dev/)

1. Sign up at <https://exe.dev/> and create a new dev sandbox.
2. Open the web terminal.
3. Install Node + OpenClaw:
   ```bash
   npm install -g openclaw@latest
   openclaw onboard --install-daemon
   ```
4. **Note**: exe.dev storage may be ephemeral — back up `~/.openclaw/` if
   you want to persist agent state across rebuilds.

![](screenshots/04-exedev-terminal.png)

---

## Step 4 — Verify Installation

```bash
openclaw --version
openclaw doctor
openclaw gateway status
```

`openclaw doctor` should report all green checkmarks.

![](screenshots/05-doctor-output.png)

---

## Step 5 — Connect a Model Provider

Pick **one** provider. OpenAI and MiniMax support **OAuth sign-in** (no API key
needed — credentials are stored in `~/.openclaw/auth/`). DeepSeek still uses an
API key.

### Option A — OpenAI (OAuth, GPT-5.5)

1. Start the OAuth flow:
   ```bash
   openclaw auth login openai
   ```
2. The CLI prints a URL and opens your default browser. If it doesn't open
   automatically, copy the URL into a browser manually.
3. Sign in with your **OpenAI / ChatGPT account**.
4. On the consent screen, click **Authorize OpenClaw**. Approve the requested
   scopes (model access, billing read).
5. The browser shows `Authorization complete — you can close this tab.` and
   the CLI prints `✓ Logged in as <your-email>`.
6. Select GPT-5.5 as the active model:
   ```bash
   openclaw config set provider openai
   openclaw config set model openai/gpt-5.5
   ```
7. Verify:
   ```bash
   openclaw auth status
   openclaw model test
   ```

### Option B — DeepSeek (API key)
```bash
export DEEPSEEK_API_KEY="sk-..."
openclaw config set provider deepseek
openclaw config set model deepseek/deepseek-chat
```

### Option C — MiniMax (OAuth, MiniMax 2.7)

1. Start the OAuth flow:
   ```bash
   openclaw auth login minimax
   ```
2. The CLI prints a URL and opens your default browser. Copy it manually if
   the browser doesn't launch.
3. Sign in with your **MiniMax account** (email + password, or scan the
   MiniMax app QR code).
4. On the consent screen, click **Allow** to grant OpenClaw access to model
   inference and your group ID.
5. The browser shows `登录成功 / Login successful — return to your terminal.`
   The CLI prints `✓ Logged in as <your-account>` and the **group ID** is
   captured automatically.
6. Select MiniMax 2.7 as the active model:
   ```bash
   openclaw config set provider minimax
   openclaw config set model minimax/minimax-2.7
   ```
7. Verify:
   ```bash
   openclaw auth status
   openclaw model test
   ```

Confirm:
```bash
openclaw auth status
openclaw model list
openclaw model current
```

![](screenshots/06-model-set.png)

> **Tip**: For DeepSeek, persist `DEEPSEEK_API_KEY` in `~/.zshrc` (Mac/Linux)
> or System Environment Variables (Windows) so it survives reboots. OAuth
> tokens are persisted automatically.

---

## Step 6 — Add Your First Skill

```bash
openclaw skills list
openclaw skills add web-research
```

(Lab 3 covers skills in depth.)

---

## Step 7 — Setup Telegram Channel

1. Open Telegram and search for **@BotFather**.
2. Send `/newbot`.
3. Enter a **display name** (e.g. `My OpenClaw Bot`).
4. Enter a **username** — must be unique and **end in `_bot`**
   (e.g. `myopenclaw_bot`).
5. BotFather replies with an HTTP API **token** like
   `123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`. **Copy it.**

![](screenshots/07-botfather-token.png)

6. Register the channel:
   ```bash
   openclaw channel add telegram --token 123456789:ABC-DEF1234ghIkl-...
   openclaw channel start telegram
   ```
7. In Telegram, search for your bot's username and send `hello`.

---

## Step 8 — Pair WhatsApp

```bash
openclaw channel add whatsapp
openclaw channel start whatsapp
```

A QR code will print in your terminal.

1. On your phone: WhatsApp → **Settings → Linked Devices → Link a Device**.
2. Scan the QR code in your terminal.
3. Wait for `whatsapp: connected` in the OpenClaw log.

![](screenshots/08-whatsapp-qr.png)

> WhatsApp keeps a stateful session on disk. Don't delete `~/.openclaw/whatsapp/`
> unless you want to re-pair.

---

## Verification

End of lab — confirm **all four** work:

- `openclaw doctor` → all green
- Send a message to your **Telegram bot** → agent replies
- Send a message to the linked **WhatsApp** account → agent replies
- `openclaw gateway status` shows both channels running

---

## Troubleshooting

| Symptom | Fix |
|--------|-----|
| `openclaw: command not found` | Reopen terminal, or add `~/.openclaw/bin` to `PATH`. |
| `gateway not running` | `openclaw gateway start`. |
| Telegram bot doesn't reply | Re-check token; make sure model API key works (`openclaw model test`). |
| WhatsApp QR expired | Restart the channel: `openclaw channel restart whatsapp`. |
| Provider auth errors | Verify `echo $OPENAI_API_KEY` (etc.) returns the key. |

---

## Exercise

1. Switch your provider mid-conversation: `openclaw model use deepseek/deepseek-chat`
   and ask the bot the same question via Telegram. Note any quality/speed differences.
2. Add a **second** Telegram bot (different username) and confirm both can run
   simultaneously through one OpenClaw instance.

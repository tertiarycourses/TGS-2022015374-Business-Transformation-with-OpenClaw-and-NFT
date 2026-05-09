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

The same three-step flow works on any Ubuntu host — Hostinger VPS or
exe.dev sandbox. Pick one, then follow the steps below.

### 3A. Hostinger VPS (Ubuntu 22.04 KVM)

1. Buy/launch a KVM VPS from <https://www.hostinger.com?REFERRALCODE=FEGANGCHQ20C> (use this link for a 20% discount).
2. Log in to **hPanel** at <https://hpanel.hostinger.com/vps>.
3. Click your **VPS** → **Manage**.
4. On the VPS Overview page, click **Browser terminal** in the top-right
   corner. A web-based shell opens — no local SSH client needed.
5. Continue with the **Ubuntu install steps** below directly inside the
   browser terminal.

> **Tip**: Hostinger also offers **Kodee VPS Terminal Edition**, an AI
> sysadmin in the same panel that can run commands from natural-language
> prompts. See the
> [browser terminal guide](https://www.hostinger.com/support/7978544-how-to-use-the-browser-terminal-in-hostinger/)
> for details.

![](screenshots/03-hostinger-ssh.png)

### 3B. exe.dev sandbox (https://exe.dev/)

1. Sign up at <https://exe.dev/> and create a new dev sandbox.
2. Open the web terminal.
3. Continue with the **Ubuntu install steps** below.

> **Note**: exe.dev storage may be ephemeral — back up `~/.openclaw/` if
> you want to persist agent state across rebuilds.

![](screenshots/04-exedev-terminal.png)

### Ubuntu install steps (VPS or exe.dev)

**Step 1 — Install Node.js 24:**
```bash
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt-get install -y nodejs
node -v && npm -v
```

**Step 2 — Install OpenClaw globally:**
```bash
sudo npm install -g openclaw@latest
```

**Step 3 — Run the onboarding wizard:**
```bash
openclaw onboard
```

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

Pick **one** provider. OpenAI and MiniMax support **OAuth sign-in** (no API
key — credentials are stored in `~/.openclaw/auth/`). Anthropic, DeepSeek, and
OpenRouter use API keys.

### Option A — OpenAI Codex (OAuth, GPT-5.5)

OAuth uses the `openai-codex` provider, which lets you sign in with your
**ChatGPT Plus / Pro** subscription instead of paying per-token.

1. Start the OAuth flow:
   ```bash
   openclaw models auth login --provider openai-codex
   ```
   (Or run `openclaw onboard` and pick **`openai-codex`** at the auth-choice
   prompt.)
2. The terminal prints an authorization URL. **Copy it** and open it in a
   browser.
3. Sign in to your **OpenAI / ChatGPT account** and click **Authorize
   OpenClaw**.
4. After approval the browser is redirected to a callback URL. **Copy the
   entire callback URL** (including the `?code=…` query string) and paste it
   back into the terminal.
5. The wizard exchanges the code for an access token and saves the profile to
   `~/.openclaw/auth-profiles/openai-codex.json`. Refresh is automatic.
6. Select GPT-5.5 as the active model:
   ```bash
   openclaw models set openai-codex/gpt-5.5
   ```
7. Verify:
   ```bash
   openclaw models auth status
   openclaw models list
   ```

### Option B — MiniMax (OAuth, MiniMax-M2.7)

MiniMax exposes two OAuth realms — pick the one matching your account region.

1. Enable the OAuth plugin and restart the gateway:
   ```bash
   openclaw plugins enable minimax-portal-auth
   openclaw gateway restart
   ```
2. Start the OAuth flow (pick one):
   - **Global** (api.minimax.io):
     ```bash
     openclaw onboard --auth-choice minimax-global-oauth
     ```
   - **China** (api.minimaxi.com):
     ```bash
     openclaw onboard --auth-choice minimax-cn-oauth
     ```
   Or run directly:
   ```bash
   openclaw models auth login --provider minimax-portal --set-default
   ```
3. The CLI prints a **user code** and a verification URL. Open the URL in a
   browser, paste the code, and sign in to your **MiniMax account**.
4. Click **Allow** to grant OpenClaw access. The terminal prints
   `✓ Logged in` and the group ID is captured automatically.
5. Select MiniMax-M2.7 as the active model:
   ```bash
   openclaw models set minimax-portal/MiniMax-M2.7
   ```
   (Use `MiniMax-M2.7-highspeed` for the faster variant.)
6. Verify:
   ```bash
   openclaw models auth status
   openclaw models list
   ```

### Option C — Anthropic (API key, Claude Opus 4.7)

1. Get an API key from <https://console.anthropic.com/settings/keys>.
2. Export and configure:
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   openclaw config set provider anthropic
   openclaw config set model anthropic/claude-opus-4-7
   ```
3. Verify:
   ```bash
   openclaw model test
   ```

### Option D — DeepSeek (API key, V4)

1. Get an API key from <https://platform.deepseek.com/api_keys>.
2. Export and configure:
   ```bash
   export DEEPSEEK_API_KEY="sk-..."
   openclaw config set provider deepseek
   openclaw config set model deepseek/deepseek-v4
   ```
3. Verify:
   ```bash
   openclaw model test
   ```

### Option E — OpenRouter (API key, Claude Opus 4.7)

1. Get an API key from <https://openrouter.ai/keys>.
2. Export and configure:
   ```bash
   export OPENROUTER_API_KEY="sk-or-..."
   openclaw config set provider openrouter
   openclaw config set model openrouter/anthropic/claude-opus-4.7
   ```
3. Verify:
   ```bash
   openclaw model test
   ```

Confirm the active provider:
```bash
openclaw auth status
openclaw model list
openclaw model current
```

![](screenshots/06-model-set.png)

> **Tip**: Persist API keys (`ANTHROPIC_API_KEY`, `DEEPSEEK_API_KEY`,
> `OPENROUTER_API_KEY`) in `~/.zshrc` (Mac/Linux) or System Environment
> Variables (Windows) so they survive reboots. OAuth tokens are persisted
> automatically.

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

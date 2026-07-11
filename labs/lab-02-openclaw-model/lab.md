# Lab 2 — OpenClaw Model

Connect OpenClaw to a large language model (LLM). This lab covers four options: Groq (free tier), OpenAI (OAuth), Ollama (local), and the Default config file.

**Lab environment:** Hostinger VPS (from Lab 1) **or** Local machine with Docker Desktop (Windows 10/11, macOS 12+, Ubuntu 22.04+)

**Prerequisite:** Lab 1 completed — OpenClaw installed and gateway running.
**Estimated time:** 30 minutes

---

## Option A — Groq (Free Tier, Recommended)

Groq offers a genuinely free API with no credit card required. Fast inference with Llama 3.1 70B.

### Step A1 — Sign Up for Groq

Visit https://console.groq.com and create a free account.

### Step A2 — Get Your API Key

In the Groq console → **API Keys** → **Create API Key**.

Copy the key (it starts with `gsk_...`).

### Step A3 — Configure OpenClaw

```bash
openclaw model set groq \
  --api-key YOUR_GROQ_API_KEY \
  --model llama-3.1-70b-versatile
```

### Step A4 — Test the Model

```bash
openclaw model test
```

Expected output:
```
Provider: groq
Model:    llama-3.1-70b-versatile
Status:   ✓ Connected
Response: Hello! I am your OpenClaw agent.
```

---

## Option B — OpenAI (OAuth — 4-Step Process)

### Step B1 — Open Model Settings in OpenClaw

```bash
openclaw model set openai --oauth
```

### Step B2 — Authorise in Browser

OpenClaw prints a URL. Open it in your browser:

```
Open this URL to authorise OpenAI:
https://openclaw.ai/oauth/openai?state=xxxx
```

### Step B3 — Sign In with OpenAI Account

Log in with your OpenAI account. Click **Allow** to grant OpenClaw access.

### Step B4 — Confirm Token Saved

Return to your terminal. Expected output:

```
✓ OpenAI OAuth token saved.
Provider: openai
Model:    gpt-4o-mini (default)
```

Test:
```bash
openclaw model test
```

---

## Option C — Ollama (Local Model, No API Key)

Run a model completely on your own machine with zero cost.

### Step C1 — Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Step C2 — Launch OpenClaw's Recommended Model

```bash
ollama launch openclaw
```

This pulls and starts the `openclaw` model bundle optimised for agent tasks.

### Step C3 — Configure OpenClaw to Use Ollama

```bash
openclaw model set ollama \
  --host http://localhost:11434 \
  --model openclaw
```

### Step C4 — Test

```bash
openclaw model test
```

Expected output:
```
Provider: ollama
Model:    openclaw
Status:   ✓ Connected (local)
```

---

## Option D — Default Config File

Edit the OpenClaw config file directly to set any provider or model.

```bash
nano ~/.openclaw/openclaw.json
```

Example config:
```json
{
  "model": {
    "provider": "anthropic",
    "model": "claude-haiku-4-5-20251001",
    "apiKey": "sk-ant-..."
  }
}
```

Save and restart the gateway:
```bash
openclaw gateway restart
openclaw model test
```

---

## Verification

| Check | Expected |
|-------|----------|
| `openclaw model list` | Configured provider shown with status `active` |
| `openclaw model test` | `Status: ✓ Connected` |
| Chat test via Telegram (after Lab 3) | Agent replies with correct model name |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Invalid API key` for Groq | Re-copy the key — starts with `gsk_` |
| OAuth URL not opening | Copy the URL manually to a browser |
| Ollama model pull fails | Check disk space: `df -h` — need at least 4 GB free |
| `model test` times out | Confirm gateway is running: `openclaw gateway status` |

---

## Reference

- Providers: https://docs.openclaw.ai/providers
- Groq (free): https://console.groq.com
- Ollama: https://ollama.com

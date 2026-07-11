# Lab 2 — OpenClaw Model

Connect OpenClaw to a large language model (LLM). Choose one of the five providers below.

**Lab environment:** Hostinger VPS (from Lab 1) **or** Local machine with Docker Desktop (Windows 10/11, macOS 12+, Ubuntu 22.04+)

**Prerequisite:** Lab 1 completed — OpenClaw installed and gateway running.
**Estimated time:** 30 minutes

> **Docker Desktop users:** Prefix every `openclaw` command with `docker exec -it openclaw` — for example: `docker exec -it openclaw openclaw model set groq ...`

---

## Option A — Groq (Free Tier, Recommended for this lab)

Groq offers a genuinely free API — no credit card required. Fast inference with Llama models.

### Step A1 — Sign Up for Groq

Visit https://console.groq.com and create a free account.

### Step A2 — Get Your API Key

Groq console → **API Keys** → **Create API Key**.  
Copy the key — it starts with `gsk_`.

### Step A3 — Configure OpenClaw

**VPS:**
```bash
openclaw model set groq \
  --api-key YOUR_GROQ_API_KEY \
  --model llama-3.3-70b-versatile
```

**Docker Desktop:**
```bash
docker exec -it openclaw openclaw model set groq \
  --api-key YOUR_GROQ_API_KEY \
  --model llama-3.3-70b-versatile
```

### Step A4 — Test the Model

```bash
openclaw model test
# Docker: docker exec -it openclaw openclaw model test
```

Expected output:
```
Provider: groq
Model:    llama-3.3-70b-versatile
Status:   ✓ Connected
Response: Hello! I am your OpenClaw agent.
```

---

## Option B — OpenAI (API Key)

### Step B1 — Get Your API Key

Visit https://platform.openai.com/api-keys → **Create new secret key**.  
Copy the key — it starts with `sk-`.

### Step B2 — Configure OpenClaw

**VPS:**
```bash
openclaw model set openai \
  --api-key YOUR_OPENAI_API_KEY \
  --model gpt-4o-mini
```

**Docker Desktop:**
```bash
docker exec -it openclaw openclaw model set openai \
  --api-key YOUR_OPENAI_API_KEY \
  --model gpt-4o-mini
```

Available OpenAI models:

| Model | Speed | Cost | Best for |
|-------|-------|------|----------|
| `gpt-4o-mini` | Fast | Low | General agent tasks (recommended) |
| `gpt-4o` | Medium | Medium | Complex reasoning |
| `o1-mini` | Slow | Medium | Deep step-by-step reasoning |

### Step B3 — Test

```bash
openclaw model test
# Docker: docker exec -it openclaw openclaw model test
```

Expected output:
```
Provider: openai
Model:    gpt-4o-mini
Status:   ✓ Connected
```

---

## Option C — Anthropic Claude (API Key)

### Step C1 — Get Your API Key

Visit https://console.anthropic.com → **API Keys** → **Create Key**.  
Copy the key — it starts with `sk-ant-`.

### Step C2 — Configure OpenClaw

**VPS:**
```bash
openclaw model set anthropic \
  --api-key YOUR_ANTHROPIC_API_KEY \
  --model claude-haiku-4-5-20251001
```

**Docker Desktop:**
```bash
docker exec -it openclaw openclaw model set anthropic \
  --api-key YOUR_ANTHROPIC_API_KEY \
  --model claude-haiku-4-5-20251001
```

Available Claude models:

| Model | Speed | Cost | Best for |
|-------|-------|------|----------|
| `claude-haiku-4-5-20251001` | Fastest | Lowest | Lightweight agent tasks (recommended) |
| `claude-sonnet-5` | Medium | Medium | Balanced capability |
| `claude-opus-4-8` | Slower | Higher | Complex reasoning and writing |

### Step C3 — Test

```bash
openclaw model test
# Docker: docker exec -it openclaw openclaw model test
```

Expected output:
```
Provider: anthropic
Model:    claude-haiku-4-5-20251001
Status:   ✓ Connected
```

---

## Option D — OpenAI (OAuth — No API Key Needed)

### Step D1 — Start OAuth Flow

**VPS:**
```bash
openclaw model set openai --oauth
```

**Docker Desktop:**
```bash
docker exec -it openclaw openclaw model set openai --oauth
```

### Step D2 — Authorise in Browser

OpenClaw prints a URL. Open it in your browser:
```
Open this URL to authorise OpenAI:
https://openclaw.ai/oauth/openai?state=xxxx
```

### Step D3 — Sign In and Allow

Log in with your OpenAI account and click **Allow**.

### Step D4 — Confirm

Return to your terminal. Expected output:
```
✓ OpenAI OAuth token saved.
Provider: openai
Model:    gpt-4o-mini (default)
```

---

## Option E — Ollama (Local Model, No API Key, No Cost)

Run a model completely on your own machine.

### Step E1 — Install Ollama

**macOS / Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**  
Download the installer from https://ollama.com/download and run it.

### Step E2 — Pull a Model

```bash
ollama pull llama3.2
```

### Step E3 — Configure OpenClaw

**VPS:**
```bash
openclaw model set ollama \
  --host http://localhost:11434 \
  --model llama3.2
```

**Docker Desktop (Ollama on host machine):**
```bash
docker exec -it openclaw openclaw model set ollama \
  --host http://host.docker.internal:11434 \
  --model llama3.2
```

> On Docker Desktop, use `host.docker.internal` instead of `localhost` to reach Ollama running on the host machine.

### Step E4 — Test

```bash
openclaw model test
# Docker: docker exec -it openclaw openclaw model test
```

Expected output:
```
Provider: ollama
Model:    llama3.2
Status:   ✓ Connected (local)
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

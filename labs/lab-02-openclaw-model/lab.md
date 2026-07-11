# Lab 2 — OpenClaw Model

Connect OpenClaw to a large language model (LLM).

**Lab environment:** Hostinger VPS (from Lab 1) **or** Docker Desktop (Windows 10/11, macOS 12+, Ubuntu 22.04+)  
**Prerequisite:** Lab 1 completed — OpenClaw installed and gateway running.  
**Estimated time:** 30 minutes

> **No API key?** Use **Option F — Ollama**. It runs a model locally with no account and no cost.

---

## How to Run the Model Wizard

The model is configured through an **interactive wizard**. Run it once and follow the prompts.

**VPS:**
```bash
openclaw configure --section model
```

**Docker Desktop:**
```bash
docker exec -it openclaw openclaw configure --section model
```

The wizard shows a menu — use **arrow keys** to select your provider and press **Enter**.

---

## Option A — Groq (Free Tier, Recommended)

Groq offers a free API with no credit card required.

### Step A1 — Sign Up

Visit https://console.groq.com → create a free account.

### Step A2 — Get Your API Key

Groq console → **API Keys** → **Create API Key**.  
Copy the key — it starts with `gsk_`.

### Step A3 — Run the Wizard

```bash
# VPS
openclaw configure --section model

# Docker Desktop
docker exec -it openclaw openclaw configure --section model
```

In the wizard:
1. Select **More…**
2. Find and select **Groq**
3. Paste your `gsk_...` API key when prompted
4. Select model: `llama-3.3-70b-versatile`

---

## Option B — OpenAI (API Key)

### Step B1 — Get Your API Key

Visit https://platform.openai.com/api-keys → **Create new secret key**.  
Copy the key — it starts with `sk-`.

### Step B2 — Run the Wizard

```bash
# VPS
openclaw configure --section model

# Docker Desktop
docker exec -it openclaw openclaw configure --section model
```

In the wizard:
1. Select **OpenAI (ChatGPT/Codex sign-in or API key)**
2. Choose **API key** (not OAuth)
3. Paste your `sk-...` API key when prompted
4. Select model:

| Model | Speed | Cost | Best for |
|-------|-------|------|----------|
| `gpt-4o-mini` | Fast | Low | General agent tasks (recommended) |
| `gpt-4o` | Medium | Medium | Complex reasoning |
| `o1-mini` | Slow | Medium | Deep step-by-step reasoning |

---

## Option C — Anthropic Claude (API Key)

### Step C1 — Get Your API Key

Visit https://console.anthropic.com → **API Keys** → **Create Key**.  
Copy the key — it starts with `sk-ant-`.

### Step C2 — Run the Wizard

```bash
# VPS
openclaw configure --section model

# Docker Desktop
docker exec -it openclaw openclaw configure --section model
```

In the wizard:
1. Select **Anthropic**
2. Paste your `sk-ant-...` API key when prompted
3. Select model:

| Model | Speed | Cost | Best for |
|-------|-------|------|----------|
| `claude-haiku-4-5-20251001` | Fastest | Lowest | Lightweight tasks (recommended) |
| `claude-sonnet-5` | Medium | Medium | Balanced capability |
| `claude-opus-4-8` | Slower | Higher | Complex reasoning |

---

## Option D — OpenAI (OAuth — No API Key Needed)

### Step D1 — Run the Wizard

```bash
# VPS
openclaw configure --section model

# Docker Desktop
docker exec -it openclaw openclaw configure --section model
```

In the wizard:
1. Select **OpenAI (ChatGPT/Codex sign-in or API key)**
2. Choose **Sign in with OpenAI** (OAuth)
3. OpenClaw prints a URL — open it in your browser
4. Log in with your OpenAI account and click **Allow**
5. Return to the terminal — token is saved automatically

---

## Option E — Google Gemini (API Key)

### Step E1 — Get Your API Key

Visit https://aistudio.google.com/app/apikey → **Create API Key**.  
Copy the key — it starts with `AIza`.

### Step E2 — Run the Wizard

```bash
# VPS
openclaw configure --section model

# Docker Desktop
docker exec -it openclaw openclaw configure --section model
```

In the wizard:
1. Select **Google**
2. Paste your `AIza...` API key when prompted
3. Select model:

| Model | Speed | Cost | Best for |
|-------|-------|------|----------|
| `gemini-2.0-flash` | Fastest | Low | General agent tasks (recommended) |
| `gemini-2.0-pro` | Medium | Medium | Complex reasoning |
| `gemini-2.5-pro` | Slower | Higher | Advanced multimodal tasks |

---

## Option F — Ollama (Local Model, No API Key, No Cost)

### Step F1 — Install Ollama

**macOS / Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**  
Download and run the installer from https://ollama.com/download

### Step F2 — Pull a Model

```bash
ollama pull llama3.2
```

### Step F3 — Run the Wizard

```bash
# VPS
openclaw configure --section model

# Docker Desktop
docker exec -it openclaw openclaw configure --section model
```

In the wizard:
1. Select **More…**
2. Find and select **Ollama**
3. Enter the host:
   - VPS or native install: `http://localhost:11434`
   - Docker Desktop: `http://host.docker.internal:11434`
4. Enter model name: `llama3.2`

---

## Verify Model is Connected

After completing the wizard:

```bash
# VPS
openclaw models status

# Docker Desktop
docker exec -it openclaw openclaw models status
```

Expected output:
```
Provider: <your provider>
Model:    <your model>
Status:   ✓ Connected
```

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Unknown command: openclaw model` | Use `models` (plural) — `openclaw models status` |
| `--api-key not recognised` | Use the wizard: `openclaw configure --section model` |
| Groq key rejected | Key must start with `gsk_` — re-copy from console.groq.com |
| OpenAI key rejected | Key must start with `sk-` — re-copy from platform.openai.com/api-keys |
| Anthropic key rejected | Key must start with `sk-ant-` — re-copy from console.anthropic.com |
| Ollama not found | Start Ollama first: `ollama serve` then retry |
| Docker: Ollama unreachable | Use `http://host.docker.internal:11434` not `localhost` |
| `models status` shows disconnected | Re-run `openclaw configure --section model` and re-enter the key |

---

## Reference

- Providers: https://docs.openclaw.ai/providers
- Groq (free): https://console.groq.com
- OpenAI: https://platform.openai.com
- Anthropic: https://console.anthropic.com
- Google AI Studio: https://aistudio.google.com
- Ollama: https://ollama.com

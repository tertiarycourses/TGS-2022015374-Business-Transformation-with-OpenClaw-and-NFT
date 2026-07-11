# Lab 9 — OpenClaw Cost Saving

Reduce AI running costs through smart model selection, context management, and free-tier options.

**Lab environment:** Hostinger VPS (from Lab 1) **or** Docker Desktop (Windows 10/11, macOS 12+, Ubuntu 22.04+)  
**Prerequisite:** Lab 2 completed — a model provider configured.  
**Estimated time:** 20 minutes

> **Docker Desktop users:** Prefix every `openclaw` command with `docker exec -it openclaw`.

---

## Cost Overview

| Approach | Cost | Notes |
|----------|------|-------|
| Claude Opus 4.8 API | High | Best quality, pay per token |
| Claude Sonnet 5 API | Medium | Good balance |
| Claude Haiku 4.5 API | Low | Fast, cheap, good for simple tasks |
| Groq Llama 3.3 70B | Free tier | No credit card, fast inference |
| Google Gemini 2.0 Flash | Free tier | Generous free quota |
| Ollama (local) | Zero API cost | Runs on your hardware |

---

## Strategy 1 — Switch to a Cheaper Model

The fastest cost saving is switching to a smaller, cheaper model.

```bash
# VPS
openclaw configure --section model

# Docker Desktop
docker exec -it openclaw openclaw configure --section model
```

In the wizard, select your provider and choose a cheaper model:

| Switch | Cost Saving |
|--------|-------------|
| Claude Opus → Haiku | ~90% per token |
| GPT-4o → GPT-4o-mini | ~85% per token |
| Any paid → Groq Llama | ~100% (free tier) |

---

## Strategy 2 — Use Groq Free Tier for Testing

During learning and testing, Groq gives you fast inference for free.

```bash
# VPS
openclaw configure --section model

# Docker Desktop
docker exec -it openclaw openclaw configure --section model
```

In the wizard:
1. Select **More…** → **Groq**
2. Enter your `gsk_...` API key from https://console.groq.com
3. Select `llama-3.3-70b-versatile`

Switch back to a paid model for production when needed.

---

## Strategy 3 — Use Ollama for Zero-Cost Local Testing

No API costs — the model runs on your machine.

**Step 1 — Install Ollama:**

```bash
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows — download from https://ollama.com/download
```

**Step 2 — Pull a model:**
```bash
ollama pull llama3.2
```

**Step 3 — Configure OpenClaw:**
```bash
# VPS
openclaw configure --section model
# Select Ollama → host: http://localhost:11434 → model: llama3.2

# Docker Desktop
docker exec -it openclaw openclaw configure --section model
# Select Ollama → host: http://host.docker.internal:11434 → model: llama3.2
```

**Step 4 (Docker Desktop only) — Register the model in config:**

The wizard sets the default model but does not register the model entry. Run this to fix it:

```bash
docker exec openclaw sh -c 'cat > /tmp/fix-ollama.js << '"'"'EOF'"'"'
const fs=require("fs");
const p=process.env.HOME+"/.openclaw/openclaw.json";
const c=JSON.parse(fs.readFileSync(p));
if(!c.models) c.models={};
if(!c.models.providers) c.models.providers={};
if(!c.models.providers.ollama) c.models.providers.ollama={api:"ollama",baseUrl:"http://host.docker.internal:11434",models:[]};
if(!c.models.providers.ollama.models) c.models.providers.ollama.models=[];
const exists=c.models.providers.ollama.models.find(function(m){return m.id==="llama3.2";});
if(!exists) c.models.providers.ollama.models.push({id:"llama3.2",name:"llama3.2"});
c.models.providers.ollama.baseUrl="http://host.docker.internal:11434";
fs.writeFileSync(p,JSON.stringify(c,null,2));
console.log("done");
EOF'
MSYS_NO_PATHCONV=1 docker exec openclaw node /tmp/fix-ollama.js
```

Expected output: `done`

**Step 5 — Set as default and restart:**
```bash
docker exec -it openclaw openclaw models set ollama/llama3.2
docker restart openclaw
```

---

## Strategy 4 — Context Compaction

Context compaction summarises old conversation history to reduce tokens sent per request. This can cut costs by 50–70%.

```bash
# VPS
openclaw config set context.compaction enabled
openclaw config get context.compaction

# Docker Desktop
docker exec -it openclaw openclaw config set context.compaction enabled
docker exec -it openclaw openclaw config get context.compaction
```

Expected:
```
context.compaction: enabled
```

---

## Strategy 5 — Use Google Gemini Free Tier

Google Gemini 2.0 Flash has a generous free quota with no credit card needed for the free tier.

```bash
# VPS
openclaw configure --section model

# Docker Desktop
docker exec -it openclaw openclaw configure --section model
```

In the wizard:
1. Select **Google**
2. Enter your `AIza...` key from https://aistudio.google.com/app/apikey
3. Select `gemini-2.0-flash`

---

## Cost Saving Summary

| Action | Potential Saving |
|--------|----------------|
| Claude Opus → Haiku | ~90% per token |
| Switch to Groq free tier | 100% during testing |
| Switch to Ollama locally | 100% API cost |
| Enable context compaction | 50–70% per session |
| Google Gemini free tier | 100% within free quota |

---

## Verification

| Check | Expected |
|-------|----------|
| `openclaw configure --section model` | Wizard opens, model changeable |
| `openclaw config get context.compaction` | `enabled` |
| Chat test after model switch | Agent replies with new model |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| After switching model, agent stops responding | Re-run `openclaw configure --section model` and re-enter credentials |
| Ollama unreachable from Docker | Use `http://host.docker.internal:11434` not `localhost` |
| `Unknown model: ollama/llama3.2` error in logs | Run Step 4 above — the model must be registered in `models.providers.ollama.models[]` |
| Git Bash `!` expansion error in script | Use `MSYS_NO_PATHCONV=1` prefix before `docker exec` commands with Linux paths |
| Context compaction causes incomplete answers | Increase threshold: `openclaw config set context.compaction-threshold 100000` |
| Groq rate limits | Free tier has rate limits — wait 1 minute and retry |

---

## Reference

- Model providers: https://docs.openclaw.ai/providers
- Groq (free): https://console.groq.com
- Google AI Studio: https://aistudio.google.com
- Ollama: https://ollama.com

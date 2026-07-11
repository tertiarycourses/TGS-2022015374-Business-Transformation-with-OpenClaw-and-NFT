# Lab 9 — OpenClaw Cost Saving

Reduce your AI running costs by up to 90–97% through smart model selection, context management, and the Claude subscription option.

**Lab environment:** Hostinger VPS (from Lab 1) **or** Local machine with Docker Desktop

**Prerequisite:** Lab 2 completed — a model provider configured.
**Estimated time:** 20 minutes

---

## Cost Overview

| Approach | Estimated Cost | Notes |
|----------|---------------|-------|
| Claude API (Opus) | High | Best quality, pay per token |
| Claude API (Sonnet) | Medium | Good balance of quality and cost |
| Claude API (Haiku) | Low | Fast, cheap, good for simple tasks |
| Claude.ai Subscription | Fixed monthly | Unlimited usage within plan limits |
| MiniMax M2.7 (free tier) | Free | Great for learning and testing |
| Ollama (local) | Zero API cost | Runs on your hardware |

---

## Strategy 1 — Use Claude Subscription Instead of API

If you use Claude heavily, a Claude.ai subscription ($20/month) is cheaper than paying per API token.

### Step 1a — Enable Claude Subscription Mode

```bash
openclaw model set anthropic --subscription
```

Expected output:
```
Provider: anthropic
Mode:     subscription (claude.ai)
Model:    claude-sonnet-5 (default)
```

### Step 1b — Choose the Right Model Tier

| Model | Best For | Token Cost |
|-------|---------|-----------|
| `claude-haiku-4-5-20251001` | Simple questions, fast responses | Cheapest |
| `claude-sonnet-5` | General tasks, balanced quality | Medium |
| `claude-opus-4-8` | Complex reasoning, best quality | Most expensive |

Set Haiku for daily routine tasks:
```bash
openclaw model set anthropic \
  --model claude-haiku-4-5-20251001
openclaw model test
```

---

## Strategy 2 — Context Compaction

Context compaction summarises old conversation history to reduce the number of tokens sent to the model on each request. This can reduce costs by 50–70%.

### Step 2a — Enable Context Compaction

```bash
openclaw config set context.compaction enabled
openclaw config set context.compaction-threshold 50000
```

This tells OpenClaw to compact the context when it exceeds 50,000 tokens.

### Step 2b — Verify

```bash
openclaw config get context.compaction
```

Expected:
```
context.compaction: enabled
context.compaction-threshold: 50000
```

---

## Strategy 3 — Use MiniMax Free Tier for Testing

During development and testing, use the free MiniMax M2.7 model instead of a paid API.

```bash
openclaw model set minimax \
  --api-key YOUR_MINIMAX_API_KEY \
  --model abab6.5s-chat
openclaw model test
```

Switch back to Anthropic for production:
```bash
openclaw model set anthropic \
  --model claude-haiku-4-5-20251001
```

---

## Strategy 4 — Ollama for Zero-Cost Local Testing

No API costs at all — the model runs entirely on your machine.

```bash
openclaw model set ollama \
  --host http://localhost:11434 \
  --model openclaw
openclaw model test
```

**Note:** Requires a machine with at least 8 GB RAM for small models. Quality is lower than cloud models.

---

## Strategy 5 — Monitor Token Usage

```bash
openclaw usage stats
```

Expected output:
```
Period:       Last 30 days
Total tokens: 1,234,567
Estimated cost: $2.47
Top consumer:  firecrawl (34%)
```

Set a usage alert:
```bash
openclaw usage alert --threshold 5.00 --channel telegram
```

The agent will send a Telegram message when monthly spend exceeds $5.00.

---

## Verification

| Check | Expected |
|-------|----------|
| `openclaw model test` | Correct provider and model shown |
| `openclaw config get context.compaction` | `enabled` |
| `openclaw usage stats` | Token count and cost breakdown shown |
| Telegram alert | Fires when cost threshold is crossed |

---

## Cost Saving Summary

| Action | Potential Saving |
|--------|----------------|
| Switch Claude Opus → Haiku | ~90% reduction per token |
| Enable context compaction | ~50–70% reduction |
| Use MiniMax free tier for testing | 100% during development |
| Use Ollama for local testing | 100% API cost eliminated |
| Claude subscription vs. heavy API use | Breakeven at ~$20/month usage |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `openclaw usage stats` shows zero | Wait until at least one model call is made |
| Compaction causes incomplete context | Increase threshold: `openclaw config set context.compaction-threshold 100000` |
| Haiku quality too low for task | Switch up: `openclaw model set anthropic --model claude-sonnet-5` |

---

## Reference

- Model providers: https://docs.openclaw.ai/providers
- Claude models: https://www.anthropic.com/claude
- MiniMax: https://www.minimaxi.com
- Ollama: https://ollama.com

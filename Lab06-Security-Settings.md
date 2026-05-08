# Lab 6 — Security Settings for OpenClaw

## Objective
Lock down your OpenClaw deployment: protect API keys, restrict who can DM
the agent, sandbox dangerous tools, and audit what the agent has done.

## Prerequisites
- Labs 1–2 completed
- A public-facing channel (Telegram bot is ideal for this lab)

## Estimated Time
~30 minutes

---

## Step 1 — Secure API Keys

**Never** hardcode keys in scripts or commit them to git.

### Use environment variables, stored once

**macOS / Linux** — append to `~/.zshrc` or `~/.bashrc`:
```bash
export OPENAI_API_KEY="sk-..."
export FIRECRAWL_API_KEY="fc-..."
```

**Windows (PowerShell)** — set permanent user variable:
```powershell
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY","sk-...","User")
```

### Verify .env is gitignored
If you keep a project `.env`:
```bash
echo ".env" >> .gitignore
git rm --cached .env 2>/dev/null || true
```

### Inspect what OpenClaw stores
```bash
ls -la ~/.openclaw/
cat ~/.openclaw/config.toml | grep -i key   # confirm keys aren't pasted in cleartext
```

![](screenshots/lab6-01-env-vars.png)

---

## Step 2 — Pairing & Allowlists for DMs

By default, anyone who finds your Telegram bot can DM it — including strangers
who'll burn your API quota. Restrict access:

```bash
# Only allow specific Telegram user IDs to DM the bot
openclaw channel set telegram \
  --allow-users 12345678,87654321 \
  --pair-mode allowlist
```

For WhatsApp:
```bash
openclaw channel set whatsapp \
  --allow-numbers +6591234567,+6598765432
```

Group chats — restrict who can mention the bot:
```bash
openclaw channel set telegram --group-policy mention-only
```

---

## Step 3 — Tool Deny Lists

Block dangerous tools on public-facing channels:

```bash
# No shell exec or filesystem writes from Telegram
openclaw channel set telegram --deny exec,fs.write,fs.delete

# Allow only web tools on a public channel
openclaw channel set telegram --allow group:web
```

Use the `messaging` preset for safe defaults:
```bash
openclaw channel set telegram --profile messaging
```

Verify:
```bash
openclaw channel show telegram | grep -E "(allow|deny|profile)"
```

---

## Step 4 — Sandbox Limits for Code Execution

The Python / `exec` tool runs in a sandbox. Tighten the limits:

```bash
openclaw tools config exec \
  --timeout 10s \
  --memory 256mb \
  --network deny

openclaw tools config python \
  --timeout 30s \
  --memory 512mb \
  --network deny
```

![](screenshots/lab6-02-sandbox.png)

---

## Step 5 — Audit Logs

Every tool call, model call, and channel event is logged.

```bash
openclaw gateway logs --tail 100
openclaw gateway logs --filter tool=exec
openclaw gateway logs --since 1h --filter level=warn
openclaw gateway logs --export ~/openclaw-audit-$(date +%F).log
```

Review weekly. Anything unexpected — unknown user IDs, blocked tool
attempts, repeated auth failures — investigate.

---

## Step 6 — Rotate Provider Keys

Set a rotation calendar (e.g. every 90 days):

1. Generate a new key in the provider dashboard.
2. Update environment variable.
3. Restart gateway:
   ```bash
   openclaw gateway restart
   ```
4. Confirm `openclaw model test` still works.
5. **Revoke** the old key from the provider dashboard.

---

## Verification

- `cat ~/.openclaw/config.toml` does **not** contain raw API keys.
- A user not in your Telegram allowlist gets a polite "not authorized" reply
  (or no reply, depending on policy).
- `openclaw channel show telegram` lists `deny: exec, fs.write` (or your chosen
  policy).
- `openclaw gateway logs --filter tool=exec` shows blocked attempts when
  someone tries.

---

## Troubleshooting

| Symptom | Fix |
|--------|-----|
| Allowlist blocks **you** | Add your own Telegram user ID first; get it from `/whoami`. |
| Tool deny doesn't take effect | `openclaw gateway restart` — channel config is cached. |
| Logs grow huge | Rotate: `openclaw gateway logs rotate --keep 7`. |

---

## Exercise

1. Build a **threat model** for your bot in 1 page: who could abuse it, what
   the worst case is, what mitigations you applied.
2. Write a small bash script `check-openclaw-security.sh` that:
   - Fails if any provider key appears in `~/.openclaw/config.toml`
   - Fails if any channel has `exec` enabled with no allowlist
   - Prints a summary of currently-allowed users per channel

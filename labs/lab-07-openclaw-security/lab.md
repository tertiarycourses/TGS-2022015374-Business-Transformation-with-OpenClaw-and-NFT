# Lab 7 — OpenClaw Security

Apply the 10-step security hardening guide for OpenClaw. Protect your API keys, restrict channel access, sandbox the exec tool, and enable gateway authentication.

**Lab environment:** Hostinger VPS (from Lab 1) **or** Local machine with Docker Desktop

**Prerequisite:** Lab 3 completed — at least one channel running.
**Estimated time:** 30 minutes

---

## Security Checklist (10 Steps)

| # | Step | Purpose |
|---|------|---------|
| 1 | Store API keys as environment variables | Never hardcode secrets |
| 2 | Restrict channel access with an allowlist | Only authorised users can chat |
| 3 | Set a gateway authentication token | Protect the local API |
| 4 | Sandbox the exec tool | Limit shell access to a safe directory |
| 5 | Disable unused tools | Reduce attack surface |
| 6 | Enable audit logs | Track all agent activity |
| 7 | Rotate API keys regularly | Limit damage from leaks |
| 8 | Use HTTPS for webhook channels | Encrypt data in transit |
| 9 | Set resource limits (Docker) | Prevent runaway containers |
| 10 | Review SOUL.md and AGENTS.md | Control agent identity and permissions |

---

## Step 1 — Store API Keys as Environment Variables

**Never put keys inside config files or chat messages.**

**VPS — macOS / Linux:**
```bash
export MINIMAX_API_KEY="eyJ..."
export FIRECRAWL_API_KEY="fc-..."
export AGENTMAIL_API_KEY="am-..."
echo 'export MINIMAX_API_KEY="eyJ..."' >> ~/.bashrc
source ~/.bashrc
```

**Local — Windows PowerShell:**
```powershell
[Environment]::SetEnvironmentVariable("MINIMAX_API_KEY","eyJ...","User")
[Environment]::SetEnvironmentVariable("FIRECRAWL_API_KEY","fc-...","User")
```

Verify:
```bash
echo $MINIMAX_API_KEY
openclaw model test
```

---

## Step 2 — Restrict Channel Access with an Allowlist

Only users on the allowlist can send messages to your agent.

```bash
# Get your Telegram user ID from @userinfobot
openclaw channel config telegram \
  --allowlist-add YOUR_TELEGRAM_USER_ID

# Verify
openclaw channel config telegram --allowlist-show
```

Test: have a non-allowlisted person message the bot — they should receive `Access denied`.

---

## Step 3 — Set a Gateway Authentication Token

```bash
openclaw config set gateway.auth-token "$(openssl rand -hex 32)"
openclaw gateway restart
openclaw gateway status
```

Expected: `Gateway auth: Token (enabled)`

**Windows (PowerShell alternative):**
```powershell
$token = [System.Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))
openclaw config set gateway.auth-token $token
```

---

## Step 4 — Sandbox the Exec Tool

The exec tool can run arbitrary shell commands. Restrict it to a safe directory.

```bash
mkdir -p ~/openclaw-sandbox
openclaw tools config exec --sandbox-dir ~/openclaw-sandbox
openclaw gateway restart
```

**Docker users — sandbox inside the container:**
```bash
docker exec openclaw mkdir -p /root/openclaw-sandbox
docker exec openclaw openclaw tools config exec --sandbox-dir /root/openclaw-sandbox
docker restart openclaw
```

---

## Step 5 — Disable Unused Tools

```bash
openclaw tools list
openclaw tools disable exec   # if exec is not needed
openclaw tools list | grep exec
```

Expected: `exec    disabled`

---

## Step 6 — Enable and Review Audit Logs

```bash
openclaw logs --last 50
openclaw logs --tool firecrawl --last 20
openclaw logs --channel telegram --last 20
```

Export for review:
```bash
openclaw logs --export ~/openclaw-audit-$(date +%F).json
```

---

## Step 7 — Rotate API Keys

```bash
# Update the environment variable with the new key
export MINIMAX_API_KEY="eyJ-new-key..."
# Restart gateway to pick it up
openclaw gateway restart
openclaw model test
```

---

## Step 8 — Use HTTPS for Webhook Channels (VPS Only)

If you expose the gateway via a domain, always use HTTPS. Install Certbot:

```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d YOUR_DOMAIN
```

---

## Step 9 — Set Docker Resource Limits (Docker Users Only)

Prevent the container from consuming all system resources:

```bash
docker update openclaw \
  --memory 512m \
  --cpus 1.0
```

Verify:
```bash
docker stats openclaw --no-stream
```

---

## Step 10 — Review SOUL.md and AGENTS.md

These files define your agent's identity and capabilities.

```bash
cat ~/.openclaw/SOUL.md
cat ~/.openclaw/AGENTS.md
```

**Docker:**
```bash
docker exec openclaw cat /root/.openclaw/SOUL.md
docker exec openclaw cat /root/.openclaw/AGENTS.md
```

Remove any capabilities you did not intentionally grant.

---

## Verification

| Check | Expected |
|-------|----------|
| `echo $MINIMAX_API_KEY` | Key printed (not empty) |
| Telegram from non-allowlisted user | `Access denied` |
| `openclaw gateway status` | `Auth: Token enabled` |
| `openclaw tools list` | exec `sandboxed` or `disabled` |
| `openclaw logs --last 20` | Recent activity visible |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Model stops after key rotation | Re-export the env var and restart gateway |
| Allowlist blocks your own messages | Add your Telegram user ID: `--allowlist-add YOUR_ID` |
| Gateway fails after token set | Check: `openclaw config get gateway.auth-token` |
| Docker stats not showing | Confirm container is running: `docker ps` |

---

## Reference

- Security guide: https://docs.openclaw.ai/gateway/security
- SOUL.md reference: https://docs.openclaw.ai/soul

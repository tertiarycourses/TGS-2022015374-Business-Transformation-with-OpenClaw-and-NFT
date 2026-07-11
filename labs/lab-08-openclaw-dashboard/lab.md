# Lab 8 — OpenClaw Dashboard

Access the OpenClaw web dashboard to monitor your agent, view logs, manage plugins, and inspect memory — all from a browser.

**Lab environment:** Hostinger VPS (from Lab 1) **or** Docker Desktop (Windows 10/11, macOS 12+, Ubuntu 22.04+)  
**Prerequisite:** Lab 1 completed — gateway running on port 18789.  
**Estimated time:** 20 minutes

---

## Option A — Docker Desktop (Local Machine)

### Step A1 — Get Your Dashboard Token

The dashboard requires a token for authentication. Retrieve it:

```bash
docker exec openclaw sh -c 'node -e "const c=require(process.env.HOME+\"/.openclaw/openclaw.json\"); console.log(c.gateway.auth.token);"'
```

Copy the token printed.

### Step A2 — Open the Dashboard

Open your browser and go to:

```
http://localhost:18789/?token=YOUR_TOKEN_HERE
```

Replace `YOUR_TOKEN_HERE` with the token from Step A1.

### Step A3 — Or Launch via CLI

```bash
docker exec -it openclaw openclaw dashboard
```

This prints the full dashboard URL with token included. Copy and open it in your browser.

---

## Option B — VPS (SSH Tunnel)

The dashboard runs on the VPS but is not exposed publicly. Access it securely via SSH tunnel.

### Step B1 — Create an SSH Tunnel (on your local machine)

Open a terminal **on your local machine** (not on the VPS):

```bash
ssh -L 18789:localhost:18789 root@YOUR_VPS_IP
```

Keep this terminal open.

### Step B2 — Get the Dashboard URL on the VPS

On the VPS:
```bash
openclaw dashboard --no-open
```

This prints the URL with token. Open it in your local browser while the SSH tunnel is active.

---

## Step 3 — Explore the Dashboard

### View Live Logs

Click **Logs** in the sidebar. Send a message to your agent via Telegram — watch the log entry appear in real time.

### Inspect Memory Files

Click **Memory** to view:
- `MEMORY.md` — persistent notes your agent writes to itself
- `SOUL.md` — agent identity and persona
- `AGENTS.md` — sub-agent definitions

### View Plugins and Skills

Click **Plugins** to see all enabled and disabled plugins.  
Click **Skills** to see installed skills and their status.

### View Channel Status

Click **Channels** to see Telegram and WhatsApp connection status.

---

## Step 4 — Restart the Gateway from the Dashboard

Click **Gateway** → **Restart**. Wait 5 seconds and refresh the page.

Expected: Dashboard reconnects and shows `Gateway: running`.

---

## Verification

| Check | Expected |
|-------|----------|
| `http://localhost:18789/?token=YOUR_TOKEN` | Dashboard loads in browser |
| Logs panel | Real-time log entries visible after sending a Telegram message |
| Channels panel | Telegram shown as active |
| VPS: `openclaw dashboard --no-open` | Full URL with token printed |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Browser shows empty reply | Add `?token=YOUR_TOKEN` to the URL |
| `openclaw dashboard` opens wrong browser on VPS | Use `--no-open` and copy the URL manually |
| VPS tunnel: dashboard not loading | Confirm SSH command is still running in another terminal |
| Dashboard shows blank page | Hard-refresh the browser (Ctrl+Shift+R) |
| Token not found | Re-run: `docker exec openclaw sh -c 'node -e "const c=require(process.env.HOME+\"/.openclaw/openclaw.json\"); console.log(c.gateway.auth.token);"'` |

---

## Reference

- Dashboard: https://docs.openclaw.ai/dashboard
- SSH tunneling: https://support.hostinger.com/en/articles/ssh-tunneling

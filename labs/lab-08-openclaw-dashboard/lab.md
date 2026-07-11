# Lab 8 — OpenClaw Dashboard

Access the OpenClaw web dashboard to monitor your agent, view logs, manage tools, and inspect memory — all from a browser interface.

**Lab environment:** Hostinger VPS (from Lab 1) **or** Local machine with Docker Desktop

**Prerequisite:** Lab 1 completed — gateway running on port 18789.
**Estimated time:** 20 minutes

---

## Option A — Local Machine (Docker or Direct Install)

### Step A1 — Start the Dashboard

```bash
openclaw dashboard
```

Expected output:
```
OpenClaw Dashboard
URL: http://localhost:18789
Open this in your browser.
```

### Step A2 — Open in Browser

Open your web browser and go to:

```
http://localhost:18789
```

You will see the OpenClaw dashboard with:

| Panel | Description |
|-------|-------------|
| Overview | Agent name, model, uptime, gateway status |
| Channels | Active channels (Telegram, WhatsApp) and their status |
| Tools | Enabled tools and usage count |
| Skills | Installed skills and commands |
| Logs | Live log stream of agent activity |
| Memory | Contents of MEMORY.md, SOUL.md, AGENTS.md |
| Cron | Active cron jobs and next scheduled run |

---

## Option B — VPS (SSH Tunnel)

The dashboard runs on the VPS but is not exposed publicly. Access it securely via an SSH tunnel.

### Step B1 — Create an SSH Tunnel from Your Local Machine

Open a terminal **on your local machine** (not on the VPS) and run:

```bash
ssh -L 18789:localhost:18789 root@YOUR_VPS_IP
```

Keep this terminal open — the tunnel stays active as long as the SSH session is open.

### Step B2 — Open the Dashboard in Your Local Browser

While the SSH tunnel is active, open:

```
http://localhost:18789
```

This forwards your local port 18789 to the VPS port 18789 through the encrypted SSH tunnel.

---

## Step 3 — Explore the Dashboard

### View Live Logs

Click **Logs** in the sidebar. Send a message to your agent via Telegram — watch the log entry appear in real time.

### Inspect Memory Files

Click **Memory** to view:
- `MEMORY.md` — persistent notes your agent writes to itself
- `SOUL.md` — agent identity, persona, and values
- `AGENTS.md` — sub-agent definitions
- `HEARTBEAT.md` — heartbeat configuration

### Test a Tool from the Dashboard

Click **Tools** → select `firecrawl` → **Test**. Enter a URL and click **Run**.

---

## Step 4 — Restart the Gateway from the Dashboard

Click **Gateway** → **Restart**. Wait 5 seconds, then refresh the page.

Expected: Dashboard reconnects and shows `Gateway: running`.

---

## Verification

| Check | Expected |
|-------|----------|
| `http://localhost:18789` opens | Dashboard loads in browser |
| Logs panel | Real-time log entries visible |
| Channels panel | Telegram / WhatsApp shown as active |
| Memory panel | MEMORY.md contents visible |
| VPS SSH tunnel: `http://localhost:18789` | Dashboard loads via SSH tunnel |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `http://localhost:18789` — connection refused | Run `openclaw gateway status`; start if not running |
| VPS tunnel: dashboard not loading | Confirm SSH command is still running in another terminal |
| Dashboard shows blank page | Hard-refresh the browser (Ctrl+Shift+R) |
| Docker: port not reachable | Confirm container started with `-p 18789:18789` |

---

## Reference

- Dashboard: https://docs.openclaw.ai/dashboard
- SSH tunnel guide: https://support.hostinger.com/en/articles/ssh-tunneling

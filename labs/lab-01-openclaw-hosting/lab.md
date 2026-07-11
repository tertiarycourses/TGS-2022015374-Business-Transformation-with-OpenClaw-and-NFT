# Lab 1 — OpenClaw Hosting

Install and start OpenClaw. Choose one of the two environments:

- **Option A — Hostinger VPS (Cloud):** Runs 24/7, accessible from anywhere.
- **Option B — Docker Desktop (Local):** Runs on your own laptop, ideal for learning and testing.

**Prerequisite:** None. Start here.
**Estimated time:** 30 minutes

---

## Option A — Hostinger VPS (Ubuntu 22.04 LTS)

Recommended for production use. Sign up with the referral link for a discount:
[https://www.hostinger.com?REFERRALCODE=FEGANGCHQ20C](https://www.hostinger.com?REFERRALCODE=FEGANGCHQ20C)

### Step A1 — Connect to Your VPS

```bash
ssh root@YOUR_VPS_IP
```

Replace `YOUR_VPS_IP` with the IP shown in your Hostinger hPanel.

### Step A2 — Install OpenClaw

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

Expected output:
```
Installing OpenClaw...
✓ Node.js runtime detected
✓ OpenClaw CLI installed
✓ Gateway daemon registered
OpenClaw v1.x.x installed successfully.
Run: openclaw onboard
```

### Step A3 — Run the Onboarding Wizard

```bash
openclaw onboard
```

When prompted:
1. Enter a display name for your agent (e.g. `Alfred`)
2. Skip model setup for now (press Enter) — configure in Lab 2
3. Start the gateway now: `y`

### Step A4 — Enable Auto-Start

```bash
openclaw daemon install
systemctl status openclaw
```

Expected: `Active: active (running)`

### Step A5 — Verify Gateway

```bash
openclaw --version
openclaw gateway status
```

Expected:
```
openclaw/1.x.x linux-x64 node-v20.x.x
Gateway: running
Port:    18789
```

---

## Option B — Docker Desktop (Local Machine)

No VPS needed. OpenClaw runs inside a Docker container on Windows, macOS, or Linux.

**Prerequisite:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

### Step B1 — Pull the OpenClaw Docker Image

```bash
docker pull openclaw/openclaw:latest
```

Expected output:
```
latest: Pulling from openclaw/openclaw
...
Status: Downloaded newer image for openclaw/openclaw:latest
```

### Step B2 — Create the Config

The gateway needs a config file before it can start. This step creates it and saves it to a named volume so it persists across container restarts.

**Windows (Git Bash):**
```bash
MSYS_NO_PATHCONV=1 docker run --rm \
  -v openclaw-data:/home/node/.openclaw \
  openclaw/openclaw:latest \
  sh -c "openclaw setup --non-interactive --mode local --accept-risk; echo 'setup done'"
```

**macOS / Linux:**
```bash
docker run --rm \
  -v openclaw-data:/home/node/.openclaw \
  openclaw/openclaw:latest \
  sh -c "openclaw setup --non-interactive --mode local --accept-risk; echo 'setup done'"
```

Expected output (all platforms):
```
Updated config: ~/.openclaw/openclaw.json
Workspace OK: ~/.openclaw/workspace
Sessions OK: ~/.openclaw/agents/main/sessions
setup done
```

> **Windows Git Bash note:** `MSYS_NO_PATHCONV=1` prevents Git Bash from converting Linux paths like `/home/node` to Windows paths before passing them to Docker. Always include it on Windows.

### Step B3 — Set Gateway to LAN Mode

By default the gateway only listens on loopback (127.0.0.1 inside the container) — the host browser cannot reach it. This step changes `bind` to `lan` so it listens on all interfaces.

**Windows (Git Bash):**
```bash
MSYS_NO_PATHCONV=1 docker run --rm \
  -v openclaw-data:/home/node/.openclaw \
  openclaw/openclaw:latest \
  node -e "
const fs=require('fs');
const f='/home/node/.openclaw/openclaw.json';
const c=JSON.parse(fs.readFileSync(f));
c.gateway.bind='lan';
fs.writeFileSync(f,JSON.stringify(c,null,2));
console.log('bind set to lan');
"
```

**macOS / Linux:**
```bash
docker run --rm \
  -v openclaw-data:/home/node/.openclaw \
  openclaw/openclaw:latest \
  node -e "
const fs=require('fs');
const f='/home/node/.openclaw/openclaw.json';
const c=JSON.parse(fs.readFileSync(f));
c.gateway.bind='lan';
fs.writeFileSync(f,JSON.stringify(c,null,2));
console.log('bind set to lan');
"
```

Expected output: `bind set to lan`

### Step B4 — Start the OpenClaw Container

**Windows (Git Bash):**
```bash
MSYS_NO_PATHCONV=1 docker run -d \
  --name openclaw \
  -p 18789:18789 \
  -v openclaw-data:/home/node/.openclaw \
  openclaw/openclaw:latest
```

**macOS / Linux:**
```bash
docker run -d \
  --name openclaw \
  -p 18789:18789 \
  -v openclaw-data:/home/node/.openclaw \
  openclaw/openclaw:latest
```

| Flag | Purpose |
|------|---------|
| `-d` | Run in background (detached) |
| `-p 18789:18789` | Expose gateway port to host |
| `-v openclaw-data:/home/node/.openclaw` | Mount the config volume from Steps B2–B3 |

Confirm it is healthy (all platforms):
```bash
docker ps
```

Expected: `openclaw` with status `Up (healthy)` and port `0.0.0.0:18789->18789/tcp`.

### Step B5 — Get Your Dashboard Token

The dashboard requires a token for authentication. Retrieve it from the config (all platforms):

```bash
docker exec openclaw sh -c 'node -e "const c=require(process.env.HOME+\"/\.openclaw/openclaw.json\"); console.log(c.gateway.auth.token);"'
```

Copy the token printed — you will need it in the next step.

### Step B6 — Open the Dashboard

Open your browser and navigate to (all platforms):

```
http://localhost:18789/?token=YOUR_TOKEN_HERE
```

Replace `YOUR_TOKEN_HERE` with the token copied from Step B5.

You should see the OpenClaw web dashboard. You are now ready to proceed to Lab 2.

---

## Verification

| Check | Expected |
|-------|----------|
| VPS: `openclaw --version` | Version string printed |
| VPS: `openclaw gateway status` | `Gateway: running` on port 18789 |
| VPS: `systemctl status openclaw` | `Active: active (running)` |
| Docker: `docker ps` | `openclaw` container — status `Up (healthy)`, port `0.0.0.0:18789->18789/tcp` |
| Browser: `http://localhost:18789/?token=YOUR_TOKEN` | OpenClaw dashboard loads |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| VPS: `curl: command not found` | Run `apt install curl -y` first |
| VPS: `openclaw: command not found` after install | Run `source ~/.bashrc` or reconnect SSH |
| VPS: Port 18789 blocked | Open in Hostinger hPanel → Firewall → Allow 18789 TCP |
| Docker: `Cannot connect to Docker daemon` | Start Docker Desktop first |
| Docker: Container exits with code 78 | Run Step B2 (setup) first — daemon needs config before starting |
| Docker: Config not found even after setup | Volume must mount to `/home/node/.openclaw` (container runs as user `node`, not root) |
| Git Bash path errors in volume mounts | Prefix every `docker run` with `MSYS_NO_PATHCONV=1` |
| Docker: Browser shows empty reply or can't connect | Run Step B3 to set `bind=lan` — default is loopback-only |
| Docker: Dashboard says "token missing" | Open URL as `http://localhost:18789/?token=YOUR_TOKEN` (see Step B5) |
| Docker: Port 18789 already in use | `netstat -ano \| findstr 18789` (Windows) to find and stop the conflicting process |

---

## Reference

- OpenClaw install: https://docs.openclaw.ai/install
- Hostinger VPS: https://support.hostinger.com/en/articles/vps-getting-started
- Docker Desktop: https://docs.docker.com/desktop/

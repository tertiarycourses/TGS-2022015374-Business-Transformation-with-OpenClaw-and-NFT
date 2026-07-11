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

### Step B2 — Run the Onboarding Wizard

The onboarding wizard must run **before** starting the gateway — it creates the config file that the daemon needs.

```bash
docker run -it --rm \
  -v openclaw-data:/root/.openclaw \
  openclaw/openclaw:latest openclaw onboard
```

When prompted:
1. Enter a display name (e.g. `Alfred`)
2. Skip model setup for now — configure in Lab 2
3. Start the gateway: `y`

> The `-v openclaw-data:/root/.openclaw` volume saves the config so it persists when you restart the container.

### Step B3 — Start the OpenClaw Container

Now that the config exists, start the daemon in background:

```bash
docker run -d \
  --name openclaw \
  -p 18789:18789 \
  -v openclaw-data:/root/.openclaw \
  openclaw/openclaw:latest
```

| Flag | Purpose |
|------|---------|
| `-d` | Run in background (detached) |
| `-p 18789:18789` | Expose gateway port |
| `-v openclaw-data:/root/.openclaw` | Mount the config volume created in Step B2 |

Confirm the container is running:

```bash
docker ps
```

Expected: `openclaw` with status `Up`.

### Step B4 — Verify Gateway

```bash
docker exec openclaw openclaw --version
docker exec openclaw openclaw gateway status
```

Expected:
```
openclaw/1.x.x linux-x64 node-v20.x.x
Gateway: running
Port:    18789
```

### Step B5 — Access OpenClaw CLI from Host

To avoid typing `docker exec openclaw` every time, create a shell alias:

**macOS / Linux:**
```bash
echo 'alias openclaw="docker exec -it openclaw openclaw"' >> ~/.zshrc
source ~/.zshrc
```

**Windows (PowerShell profile):**
```powershell
Add-Content $PROFILE 'function openclaw { docker exec -it openclaw openclaw @args }'
. $PROFILE
```

Now you can simply type `openclaw gateway status` directly.

---

## Verification

| Check | Expected |
|-------|----------|
| `openclaw --version` | Version string printed |
| `openclaw gateway status` | `Gateway: running` on port 18789 |
| VPS: `systemctl status openclaw` | `Active: active (running)` |
| Docker: `docker ps` | `openclaw` container status `Up` |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| VPS: `curl: command not found` | Run `apt install curl -y` first |
| VPS: `openclaw: command not found` after install | Run `source ~/.bashrc` or reconnect SSH |
| VPS: Port 18789 blocked | Open in Hostinger hPanel → Firewall → Allow 18789 TCP |
| Docker: `Cannot connect to Docker daemon` | Start Docker Desktop first |
| Docker: Container exits with code 78 | Run Step B2 (onboard) first — the daemon needs config before it can start |
| Docker: Port 18789 already in use | Stop whatever uses that port: `netstat -ano | findstr 18789` (Windows) |

---

## Reference

- OpenClaw install: https://docs.openclaw.ai/install
- Hostinger VPS: https://support.hostinger.com/en/articles/vps-getting-started
- Docker Desktop: https://docs.docker.com/desktop/

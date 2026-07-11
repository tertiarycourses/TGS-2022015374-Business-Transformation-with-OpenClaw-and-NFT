# Lab 6 — Cron Jobs and Heartbeat

Schedule recurring agent tasks with cron jobs and monitor agent uptime with heartbeat.

**Lab environment:** Hostinger VPS (from Lab 1) **or** Docker Desktop (Windows 10/11, macOS 12+, Ubuntu 22.04+)  
**Prerequisite:** Lab 3 completed — at least one channel active.  
**Estimated time:** 30 minutes

> **Docker Desktop users:** Prefix every `openclaw` command with `docker exec -it openclaw`.  
> Example: `docker exec -it openclaw openclaw cron list`

---

## Cron vs Heartbeat

| Feature | Cron Jobs | Heartbeat |
|---------|-----------|-----------|
| Purpose | Run a task on a schedule | Confirm the agent is alive |
| Trigger | Time-based (e.g. every morning) | Interval ping |
| Output | Task result sent to channel | Short status message |
| Use case | Daily reports, weekly research | Uptime monitoring |

---

## Part A — Cron Jobs

### Step A1 — Create a Daily Morning Briefing

```bash
# VPS
openclaw cron add \
  --cron "0 9 * * *" \
  --name morning-briefing \
  --channel telegram \
  "Summarise today's top AI news"

# Docker Desktop
docker exec -it openclaw openclaw cron add \
  --cron "0 9 * * *" \
  --name morning-briefing \
  --channel telegram \
  "Summarise today's top AI news"
```

Cron syntax: `minute hour day month weekday`  
`0 9 * * *` = every day at 9:00 AM

---

### Step A2 — Create a Weekly Research Cron

```bash
# VPS
openclaw cron add \
  --cron "0 8 * * 1" \
  --name weekly-ai-news \
  --channel telegram \
  "Research top AI agent news this week and send a summary"

# Docker Desktop
docker exec -it openclaw openclaw cron add \
  --cron "0 8 * * 1" \
  --name weekly-ai-news \
  --channel telegram \
  "Research top AI agent news this week and send a summary"
```

`0 8 * * 1` = every Monday at 8:00 AM

---

### Step A3 — List All Cron Jobs

```bash
# VPS
openclaw cron list

# Docker Desktop
docker exec -it openclaw openclaw cron list
```

Expected output:
```
NAME               SCHEDULE      CHANNEL     STATUS
morning-briefing   0 9 * * *     telegram    enabled
weekly-ai-news     0 8 * * 1     telegram    enabled
```

---

### Step A4 — Run a Cron Immediately (Test)

```bash
# VPS
openclaw cron run morning-briefing

# Docker Desktop
docker exec -it openclaw openclaw cron run morning-briefing
```

Expected: Telegram receives the briefing without waiting for the schedule.

---

### Step A5 — Disable and Enable a Cron

```bash
# VPS
openclaw cron disable morning-briefing
openclaw cron list
openclaw cron enable morning-briefing

# Docker Desktop
docker exec -it openclaw openclaw cron disable morning-briefing
docker exec -it openclaw openclaw cron enable morning-briefing
```

---

### Step A6 — Delete a Cron

```bash
# VPS
openclaw cron rm weekly-ai-news

# Docker Desktop
docker exec -it openclaw openclaw cron rm weekly-ai-news
```

---

## Part B — Heartbeat

Heartbeat sends a regular ping to confirm the agent and gateway are running.

### Step B1 — Enable Heartbeat

```bash
# VPS
openclaw system heartbeat enable

# Docker Desktop
docker exec -it openclaw openclaw system heartbeat enable
```

### Step B2 — Check Last Heartbeat

```bash
# VPS
openclaw system heartbeat last

# Docker Desktop
docker exec -it openclaw openclaw system heartbeat last
```

### Step B3 — Disable Heartbeat

```bash
# VPS
openclaw system heartbeat disable

# Docker Desktop
docker exec -it openclaw openclaw system heartbeat disable
```

---

## Verification

| Check | Expected |
|-------|----------|
| `openclaw cron list` | `morning-briefing` shown as `enabled` |
| `openclaw cron run morning-briefing` | Telegram receives the briefing immediately |
| `openclaw system heartbeat last` | Last heartbeat timestamp shown |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Cron does not fire on schedule | Gateway must be running continuously — check `openclaw gateway status` |
| `cron run` returns error | Verify channel is active: `openclaw channels status` |
| Docker: cron fires but no Telegram message | Confirm bot token and pairing are still valid |
| `cron rm` not found | Command is `rm` not `delete` |

---

## Reference

- Cron docs: https://docs.openclaw.ai/cron
- Heartbeat: https://docs.openclaw.ai/heartbeat

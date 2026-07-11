# Lab 6 — Cron Jobs and Heartbeat

Schedule recurring agent tasks with cron jobs and monitor agent uptime with the heartbeat feature. Also learn when to use each.

**Lab environment:** Hostinger VPS (from Lab 1) **or** Local machine with Docker Desktop

**Prerequisite:** Lab 5 completed — at least one channel active and at least one skill installed.
**Estimated time:** 30 minutes

---

## Cron vs Heartbeat — Decision Guide

| Feature | Cron Jobs | Heartbeat |
|---------|-----------|-----------|
| Purpose | Run a task on a schedule | Confirm the agent is alive |
| Trigger | Time-based (e.g. every morning) | Interval ping (e.g. every 30 min) |
| Output | Task result sent to channel | Short status message sent to channel |
| Use case | Daily reports, weekly research | Uptime monitoring, alerting |
| Configured in | `openclaw cron` commands | `HEARTBEAT.md` or `openclaw heartbeat` |

---

## Part A — Cron Jobs

### Cron Syntax

```
<minute> <hour> <day-of-month> <month> <day-of-week>
```

| Symbol | Meaning |
|--------|---------|
| `*` | Every |
| `0 9 * * *` | Every day at 9:00 AM |
| `0 8 * * 1` | Every Monday at 8:00 AM |

---

### Step A1 — Create a Daily Morning Briefing Cron

```bash
openclaw cron create \
  --schedule "0 9 * * *" \
  --prompt "Summarise my unread email from the last 24 hours and give me today's top AI news" \
  --channel telegram \
  --name morning-briefing
```

---

### Step A2 — Create a Weekly Research Cron

```bash
openclaw cron create \
  --schedule "0 8 * * 1" \
  --prompt "/web-research top AI agent news this week" \
  --channel telegram \
  --name weekly-ai-news
```

---

### Step A3 — List All Cron Jobs

```bash
openclaw cron list
```

Expected output:
```
NAME               SCHEDULE      CHANNEL     STATUS
morning-briefing   0 9 * * *     telegram    active
weekly-ai-news     0 8 * * 1     telegram    active
```

---

### Step A4 — Run a Cron Immediately (Test)

```bash
openclaw cron run morning-briefing
```

Expected: Telegram receives the morning briefing immediately without waiting for the schedule.

---

### Step A5 — Pause and Resume a Cron

```bash
openclaw cron pause morning-briefing
openclaw cron list
```

Expected: `morning-briefing` shows status `paused`.

```bash
openclaw cron resume morning-briefing
```

---

### Step A6 — Delete a Cron

```bash
openclaw cron delete weekly-ai-news
openclaw cron list
```

Expected: `weekly-ai-news` no longer in the list.

---

## Part B — Heartbeat

Heartbeat sends a regular ping to your channel to confirm the agent is alive and the gateway is running.

### Step B1 — Configure Heartbeat via HEARTBEAT.md

```bash
nano ~/.openclaw/HEARTBEAT.md
```

Add:
```markdown
# Heartbeat

- interval: 30m
- channel: telegram
- message: "✅ OpenClaw is alive"
```

Save and exit (`Ctrl+X`, `Y`, `Enter`).

**Docker users:**
```bash
docker exec -it openclaw nano /root/.openclaw/HEARTBEAT.md
```

---

### Step B2 — Enable Heartbeat via CLI

Alternatively, use the CLI:

```bash
openclaw heartbeat enable \
  --interval 30m \
  --channel telegram \
  --message "✅ OpenClaw is alive"
```

---

### Step B3 — Check Heartbeat Status

```bash
openclaw heartbeat status
```

Expected output:
```
Heartbeat: enabled
Interval:  30m
Channel:   telegram
Last ping: 2026-07-11 09:30:00
```

---

### Step B4 — Disable Heartbeat

```bash
openclaw heartbeat disable
openclaw heartbeat status
```

Expected: `Heartbeat: disabled`

---

## Verification

| Check | Expected |
|-------|----------|
| `openclaw cron list` | `morning-briefing` active |
| `openclaw cron run morning-briefing` | Telegram receives the briefing |
| `openclaw heartbeat status` | `enabled`, interval 30m |
| Telegram after 30 min | ✅ heartbeat message arrives |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Cron does not fire on schedule | Check: `openclaw gateway status` — gateway must be running |
| `cron run` returns error | Verify channel is active: `openclaw channel list` |
| Heartbeat messages not arriving | Confirm telegram channel started: `openclaw channel start telegram` |
| Docker: changes to HEARTBEAT.md not picked up | Restart container: `docker restart openclaw` |

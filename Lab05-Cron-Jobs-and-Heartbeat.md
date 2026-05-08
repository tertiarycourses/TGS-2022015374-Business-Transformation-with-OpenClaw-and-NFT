# Lab 5 — Cron Jobs & Heartbeat

## Objective
Schedule recurring agent tasks with **cron** and monitor agent uptime with
**heartbeat** so your OpenClaw runs reliably 24/7.

## Prerequisites
- Labs 1–2 completed (channels + at least one third-party tool)

## Estimated Time
~30 minutes

---

## Part A — Cron Jobs

### Create a Cron

Cron syntax: `<min> <hour> <day> <month> <weekday>`.

```bash
# Daily at 09:00 — summarize unread email
openclaw cron create \
  --schedule "0 9 * * *" \
  --prompt "Summarize my unread email from the last 24 hours" \
  --channel telegram \
  --name morning-email
```

```bash
# Every Monday at 08:00 — weekly news brief via Firecrawl
openclaw cron create \
  --schedule "0 8 * * 1" \
  --prompt "Use Firecrawl to fetch https://news.ycombinator.com/ and post the top 5 stories" \
  --channel telegram \
  --name weekly-news
```

![](screenshots/lab5-01-cron-create.png)

### List & Inspect

```bash
openclaw cron list
openclaw cron show morning-email
openclaw cron logs morning-email --tail 20
```

### Disable / Delete

```bash
openclaw cron disable morning-email
openclaw cron enable  morning-email
openclaw cron delete  morning-email
```

### Run on Demand
```bash
openclaw cron run morning-email     # fire immediately, ignoring schedule
```

---

## Part B — Heartbeat

The **heartbeat** is a periodic self-check that ensures the gateway is alive,
the model provider responds, and channels are connected. If anything fails,
the daemon attempts auto-restart and logs the incident.

### Enable / Configure
```bash
openclaw gateway heartbeat enable --interval 60s
openclaw gateway heartbeat status
openclaw gateway heartbeat logs --tail 20
```

### Optional — External Webhook

Push a heartbeat ping to an external monitor (e.g. healthchecks.io,
Better Stack):
```bash
openclaw gateway heartbeat webhook \
  --url https://hc-ping.com/<your-uuid> \
  --interval 5m
```

If OpenClaw goes down, your monitor stops receiving pings and pages you.

![](screenshots/lab5-02-heartbeat.png)

### Auto-Restart Daemon

Make sure the daemon was installed in Lab 1:
```bash
openclaw gateway status         # should show "running" + "auto-start: yes"
openclaw gateway install        # (re)install if not auto-starting
```

---

## Verification

- `openclaw cron list` shows your two scheduled jobs.
- The 9 a.m. cron actually fires (use `openclaw cron run morning-email` to test now).
- `openclaw gateway heartbeat status` says **healthy**.
- Killing the gateway (`openclaw gateway stop`) and waiting 60 s causes the
  service manager (LaunchAgent / systemd / Task Scheduler) to restart it
  — confirm with `openclaw gateway status`.

---

## Troubleshooting

| Symptom | Fix |
|--------|-----|
| Cron created but never fires | Check daemon: `openclaw gateway status`. Cron only fires while the gateway runs. |
| Cron fires but no message arrives | `openclaw cron logs <name>` — usually a model/channel issue. |
| Heartbeat shows "unhealthy: provider" | API key expired or out of credits. Re-check Lab 1 step 5. |
| Auto-restart not working | Re-run `openclaw gateway install`; verify in OS service manager. |

---

## Exercise

1. Create a cron that, **every weekday at 6 p.m.**, sends a Telegram message
   asking you "What did you ship today?" and saves your reply to a file under
   `~/.openclaw/journal/YYYY-MM-DD.md`.
2. Wire up a free <https://healthchecks.io/> check and connect the OpenClaw
   heartbeat webhook to it. Confirm you get alerted within 5 min when you
   stop the gateway.

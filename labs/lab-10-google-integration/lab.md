# Lab 10 — Google Integration for OpenClaw

Connect OpenClaw to Google Workspace so your agent can read Gmail, check Google Calendar, and post to Google Chat — using a Google Cloud service account.

**Lab environment:** Hostinger VPS (from Lab 1) **or** Local machine with Docker Desktop

**Prerequisite:** Lab 4 completed — tools configured. A Google account (personal or Workspace).
**Estimated time:** 40 minutes

---

## Overview

| Google Service | What OpenClaw Can Do |
|---------------|---------------------|
| Gmail | Read emails, send replies, filter by label |
| Google Calendar | Read events, create reminders |
| Google Chat | Post messages to spaces |

---

## Step 1 — Create a Google Cloud Project

1. Go to: https://console.cloud.google.com/
2. Click **Select a project** → **New Project**
3. Name it `openclaw-integration` → **Create**
4. Note the **Project ID** (you need it later)

---

## Step 2 — Enable the Required APIs

In the Google Cloud Console, go to **APIs & Services** → **Library** and enable each of:

| API | Enable Link |
|-----|------------|
| Gmail API | Search: `Gmail API` → Enable |
| Google Calendar API | Search: `Google Calendar API` → Enable |
| Google Chat API | Search: `Google Chat API` → Enable |

---

## Step 3 — Create a Service Account

1. Go to **IAM & Admin** → **Service Accounts** → **Create Service Account**
2. Name: `openclaw-agent`
3. Role: **Editor** (or a more restrictive role for production)
4. Click **Done**

---

## Step 4 — Generate a JSON Key

1. In the service accounts list, click on `openclaw-agent`
2. Go to the **Keys** tab → **Add Key** → **Create new key**
3. Select **JSON** → **Create**
4. A `.json` file is downloaded to your computer

---

## Step 5 — Upload the JSON Key to the Server

**VPS:**
```bash
scp ~/Downloads/openclaw-integration-xxxxxx.json \
  root@YOUR_VPS_IP:/root/.openclaw/google-service-account.json
```

**Docker (local machine):**
```bash
docker cp ~/Downloads/openclaw-integration-xxxxxx.json \
  openclaw:/root/.openclaw/google-service-account.json
```

---

## Step 6 — Set the Environment Variable

**VPS — Linux:**
```bash
export GOOGLE_CHAT_SERVICE_ACCOUNT_FILE=/root/.openclaw/google-service-account.json
echo 'export GOOGLE_CHAT_SERVICE_ACCOUNT_FILE=/root/.openclaw/google-service-account.json' >> ~/.bashrc
source ~/.bashrc
```

**Windows PowerShell (local):**
```powershell
[Environment]::SetEnvironmentVariable(
  "GOOGLE_CHAT_SERVICE_ACCOUNT_FILE",
  "C:\Users\YOUR_USERNAME\.openclaw\google-service-account.json",
  "User"
)
```

**Docker — pass as environment variable:**
```bash
docker stop openclaw
docker run -d \
  --name openclaw \
  -p 18789:18789 \
  -v openclaw-data:/root/.openclaw \
  -e GOOGLE_CHAT_SERVICE_ACCOUNT_FILE=/root/.openclaw/google-service-account.json \
  openclaw/openclaw:latest
```

---

## Step 7 — Register Google Integration with OpenClaw

```bash
openclaw tools add google \
  --service-account $GOOGLE_CHAT_SERVICE_ACCOUNT_FILE
```

Expected output:
```
✓ Google integration added.
Services: Gmail, Google Calendar, Google Chat
```

---

## Step 8 — Share Your Google Resources with the Service Account

The service account needs access to your Gmail and Calendar.

### Gmail — Grant Access

1. In Gmail → **Settings** → **See all settings** → **Accounts and Import**
2. Under **Grant access to your account** → add the service account email (e.g. `openclaw-agent@openclaw-integration.iam.gserviceaccount.com`)

### Google Calendar — Share Calendar

1. Open Google Calendar → find your calendar → **Settings** (three dots) → **Settings and sharing**
2. Under **Share with specific people** → add the service account email
3. Set permission: **Make changes to events**

---

## Step 9 — Test Google Integration via Chat

In your Telegram or WhatsApp chat, send:

```
Check my Gmail for unread messages
```

Expected: Agent replies with a summary of unread emails.

```
What meetings do I have tomorrow?
```

Expected: Agent replies with your Google Calendar events for tomorrow.

---

## Verification

| Check | Expected |
|-------|----------|
| `openclaw tools list` | `google` shown as `enabled` |
| Chat: `Check my Gmail` | Email summary returned |
| Chat: `What meetings tomorrow?` | Calendar events returned |
| `ls ~/.openclaw/google-service-account.json` | File exists |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Permission denied` when accessing Gmail | Grant access to service account email in Gmail settings |
| `API not enabled` error | Enable the API in Google Cloud Console (Step 2) |
| JSON file not found error | Check `echo $GOOGLE_CHAT_SERVICE_ACCOUNT_FILE` prints the correct path |
| Docker: env var not set after restart | Add `-e` flag to `docker run` command |
| Service account has no calendar access | Share calendar with service account email (Step 8) |

---

## Reference

- Google Cloud Console: https://console.cloud.google.com
- OpenClaw Google integration: https://docs.openclaw.ai/tools/google
- Service accounts guide: https://cloud.google.com/iam/docs/service-accounts-create

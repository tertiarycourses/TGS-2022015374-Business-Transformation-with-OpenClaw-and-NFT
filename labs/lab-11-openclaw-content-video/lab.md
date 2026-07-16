# Lab 11 — Content & Video Production Team (OpenClaw Sub-Agents)

Install a custom skill that turns your agent into a coordinated content
production team: a Content Strategist, Scriptwriter, and Video Producer
hand a video idea off to each other in sequence — using OpenClaw's built-in
media generation tools and `sessions_spawn` sub-agent delegation — then pause
for your approval in chat before anything is "published."

**Lab environment:** Hostinger VPS (from Lab 1) **or** Docker Desktop (Windows 10/11, macOS 12+, Ubuntu 22.04+)
**Prerequisite:** Lab 3 completed (Telegram or WhatsApp channel connected and tested) + Lab 4 completed (tools working) + Lab 5 completed (skills install workflow understood)
**Estimated time:** 35 minutes

> **Docker Desktop users:** Prefix every `openclaw` command with `docker exec -it openclaw`.
> Example: `docker exec -it openclaw openclaw skills list`

---

## Overview

| Phase | Role | What it does |
|-------|------|---------------|
| 1 | Content Strategist | Researches trending angles (`web_search`), picks one topic |
| 2 | Scriptwriter | Writes hook + body + CTA sized to ~60 seconds |
| 3 | Video Producer | Storyboards scenes, generates thumbnail (`image_generate`), video clips (`video_generate`), voiceover (`tts`) |
| 4 | Human Approval Gate | Always pauses in chat and waits for your explicit reply — no auto-publish |
| 5 | Publisher | Writes final SEO title/description/tags, summarises the publish-ready package (dry run) |

This is delivered as a single **skill** (`video-content-team`) rather than
separate agents — the skill instructs your existing agent to delegate the
slow parts (research, asset generation) to background sub-agent runs via the
`sessions_spawn` tool, which OpenClaw already provides. You never write code
for this — the skill file is plain instructions the model reads.

---

## Step 0 — Confirm Your Channel Is Still Connected

This whole lab is driven by chatting with your agent in Telegram or WhatsApp,
so confirm that channel from Lab 3 is still running before you install
anything. This is the same on Docker Desktop and VPS — a container
restart between labs does not affect a channel that was already paired,
but it's worth 30 seconds to check.

```bash
# VPS
openclaw channels status

# Docker Desktop
docker exec -it openclaw openclaw channels status
```

Expected output:
```
CHANNEL     STATUS    ACCOUNT
telegram    running   @your_bot_username
```

**Pass:** Your channel (Telegram and/or WhatsApp) shows `running`.

**Fail — status does not show `running`, or the channel is missing
entirely:** Go back to Lab 3 and re-run Steps A2-A4 (Telegram) or B1-B2
(WhatsApp) — this lab does not re-cover channel setup or bot pairing.

Now send a plain test message to confirm the agent actually replies, not
just that the channel process is running:

Open Telegram, find the bot you created in Lab 3 (search for the
`@..._bot` username from `channels status` above — this is a message
inside the Telegram/WhatsApp app itself, not a terminal command, even on
Docker Desktop), and send:

```
Hello
```

**Pass:** Agent replies normally. If this doesn't work, fix it now —
every later step in this lab depends on this chat working.

**Fail:** No reply → run `docker restart openclaw` (Docker Desktop) or
`sudo systemctl restart openclaw` (VPS), wait 10 seconds, and retry. Still
nothing → revisit Lab 3's Troubleshooting table.

---

## Step 1 — Download the Skill File

You do not need to clone this course repo — download the skill file
directly with `curl`, the same way Lab 1 pulled files without cloning
anything.

```bash
# VPS
mkdir -p ~/.openclaw/skills/video-content-team
curl -o ~/.openclaw/skills/video-content-team/SKILL.md \
  https://raw.githubusercontent.com/tertiarycourses/TGS-2022015374-Business-Transformation-with-OpenClaw-and-NFT/video/labs/lab-11-openclaw-content-video/skills/video-content-team/SKILL.md

# Docker Desktop — download to your machine, then copy into the container:
curl -o SKILL.md \
  https://raw.githubusercontent.com/tertiarycourses/TGS-2022015374-Business-Transformation-with-OpenClaw-and-NFT/video/labs/lab-11-openclaw-content-video/skills/video-content-team/SKILL.md
MSYS_NO_PATHCONV=1 docker exec openclaw mkdir -p /home/node/.openclaw/skills/video-content-team
MSYS_NO_PATHCONV=1 docker cp SKILL.md openclaw:/home/node/.openclaw/skills/video-content-team/SKILL.md
```

> **Docker Desktop path:** the container runs as user `node`, not root —
> its OpenClaw home is `/home/node/.openclaw` (this is the same path Lab
> 1 mounts as a volume: `-v openclaw-data:/home/node/.openclaw`). Using
> `/root/...` here fails with `Permission denied`, since `/root` belongs
> to a user this container doesn't run as.

> **Windows Git Bash users:** the `MSYS_NO_PATHCONV=1` prefix is required
> on every `docker exec`/`docker cp` command below that contains a Linux
> path like `/home/node/...` — Git Bash silently rewrites those paths
> before Docker sees them otherwise (same issue Lab 1's Troubleshooting
> table covers for `docker run`). Without it, `docker cp` can report
> "Successfully copied" and still fail with `Could not find the file ...
> in container` on the next command, because the path it actually wrote
> to wasn't the one you typed. macOS/Linux users can ignore this prefix —
> it's a no-op there.

> This lab is currently on the `video` branch of the course repo. Once it's
> merged to `main`, change `video` to `main` in the URL above.

Expected: the `curl` command exits with no error and the file is non-empty.
Quick check:

```bash
# VPS
cat ~/.openclaw/skills/video-content-team/SKILL.md | head -3

# Docker Desktop
MSYS_NO_PATHCONV=1 docker exec openclaw cat /home/node/.openclaw/skills/video-content-team/SKILL.md | head -3
```

You should see the `---` YAML frontmatter and `name: video-content-team`
at the top.

---

## Step 2 — Install the Skill

```bash
# VPS
openclaw skills install ~/.openclaw/skills/video-content-team --as video-content-team

# Docker Desktop
MSYS_NO_PATHCONV=1 docker exec -it openclaw openclaw skills install /home/node/.openclaw/skills/video-content-team --as video-content-team
```

Expected output:
```
Installing video-content-team...
✓ Skill installed.
```

---

## Step 3 — Verify It's Ready

```bash
# VPS
openclaw skills check

# Docker Desktop
docker exec -it openclaw openclaw skills check
```

Confirm `video-content-team` shows `✓ ready`. If it shows `△ needs setup`,
check that the `video_generate`, `image_generate`, and `tts` tools are
available on your model/provider — not every provider supports media
generation (see Troubleshooting).

---

## Step 4 — Kick Off a Production Run

Go back to the same Telegram or WhatsApp chat you tested in Step 0 (this
is a message inside the app, not a terminal command — Docker Desktop
users do not prefix this with `docker exec`) and send:

```
Produce a 60-second video about "3 mistakes beginners make with Docker" for our YouTube Shorts channel
```

**Pass:** Agent researches the topic, proposes 3 ideas, picks one, and tells
you which one and why (Phase 1).

**Fail:** Agent just writes a script with no research/idea step first →
confirm the skill installed correctly (`openclaw skills list`), and that it
shows as `✓ ready`, not `△ needs setup`.

---

## Step 5 — Watch the Script and Storyboard Phases

The agent should continue automatically into Phase 2 (script) and Phase 3
(storyboard + generated thumbnail/video/voiceover) without you prompting
again. This can take a minute or two — media generation is slow.

**Pass:** You receive a script, a numbered storyboard, and at least a
thumbnail image back in the chat.

**Fail:** Agent stalls after the script → send `continue`. If it still
doesn't produce assets, `video_generate`/`image_generate` may not be
available for your current model — check Step 3's troubleshooting note.

---

## Step 6 — Confirm the Approval Gate Actually Blocks

This is the important part to verify — the agent must **not** publish
without your explicit reply.

**Pass:** Agent explicitly asks "Reply APPROVE to publish, or tell me what
to change" and then stops — no further action until you reply.

**Fail:** Agent proceeds to "publish" without asking → the skill did not
load correctly, or you're running an older cached version. Re-run
`openclaw skills update` and try Step 4 again in a new conversation.

Test the gate with a change request first:

```
Make the hook punchier and shorten the CTA
```

**Pass:** Agent revises and asks for approval again — it does not publish
on the first "no."

Then approve:

```
APPROVE
```

**Pass:** Agent runs Phase 5, gives you a final title/description/tags, and
states plainly that this is a dry run (no real upload happened).

---

## Verification

| Check | Expected |
|-------|----------|
| `openclaw channels status` | Telegram and/or WhatsApp shows `running` |
| Chat: `Hello` (Step 0) | Agent replies normally, before you install anything |
| `openclaw skills check` | `video-content-team` shows `✓ ready` |
| Chat: "Produce a 60-second video about..." | Agent researches, proposes 3 ideas, picks one |
| Script + storyboard phases | Script, numbered scenes, and a generated thumbnail appear in chat |
| Approval gate | Agent explicitly stops and asks for APPROVE before publishing |
| Change request before approving | Agent revises and asks again, does not publish |
| `APPROVE` | Agent produces final title/description/tags and states it's a dry run |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `channels status` shows nothing running, or you have no bot to message | You skipped or lost Lab 3's setup — this lab does not re-cover BotFather/QR pairing, go complete Lab 3 first |
| `Permission denied` on `/root/...` (Docker Desktop) | The container runs as user `node`, not root — use `/home/node/.openclaw/...`, not `/root/.openclaw/...` (see Step 1) |
| Skill shows `△ needs setup` | Your current model/provider doesn't expose `video_generate`/`image_generate`/`tts` — check `openclaw skills check` for the specific missing requirement, or switch models with `openclaw models set` |
| Agent skips straight to a script with no research | Skill not loaded — run `openclaw skills list` and confirm `video-content-team` appears; re-run Step 2 if missing |
| Agent publishes without asking | Skill file wasn't copied correctly, or an older version is cached — re-copy the file and run `openclaw skills update` |
| Media generation takes a long time / times out | Normal for `video_generate` — it can take 1-2 minutes. If it fails outright, your provider may not support it; the skill will still complete Phases 1-2 without it |
| "Something went wrong" from the agent | Model provider issue, not this skill — check `openclaw logs --limit 20` |

---

## Extending This Lab

- **Real sub-agent workspaces:** instead of relying on `sessions_spawn`
  alone, define a dedicated agent for video production with its own
  workspace via `openclaw agents add` and bind it to a separate Telegram
  bot or WhatsApp number — see `/concepts/multi-agent` in the docs.
- **Real publishing:** install or write a plugin that calls the YouTube
  Data API and wire it in as a tool the Phase 5 instructions can call,
  instead of the current dry-run summary.
- **Batch mode:** ask the agent to "produce 3 videos for next week" and
  watch it repeat the whole pipeline per topic.

---

## Reference

- Skills docs: https://docs.openclaw.ai/skills
- Tools (media generation, sessions/agents): https://docs.openclaw.ai/tools
- Multi-agent routing & delegation: https://docs.openclaw.ai/concepts/multi-agent
- ClawHub marketplace: https://clawhub.ai

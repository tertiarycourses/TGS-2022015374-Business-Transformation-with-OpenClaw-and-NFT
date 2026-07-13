# Lab 11 — Content & Video Production Team (OpenClaw Sub-Agents)

Install a custom skill that turns your agent into a coordinated content
production team: a Content Strategist, Scriptwriter, and Video Producer
hand a video idea off to each other in sequence — using OpenClaw's built-in
media generation tools and `sessions_spawn` sub-agent delegation — then pause
for your approval in chat before anything is "published."

**Lab environment:** Hostinger VPS (from Lab 1) **or** Docker Desktop (Windows 10/11, macOS 12+, Ubuntu 22.04+)
**Prerequisite:** Lab 4 completed (tools working) + Lab 5 completed (skills install workflow understood)
**Estimated time:** 30 minutes

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

## Step 1 — Copy the Skill Into Your Workspace

The skill file lives in this lab's folder: `skills/video-content-team/SKILL.md`.

```bash
# VPS — clone this course repo if you haven't already, then:
mkdir -p ~/.openclaw/skills
cp -r labs/lab-11-openclaw-content-video/skills/video-content-team ~/.openclaw/skills/

# Docker Desktop — copy into the running container:
docker cp labs/lab-11-openclaw-content-video/skills/video-content-team openclaw:/root/.openclaw/skills/video-content-team
```

---

## Step 2 — Install the Skill

```bash
# VPS
openclaw skills install ~/.openclaw/skills/video-content-team --as video-content-team

# Docker Desktop
docker exec -it openclaw openclaw skills install /root/.openclaw/skills/video-content-team --as video-content-team
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

In your Telegram or WhatsApp chat with the agent, send:

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

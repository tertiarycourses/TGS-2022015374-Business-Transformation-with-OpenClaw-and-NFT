# Lab 11 — Content & Video Production Team (OpenClaw Sub-Agents)

Install a custom skill and four dedicated sub-agents that turn your setup
into a real coordinated content production team: a Coordinator agent
delegates each phase — Content Strategist, Scriptwriter, Video Producer,
Publisher — to its own named sub-agent via OpenClaw's `sessions_spawn` tool,
each running in its own workspace with single-purpose instructions, then
pauses for your approval in chat before anything is "published."

**Lab environment:** Hostinger VPS (from Lab 1) **or** Docker Desktop (Windows 10/11, macOS 12+, Ubuntu 22.04+)
**Prerequisite:** Lab 3 completed (Telegram or WhatsApp channel connected and tested) + Lab 4 completed (tools working) + Lab 5 completed (skills install workflow understood)
**Estimated time:** 45 minutes

> **Docker Desktop users:** Prefix every `openclaw` command with `docker exec -it openclaw`.
> Example: `docker exec -it openclaw openclaw skills list`

> **macOS users (zsh):** Terminal.app's default shell, zsh, does not treat
> `#` as a comment when you paste it interactively — pasting a whole code
> block from this lab (including lines like `# Docker Desktop`) fails with
> `zsh: command not found: #`. Either run `setopt interactivecomments`
> once at the start of your session, or copy only the actual commands and
> skip the `#` lines by hand. This does not affect `bash`/Git Bash.

---

## Overview

| Phase | Agent | What it does |
|-------|------|---------------|
| 1 | `strategist` | Researches trending angles (`web_search`), picks one topic |
| 2 | `scriptwriter` | Writes hook + body + CTA sized to ~60 seconds |
| 3 | `producer` | Storyboards scenes, generates thumbnail (`image_generate`), video clips (`video_generate`), voiceover (`tts`) |
| 4 | Coordinator (your default agent) | Human Approval Gate — always pauses in chat and waits for your explicit reply, no auto-publish |
| 5 | `publisher` | Writes final SEO title/description/tags, summarises the publish-ready package (dry run) |

This is delivered as a **skill** (`video-content-team`, installed on your
existing default agent) plus **four dedicated sub-agents**, each with its
own workspace and single-purpose `AGENTS.md`. Your existing agent becomes
the Coordinator: the skill instructs it to delegate each phase to the
matching named sub-agent with the `sessions_spawn` tool — a real
multi-agent pipeline, not one agent role-playing four jobs. You never
write code for this — every agent's behaviour comes from plain-language
instruction files the model reads.

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

## Step 2b — Set Up the Sub-Agent Team

So far your one agent does every phase itself. Now give it four dedicated
teammates — `strategist`, `scriptwriter`, `producer`, `publisher` — each
with its own workspace and its own single-purpose instructions. Your main
agent becomes the **Coordinator**: it delegates each phase to the matching
teammate with the `sessions_spawn` tool instead of doing the work itself.

**Download each teammate's instructions:**

```bash
# VPS
for a in strategist scriptwriter producer publisher; do
  mkdir -p ~/.openclaw/workspace-$a
  curl -o ~/.openclaw/workspace-$a/AGENTS.md \
    https://raw.githubusercontent.com/tertiarycourses/TGS-2022015374-Business-Transformation-with-OpenClaw-and-NFT/video/labs/lab-11-openclaw-content-video/agents/$a/AGENTS.md
done

# Docker Desktop
for a in strategist scriptwriter producer publisher; do
  curl -o AGENTS-$a.md \
    https://raw.githubusercontent.com/tertiarycourses/TGS-2022015374-Business-Transformation-with-OpenClaw-and-NFT/video/labs/lab-11-openclaw-content-video/agents/$a/AGENTS.md
  MSYS_NO_PATHCONV=1 docker exec openclaw mkdir -p /home/node/.openclaw/workspace-$a
  MSYS_NO_PATHCONV=1 docker cp AGENTS-$a.md openclaw:/home/node/.openclaw/workspace-$a/AGENTS.md
done
```

**Register the four agents (plus your existing default agent) and allow
the coordinator to spawn them.** This edits `openclaw.json`, so do it with
a small script rather than typing JSON by hand — the same pattern used
elsewhere in this course when a config needs more than a one-line change.

> **Why the script explicitly re-adds a `main` agent:** if you have never
> touched `agents.list` before, OpenClaw runs one *implicit* default agent
> with id `main` and workspace `~/.openclaw/workspace` — it doesn't appear
> in the config file at all. The moment `agents.list` gets *any* explicit
> entries (like our four teammates), that implicit default goes away, and
> your existing channel binding (which points at agent id `main`) breaks
> with `Unknown agent id "main" (not in agents.list)`. The script below
> adds `main` back explicitly, with its default path, so your existing
> Telegram/WhatsApp connection keeps working.

> **Why plain `JSON`, not `json5`:** `openclaw.json` is written by the CLI
> as plain valid JSON (no comments), and the `json5` npm package generally
> is not installed anywhere Node can resolve it from a one-off script path
> like `/tmp` — requiring it will fail with `Cannot find module 'json5'`.
> Node's built-in `JSON.parse`/`JSON.stringify` handles this file fine.

```bash
cat > patch-agents.js << 'EOF'
const fs = require('fs');
const p = process.env.OPENCLAW_CONFIG || '/home/node/.openclaw/openclaw.json';
const cfg = JSON.parse(fs.readFileSync(p, 'utf8'));

cfg.agents = cfg.agents || {};
cfg.agents.list = cfg.agents.list || [];

// Preserve the implicit default agent explicitly, or the existing
// channel binding (agentId: "main") breaks once agents.list is populated.
if (!cfg.agents.list.find(a => a.id === 'main')) {
  cfg.agents.list.unshift({ id: 'main', name: 'Main', workspace: '~/.openclaw/workspace' });
}

const team = ['strategist', 'scriptwriter', 'producer', 'publisher'];
for (const id of team) {
  if (!cfg.agents.list.find(a => a.id === id)) {
    cfg.agents.list.push({
      id,
      name: id[0].toUpperCase() + id.slice(1),
      workspace: `/home/node/.openclaw/workspace-${id}`,
    });
  }
}

cfg.agents.defaults = cfg.agents.defaults || {};
cfg.agents.defaults.subagents = cfg.agents.defaults.subagents || {};
const allow = new Set(cfg.agents.defaults.subagents.allowAgents || []);
team.forEach(id => allow.add(id));
cfg.agents.defaults.subagents.allowAgents = Array.from(allow);

fs.writeFileSync(p, JSON.stringify(cfg, null, 2));
console.log('agents.list + subagents.allowAgents patched:', ['main', ...team]);
EOF
```

```bash
# VPS
OPENCLAW_CONFIG=~/.openclaw/openclaw.json node patch-agents.js

# Docker Desktop (all OSes — the MSYS_NO_PATHCONV prefix is a no-op on
# macOS/Linux, only Windows Git Bash needs it, see Step 1)
MSYS_NO_PATHCONV=1 docker cp patch-agents.js openclaw:/tmp/patch-agents.js
MSYS_NO_PATHCONV=1 docker exec openclaw node /tmp/patch-agents.js
```

> **Why a script and not `openclaw configure`:** `openclaw configure` is
> built for single-section interactive edits. Adding five agents plus an
> allowlist entry is a structural change to `agents.list`, so a small node
> script that reads, edits, and rewrites the JSON file directly is more
> reliable — the same reasoning as Step 1's `MSYS_NO_PATHCONV` note: know
> exactly what a command touches before running it against a live config.

Restart so the new agents are picked up:

```bash
# VPS
sudo systemctl restart openclaw

# Docker Desktop
docker restart openclaw
```

Verify all five exist:

```bash
# VPS
openclaw agents list

# Docker Desktop
docker exec -it openclaw openclaw agents list
```

Expected: `main`, `strategist`, `scriptwriter`, `producer`, `publisher`
all appear.

**If the container won't come back up** (Docker Desktop only — VPS's
`systemctl restart` doesn't have this failure mode): a config error on
startup can crash the whole container, since `openclaw` is its entrypoint
process. `docker exec` needs a *running* container, so you can't fix the
file that way. `docker cp` still works on a stopped container — pull the
file out, fix it, and push it back:

```bash
MSYS_NO_PATHCONV=1 docker cp openclaw:/home/node/.openclaw/openclaw.json ./openclaw.json
# Edit ./openclaw.json with any text/JSON editor to fix the reported
# problem (`docker logs openclaw` shows the exact validation error)
MSYS_NO_PATHCONV=1 docker cp ./openclaw.json openclaw:/home/node/.openclaw/openclaw.json
docker start openclaw
docker exec -it openclaw openclaw config validate
```

This shouldn't happen if you used the script above as-is (it preserves
`main`), but it's the general recovery move for any bad hand-edit to a
running gateway's config.

**Update the skill to the sub-agent-orchestrating version.** Re-download
`SKILL.md` (Step 1) — it was rewritten to delegate via `sessions_spawn`
instead of doing all phases inline — and reinstall:

```bash
# VPS
curl -o ~/.openclaw/skills/video-content-team/SKILL.md \
  https://raw.githubusercontent.com/tertiarycourses/TGS-2022015374-Business-Transformation-with-OpenClaw-and-NFT/video/labs/lab-11-openclaw-content-video/skills/video-content-team/SKILL.md
openclaw skills update

# Docker Desktop
curl -o SKILL.md \
  https://raw.githubusercontent.com/tertiarycourses/TGS-2022015374-Business-Transformation-with-OpenClaw-and-NFT/video/labs/lab-11-openclaw-content-video/skills/video-content-team/SKILL.md
MSYS_NO_PATHCONV=1 docker cp SKILL.md openclaw:/home/node/.openclaw/skills/video-content-team/SKILL.md
docker exec -it openclaw openclaw skills update
```

**Pass:** `openclaw agents list` shows `main` plus all four teammates, and
`openclaw skills check` still shows `video-content-team` as `✓ ready`.

**Fail — `sessions_spawn` target not allowed / permission error when the
coordinator tries to delegate:** confirm `agents.defaults.subagents.allowAgents`
actually contains all four ids — re-run `patch-agents.js`, it's safe to run
more than once (it skips ids that already exist).

**Fail — `Unknown agent id "main" (not in agents.list)` after restart:**
you're running an older copy of `patch-agents.js` that doesn't re-add
`main` — re-download this step's script (it now unshifts a `main` entry
before adding the team) and use the container-stopped recovery steps
above to fix the file, then re-run it.

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

**Pass:** The Coordinator spawns `strategist`, which researches the topic,
proposes 3 ideas, picks one — and the Coordinator relays which one and why
back into this chat (Phase 1).

**Fail:** Agent just writes a script with no research/idea step first →
confirm the skill installed correctly (`openclaw skills list`, `✓ ready`
not `△ needs setup`) and that `openclaw agents list` shows `strategist`
(Step 2b) — if the sub-agent doesn't exist yet, the Coordinator has
nothing to spawn and may fall back to doing the work itself.

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
| `zsh: command not found: #` (macOS) | zsh doesn't treat `#` as a comment interactively by default — run `setopt interactivecomments` once, or paste only the real commands (see the macOS callout above) |
| `curl: (6) Could not resolve host: raw.githubusercontent.com`, or browser loads the file but `curl` still can't | DNS/proxy issue on your machine, not this lab — test with `ping -c 1 raw.githubusercontent.com`; if it fails, try `networksetup -setdnsservers Wi-Fi 8.8.8.8 1.1.1.1` (macOS) or switch networks. If the file loads fine in a browser but `curl` still fails, a system proxy (common on corporate/campus networks) is likely configured for browsers only — skip `curl` entirely and use the [macOS Offline Fallback](#macos-offline-fallback-cant-curl-from-terminal) appendix below |
| `channels status` shows nothing running, or you have no bot to message | You skipped or lost Lab 3's setup — this lab does not re-cover BotFather/QR pairing, go complete Lab 3 first |
| `Permission denied` on `/root/...` (Docker Desktop) | The container runs as user `node`, not root — use `/home/node/.openclaw/...`, not `/root/.openclaw/...` (see Step 1) |
| Skill shows `△ needs setup` | Your current model/provider doesn't expose `video_generate`/`image_generate`/`tts` — check `openclaw skills check` for the specific missing requirement, or switch models with `openclaw models set` |
| Agent skips straight to a script with no research | Skill not loaded — run `openclaw skills list` and confirm `video-content-team` appears; re-run Step 2 if missing |
| Coordinator does everything itself, never mentions `strategist`/`scriptwriter`/`producer`/`publisher` | Sub-agents weren't registered — re-run Step 2b's `patch-agents.js`, restart, then confirm `openclaw agents list` shows all four before retrying |
| `sessions_spawn` error / delegation silently fails | `agents.defaults.subagents.allowAgents` doesn't include the target id — re-run `patch-agents.js` (Step 2b), it's safe to run more than once |
| Container won't start / `Unknown agent id "main" (not in agents.list)` | `agents.list` was populated without re-adding the implicit default agent — see Step 2b's container-stopped recovery steps (`docker cp` out, fix, `docker cp` back in) |
| Agent publishes without asking | Skill file wasn't copied correctly, or an older version is cached — re-copy the file and run `openclaw skills update` |
| Media generation takes a long time / times out | Normal for `video_generate` — it can take 1-2 minutes. If it fails outright, your provider may not support it; `producer` will still return the storyboard, thumbnail, and voiceover it did produce |
| "Something went wrong" from the agent | Model provider issue, not this skill — check `openclaw logs --limit 20` |

---

## Extending This Lab

- **Give a sub-agent its own channel:** bind `producer` to a separate
  Telegram bot or WhatsApp number (`bindings` config) so heavy media
  generation runs on a channel of its own instead of sharing the
  Coordinator's — see `/concepts/multi-agent` in the docs.
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

---

## macOS Offline Fallback (can't `curl` from Terminal)

Some corporate/campus networks route browser traffic through a proxy that
`curl` doesn't know about, so a page loads fine in Safari/Chrome but every
`curl` in this lab fails with `Could not resolve host`. If that's you,
skip `curl` entirely — paste the file contents directly into a local file
with `cat`, then continue with the normal `docker` commands (no
`MSYS_NO_PATHCONV` needed on macOS — that prefix is Windows Git Bash only).

**Step 1's `SKILL.md`:**

```bash
cat > SKILL.md << 'EOF'
---
name: video-content-team
description: Coordinates a short-form video production pipeline across four dedicated sub-agents (strategist, scriptwriter, producer, publisher) via sessions_spawn, with a human approval gate in this chat before publishing.
metadata:
  openclaw:
    requires:
      anyBins: []
---

You are the **Coordinator** for a short-form video production team made of
four dedicated sub-agents, each running in its own workspace: `strategist`,
`scriptwriter`, `producer`, and `publisher` (see Lab 11's `agents/` setup
for what each one is instructed to do). You never do their work yourself —
you delegate each phase to the matching agent with the `sessions_spawn`
tool (set its target to that agent's id) and relay every result back into
this chat, mirroring how a real production team hands off work between
specialists.

## Phase 1 — Strategist

When the user asks to plan/produce a video (e.g. "produce a video about X
for our channel"), spawn a session on `strategist` with the user's full
request as the task. Wait for its result, then post the 3 proposed ideas
and the chosen one (with reasoning) back into this chat before continuing.

## Phase 2 — Scriptwriter

Spawn a session on `scriptwriter`, passing the chosen idea from Phase 1 as
the task. Post the finished script back into this chat.

## Phase 3 — Producer

Spawn a session on `producer`, passing the finished script as the task.
Post the storyboard, thumbnail, and any generated media links back into
this chat.

## Phase 4 — Human Approval Gate (always required — no exceptions)

After Phase 3 completes:

1. Summarise everything so far (idea, script, storyboard, assets) in this
   chat.
2. Explicitly ask: "Reply APPROVE to publish, or tell me what to change."
3. **Stop and wait for a reply in the chat.** Do not spawn `publisher`
   until the user has explicitly approved. If they ask for changes, work
   out which phase needs rework, re-spawn that specific agent with the
   requested change, and ask again — do not assume silence means approval.

## Phase 5 — Publisher (only after explicit approval)

Spawn a session on `publisher`, passing the full approved package (idea,
script, storyboard, asset references) as the task. Post its final
title/description/tags/summary back into this chat, including its
statement that this is a dry run.

## Rules

- Always relay each sub-agent's full result into this chat before moving
  to the next phase — the user should see the whole trail, not just a
  final answer.
- Never spawn `publisher` without an explicit APPROVE from the user in
  this chat. If the user says "just publish it" before Phase 4 has run,
  show them the assets first and ask again.
- If a sub-agent's spawn fails or times out (e.g. `producer`'s video
  generation), report that plainly and continue with whatever it did
  produce — don't silently retry more than once.
EOF

docker exec openclaw mkdir -p /home/node/.openclaw/skills/video-content-team
docker cp SKILL.md openclaw:/home/node/.openclaw/skills/video-content-team/SKILL.md
docker exec -it openclaw openclaw skills install /home/node/.openclaw/skills/video-content-team --as video-content-team
```

**Step 2b's four `AGENTS.md` files:**

```bash
mkdir -p agents/strategist agents/scriptwriter agents/producer agents/publisher

cat > agents/strategist/AGENTS.md << 'EOF'
# Content Strategist Agent

Your only job: given a video topic request, use `web_search` to check
current trending angles/formats for the topic and platform. If search comes
back thin, fall back to proven short-form formats: myth vs reality,
before/after, "3 mistakes beginners make", POV/day-in-the-life, fast
tutorial.

Propose 3 concrete ideas, each with: title, angle, hook (first 3 seconds),
target audience. Pick ONE and state clearly which was chosen and why.

Return only your idea proposals and final choice. Do not write scripts,
storyboards, or generate any media — that is the next agent's job, not
yours.
EOF

cat > agents/scriptwriter/AGENTS.md << 'EOF'
# Scriptwriter Agent

Your only job: given a chosen video topic/idea, write hook (must earn the
next 3 seconds), body, and a clear call-to-action. Target ~60 seconds
spoken (~150 words/minute — keep the script to roughly 130-160 words
unless told a different target duration).

Read the script back to yourself and cut anything that doesn't sound
natural spoken aloud.

Return only the finished script. Do not do research or generate media —
that is not your job.
EOF

cat > agents/producer/AGENTS.md << 'EOF'
# Video Producer Agent

Your only job: given a finished script, break it into numbered scenes
(2-4 seconds each): visual description + voiceover line per scene.

Then call `image_generate` to produce a thumbnail concept (bold,
high-contrast, large readable text overlay, 3 words max, matches the
video's hook), call `video_generate` for any scene needing a full
generated clip, and call `tts` to produce the voiceover audio track from
the final script.

If `video_generate` fails or times out, say so plainly, try once more at a
reduced spec, and if it still fails, continue and return the storyboard,
thumbnail, and voiceover you do have — do not retry more than twice total.

Return the storyboard plus references to whatever assets you produced. Do
not write the script or handle publishing — that is not your job.
EOF

cat > agents/publisher/AGENTS.md << 'EOF'
# Publisher Agent

Your only job: given an approved script/storyboard package, write an
SEO-optimized final title (can differ from the working title), a
description with a clear CTA and 3-5 relevant hashtags/tags, and
summarize the final publish-ready package (title, description, tags,
thumbnail, video asset, audio asset).

This is always a dry run — do not actually upload anywhere unless a
publishing tool/plugin has been explicitly configured for this workspace.
Say so plainly if you're stopping short of a real upload.

Only do this work if the coordinator tells you the user has explicitly
approved the package. If that isn't stated in your task, ask the
coordinator to confirm approval before proceeding.
EOF

for a in strategist scriptwriter producer publisher; do
  docker exec openclaw mkdir -p /home/node/.openclaw/workspace-$a
  docker cp agents/$a/AGENTS.md openclaw:/home/node/.openclaw/workspace-$a/AGENTS.md
done
```

`patch-agents.js` (Step 2b) never used `curl` in the first place, so no
change needed there — create it and run it exactly as written earlier in
this lab.

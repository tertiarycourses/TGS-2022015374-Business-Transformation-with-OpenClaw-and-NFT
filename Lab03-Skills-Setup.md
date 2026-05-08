# Lab 3 — Skills Setup (incl. Self-Improvement from skills.sh)

## Objective
Understand what OpenClaw **skills** are, install skills from the
[skills.sh](https://skills.sh/) registry — including the **self-improvement**
skill — and invoke them from chat.

## Prerequisites
- Lab 1 completed
- A working channel (Telegram or WhatsApp) for testing

## Estimated Time
~30 minutes

---

## Concept Recap

A **skill** is a reusable, named capability your agent can call: a prompt +
optional tools + optional examples. Think of skills as "shortcuts" the agent
can trigger by name. Examples: `web-research`, `code-review`,
`self-improvement`, `linkedin-post`.

---

## Step 1 — List Currently Installed Skills

```bash
openclaw skills list
```

![](screenshots/lab3-01-skills-list.png)

---

## Step 2 — Install the Self-Improvement Skill

The **self-improvement** skill lets the agent reflect on past conversations
and update its own memory / behavior preferences.

```bash
openclaw skills add self-improvement --source skills.sh
```

Verify:
```bash
openclaw skills show self-improvement
```

---

## Step 3 — Install Two More Useful Skills

```bash
openclaw skills add web-research --source skills.sh
openclaw skills add code-review  --source skills.sh
```

![](screenshots/lab3-02-skills-installed.png)

---

## Step 4 — Invoke a Skill in Chat

In Telegram (or any channel), send:

```
/skill self-improvement
```

The agent should respond by reflecting on what's worked, what hasn't, and
proposing a memory update. Approve or reject the proposal.

Try the others:
```
/skill web-research "What are the top 3 use cases for OpenClaw?"
/skill code-review path/to/file.py
```

---

## Step 5 — Browse the Registry

Open <https://skills.sh/> in your browser. Pick **one** skill that interests
you (LinkedIn post, Stripe best-practices, Remotion video, etc.) and install
it:

```bash
openclaw skills add <skill-name> --source skills.sh
```

Demo it to your classmate.

---

## Verification

- `openclaw skills list` shows `self-improvement`, `web-research`, `code-review`,
  plus your free-choice skill.
- `/skill self-improvement` runs end-to-end in chat.

---

## Troubleshooting

| Symptom | Fix |
|--------|-----|
| `skill 'foo' not found` | Run `openclaw skills update` to refresh the registry index. |
| Skill installs but `/skill` doesn't trigger | Restart gateway: `openclaw gateway restart`. |
| Self-improvement loops endlessly | Cap iterations: `openclaw skills config self-improvement --max-iterations 3`. |

---

## Exercise

1. Pick **two** skills from skills.sh you'd actually use at work. Install them.
2. Write a short note in `~/.openclaw/notes/skill-review.md` explaining what
   each skill does and one scenario where it would save you time.

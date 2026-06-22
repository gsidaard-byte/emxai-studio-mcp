# EMxAI Studio MCP

A hosted **Model Context Protocol (MCP)** server that delivers curated teaching prompts and the EM × AI Field Guide directly inside AI assistants. Built for engineering faculty to use in workshops and share with colleagues. Works with both **Claude** and **ChatGPT**.

---

## What is an MCP?

The Model Context Protocol is an open standard that lets an AI assistant (Claude, ChatGPT) connect to an external server and pull in extra capabilities. Instead of copying a long prompt into the chat every time, faculty connect this server once and the curated prompts become available on demand inside the assistant.

This server is **read-only and stateless**. It stores no user data, requires no login, and only ever returns text (prompts and reference content). It cannot modify files, send messages, or take any action on the user's behalf.

---

## Connection details

| | |
|---|---|
| **Endpoint URL** | `https://sids-eml-studio-mcp-production.up.railway.app/mcp` |
| **Health check** | `https://sids-eml-studio-mcp-production.up.railway.app/` (returns JSON status + capability list) |
| **Authentication** | None (public) |
| **Transport** | Streamable HTTP (stateless) |
| **Hosting** | Railway (auto-deploys from GitHub) |
| **Source** | `github.com/gsidaard-byte/emxai-studio-mcp` |

### Connect in Claude Desktop

Add to `claude_desktop_config.json`, then fully quit and reopen Claude:

```json
{
  "mcpServers": {
    "emxai-studio": {
      "type": "http",
      "url": "https://sids-eml-studio-mcp-production.up.railway.app/mcp"
    }
  }
}
```

Prompts then appear in the slash menu (type `/`), e.g. `/eml-architect`, `/em-list`.

### Connect in ChatGPT

Settings → **Connectors** → **Add MCP Server** → paste the endpoint URL → Authentication: **No Auth** → confirm. The capabilities appear as tools the assistant calls when asked, e.g. *"use the eml_architect tool…"*.

---

## How it is structured

Every capability is exposed in **two forms** so it works natively on both platforms:

- **As a prompt** — for Claude's slash menu. Names use hyphens (`eml-architect`).
- **As a tool** — for ChatGPT's connector. Names use underscores (`eml_architect`).

Both return identical content. There are **13 capabilities** in two groups.

### Group 1 — Teaching Prompts (8)

Standalone assistants for specific instructional-design tasks. Each one turns the AI into a specialist that guides the faculty member through a task.

| Prompt (Claude) | Tool (ChatGPT) | What it does | Parameters |
|---|---|---|---|
| `aias-advisor` | `aias_advisor` | AI Assessment Scale Advisor — redesigns homework across a 5-level AIAS framework (No AI → AI Exploration) with student-facing instructions, rubrics, and integrity safeguards | `subject`, `level` |
| `eml-architect` | `eml_architect` | EML Architect — converts a traditional textbook problem into an Entrepreneurial Mindset Learning task while preserving technical rigor. Includes all KEEN reference materials | `em_habits`, `problems` |
| `interactive-builder-planning` | `interactive_builder_planning` | Phase 1 — guides faculty through a planning blueprint for a privacy-safe, single-session educational web app | — |
| `interactive-builder-coding` | `interactive_builder_coding` | Phase 2 — turns that blueprint into a working single-file HTML prototype | — |
| `autonomy-coach` | `autonomy_coach` | Course Autonomy Coach — embeds student autonomy into a course using 20 proven strategies, with ready-to-use syllabus and rubric language | `course_subject`, `course_level` |
| `engagement-opener` | `engagement_opener` | Joyful Opener Designer — builds a 3-minute classroom micro-experiment that sparks curiosity through cognitive dissonance or surprise | `course_title`, `concept` |
| `passion-connector` | `passion_connector` | Passion Connector — designs a 5-minute classroom segment linking the instructor's personal passion to course content | `passion`, `course` |
| `prompt-optimizer` | `prompt_optimizer` | Prompt Optimizer — rewrites a rough prompt into a precise, production-ready prompt tuned for Claude, Gemini, or GPT | `target_model`, `raw_prompt`, `optional_context` |

All parameters are optional. Calling a capability with no parameters starts the assistant's normal intake flow; supplying parameters skips ahead.

### Group 2 — EM × AI Field Guide (5)

A structured library of the **18 KEEN Habits of Entrepreneurial Mindset for an age of AI**, plus **7 workflows** that compose them. These five capabilities are the access points into that library.

| Prompt (Claude) | Tool (ChatGPT) | What it returns | Parameters |
|---|---|---|---|
| `em-list` | `em_list` | The full map — 3 families, all 18 habits with their one-line tensions, and the 7 workflows. **Start here.** | — |
| `em-habit` | `em_habit` | Complete content for one habit (see field list below) | `name` |
| `em-coach` | `em_coach` | Just the *Run it yourself* paste-ready prompt for one habit | `habit` |
| `em-workflow` | `em_workflow` | A full multi-habit workflow (orchestration prompt + student blueprint + build-an-activity meta-prompt) | `name` |
| `em-diagnostic` | `em_diagnostic` | The routing diagnostic — assesses the user's AI practice across all 3 Cs and points them to the right habit or workflow | — |

Habit and workflow names are matched **case- and punctuation-insensitively** (`"systems thinking"`, `"Systems Thinking"`, and `"systems_thinking"` all resolve). An unrecognized name returns a friendly error listing the valid options.

---

## The EM × AI framework

The Field Guide is organized as **3 families (the KEEN 3Cs) → 18 habits → 7 workflows**.

### The 3 families and 18 habits

| Family | Habits |
|---|---|
| **Curiosity** — fuels exploration, challenges assumptions, reveals opportunities | Inquisitiveness · Contrarian Thinking · Opportunity Seeking · Experimentation · Confronting Ambiguity · Future-Minded |
| **Connections** — integrates perspectives, ideas, and systems to drive innovation | Creativity · Systems Thinking · Knowledge Synthesis · Implications Thinking · Strategic Thinking · Risk Awareness |
| **Creating Value** — delivers meaningful outcomes that benefit others at scale | Value Awareness · Customer-Centric Thinking · Impact Thinking · Socially Minded · Persistence · Resourcefulness |

### What each habit contains

Calling `em-habit` / `em_habit` returns all of the following for one habit:

- **Family** — which of the 3 Cs it belongs to
- **Definition** — the one-line KEEN definition
- **Frameworks** — the established engineering/design methods it teaches (e.g. Systems Thinking → the Iceberg Model, causal loop diagrams, stock-and-flow)
- **The AI-era move** — how the habit shifts when AI is in the loop
- **How AI helps build it** — concrete ways to use AI to practice the habit
- **The anti-pattern** — the failure mode to guard against
- **One-line tension** — the core trade-off in a single sentence
- **Run it yourself** — a paste-ready prompt plus its framing (*what it does*, *when to use it*, *what good output looks like*)
- **Run it with students** — a teaching blueprint (*Setup*, *AI's role*, *Assessed on*)

### The 7 workflows

Workflows chain several habits into a guided, multi-step session. Each runs as an orchestration prompt that **pauses and waits after every step**.

| Workflow | Composes | Use it when |
|---|---|---|
| **EM × AI Diagnostic** | All 18 habits | You don't yet know which habit or workflow you need |
| **Reality Check** | Inquisitiveness, Customer-Centric Thinking | You're about to trust a claim or design and need to get to primary sources and real stakeholders |
| **Assumption Buster** | Contrarian Thinking, Implications Thinking, Risk Awareness | You have a real decision to pressure-test before committing |
| **Experiment Multiplier** | Experimentation, Creativity | Cheap generation tempts you to ship the first idea |
| **Expertise to Files** | Knowledge Synthesis, Resourcefulness | You keep making the same judgment and want it reusable |
| **System Builder** | Systems Thinking, Strategic Thinking, Persistence | A task you keep redoing should become a system |
| **Value-Chain Climber** | Value Awareness, Opportunity Seeking, Impact Thinking | You want to move work from output up to outcomes |

### What each workflow contains

Calling `em-workflow` / `em_workflow` returns:

- **Composes habits** — which habits the workflow exercises
- **When to reach for this** — the situation it fits
- **Run it yourself — orchestration prompt** — a full system prompt with a pause-after-each-step contract
- **Run it with students** — the teaching blueprint (*Setup*, *AI's role*, *Assessed on*)
- **Prompt to build this activity** — a faculty meta-prompt that has AI generate the assignment brief, student instructions, and rubric

---

## The two delivery modes

Every habit and workflow supports two ways of working, which is the core design of the Field Guide:

- **Run it yourself** — a prompt the faculty member runs on their own task, to practice the habit themselves.
- **Run it with students** — a strategy the faculty member designs and leads in class, expressed as a *Setup / AI's role / Assessed on* blueprint (not a prompt to paste).

This mirrors the guide's principle that faculty should both **practice** these habits and **teach** them.

---

## The master principle

Every habit and workflow returned by the server carries this principle:

> You can't evaluate work in a domain you haven't mastered, so polished output reads as competent when it isn't. AI amplifies the judgment you bring. It cannot supply the judgment you lack. Develop expertise first, then let AI scale it. Never the reverse.

---

## Technical architecture (for reference)

- **Language:** TypeScript, built with the official `@modelcontextprotocol/sdk`.
- **Transport:** Streamable HTTP in **stateless** mode — each request gets a fresh server instance, no session tracking. This is what makes the same endpoint work for both Claude and ChatGPT.
- **Content source of truth:** all prompt and Field Guide text lives in `src/content/`. The EM × AI content (`em-field-guide.ts`) is generated verbatim from a canonical handoff document (`context.md`) so the server, the HTML guide, and the source stay in sync.
- **Tool annotations:** every tool is marked read-only, non-destructive, closed-world, and idempotent — required for the ChatGPT connector.
- **CORS:** open (`*`), since the service is public and unauthenticated.
- **Deployment:** pushing to the `main` branch on GitHub triggers an automatic Railway rebuild and redeploy. The endpoint URL never changes, so faculty never need to reconfigure.

### Capability summary

```
13 capabilities  =  8 teaching prompts  +  5 EM Field Guide access points
Each exposed as both a prompt (Claude) and a tool (ChatGPT)
Behind the Field Guide: 3 families · 18 habits · 7 workflows
```

---

## Typical usage flows

**A faculty member new to the framework**
1. Call `em-diagnostic` / `em_diagnostic` — answer its questions about what they teach and how they use AI.
2. It names their weak habits and routes them to a specific habit coach or workflow.

**A faculty member who knows what they want**
1. Call `em-list` to browse, or go straight to `em-habit` with a name like *"Risk Awareness"*.
2. Use `em-coach` to grab just the paste-ready prompt, or `em-workflow` for a full guided session.

**Designing a class activity**
1. Call `em-workflow` for the relevant workflow.
2. Use the included *Prompt to build this activity* to have AI draft the brief, instructions, and rubric for their specific course.

**Redesigning an assignment for AI**
1. Call `aias-advisor` / `aias_advisor` with the subject and level.
2. Paste the original homework problem; receive a 5-level redesign with rubrics and safeguards.

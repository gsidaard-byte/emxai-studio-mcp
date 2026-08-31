# EMxAI Studio MCP

A hosted MCP (Model Context Protocol) server that exposes curated teaching prompts for workshops and faculty use. Works with both **Claude** and **ChatGPT**.

Every capability is exposed both as a **prompt** (Claude slash-menu, e.g. `/eml-architect`) and as a **tool** (ChatGPT connector, e.g. `eml_architect`). Tool names use underscores; prompt names use hyphens.

## Teaching Prompts

| Prompt | Description | Parameters |
|---|---|---|
| `aias-advisor` | AI Assessment Scale Advisor — redesigns homework using a 5-level AIAS framework | `subject`, `level` |
| `eml-architect` | EML Architect — converts textbook problems into Entrepreneurial Mindset Learning tasks (includes all reference materials) | `em_habits`, `problems` |
| `interactive-builder-planning` | Phase 1 — designs a privacy-safe educational web-app blueprint | — |
| `interactive-builder-coding` | Phase 2 — builds a working single-file HTML prototype from the blueprint | — |
| `autonomy-coach` | Course Autonomy Coach — embeds student autonomy using 20 proven strategies | `course_subject`, `course_level` |
| `engagement-opener` | Joyful Opener Designer — creates a 3-minute curiosity-sparking classroom micro-experiment | `course_title`, `concept` |
| `passion-connector` | Passion Connector — links personal passion to course content in 5 minutes | `passion`, `course` |
| `prompt-optimizer` | Prompt Optimizer — rewrites rough prompts for Claude, Gemini, or GPT | `target_model`, `raw_prompt` |

## EM × AI Field Guide

The 18 KEEN Habits of Entrepreneurial Mindset for an age of AI, organized as 3 families → 18 habits → 7 workflows. Content is canonical from `context.md`.

| Prompt | Description | Parameters |
|---|---|---|
| `em-list` | The full map — 3 families, 18 habits with their tensions, 7 workflows. Start here. | — |
| `em-habit` | Full content for one habit (frameworks, AI-era move, anti-pattern, both delivery modes) | `name` |
| `em-coach` | Just the Run-it-yourself paste-ready prompt for a habit | `habit` |
| `em-workflow` | A multi-habit workflow with orchestration prompt + student blueprint + build-activity meta-prompt | `name` |
| `em-diagnostic` | The EM × AI Diagnostic — assesses your AI practice and routes you to the right tool | — |

**18 habits** — Curiosity: Inquisitiveness, Contrarian Thinking, Opportunity Seeking, Experimentation, Confronting Ambiguity, Future-Minded · Connections: Creativity, Systems Thinking, Knowledge Synthesis, Implications Thinking, Strategic Thinking, Risk Awareness · Creating Value: Value Awareness, Customer-Centric Thinking, Impact Thinking, Socially Minded, Persistence, Resourcefulness

**7 workflows** — EM × AI Diagnostic, Reality Check, Assumption Buster, Experiment Multiplier, Expertise to Files, System Builder, Value-Chain Climber

## EM Assessment Toolkit

Source-grounded, course-embedded assessment of the 18 Habits of EM and eight observable EM behaviors. Assesses demonstrated performance in artifacts, never personality; `NE` (not elicited) is always distinct from a score of `0`. Data and scoring logic live in `em_assessment_data.py` / `em_assessment_logic.py` (ported verbatim from the EM Assessment Toolkit).

| Tool | Purpose | Key parameters |
|---|---|---|
| `em_list_habits` | Discover/filter the 18 habits with category and search filters | `category`, `search` |
| `em_get_habit` | One habit's assessment definition: core theme, evidence look-fors, exclusions, related behaviors | `habit` |
| `em_get_behavior_rubric` | The four developmental anchors (0–3) for one observable behavior | `behavior` |
| `em_plan_assessment` | Aligned elicitation and evidence plan for one assignment (1–3 target habits, AI-use policy, stakes) | `assignment_name`, `artifact_type`, `target_habits`, `ai_use`, `stakes` |
| `em_score_evidence_episode` | Deterministic NE/0–3 scoring of one evidence episode from encoded judgments | `target_habit` + 8 boolean judgments |
| `em_synthesize_profile` | Guarded course-level screening statuses from multiple rated episodes | `episodes` |

Also exposes `em://habits`, `em://observable-behaviors`, and `em://scoring-scale` resources, and a `review-em-evidence` prompt.

**Server totals: 19 tools · 14 prompts · 3 resources.**

---

## Deployment (FastMCP Cloud — Recommended)

The production server is [`server.py`](server.py), a Python [FastMCP](https://pypi.org/project/fastmcp/) app. It loads its content from `content.json`.

1. Go to [fastmcp.cloud](https://fastmcp.cloud) and sign in with GitHub.
2. Create a project from the `emxai-studio-mcp` repo.
3. Set the entrypoint to `server.py` (the server object is `mcp`).
4. Deploy. Your MCP endpoint will be `https://<project>.fastmcp.app/mcp`.

Every push to `main` redeploys automatically.

### Content pipeline

The **TypeScript files in `src/content/` are the source of truth**. After editing any content there, regenerate `content.json` and commit it:

```bash
npm run build && node scripts/dump-content.mjs
```

The TypeScript server (`src/index.ts`, deployable via the `Dockerfile` to Railway/Render) remains as an alternative; both serve identical content.

### Run the Python server locally

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python server.py    # http://localhost:3000/mcp
```

---

## Connecting to Claude (Desktop App)

Add to your Claude Desktop config file (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "emxai-studio": {
      "type": "http",
      "url": "https://your-app.up.railway.app/mcp"
    }
  }
}
```

Restart Claude Desktop. You'll see the prompts available in the prompt picker.

## Connecting to ChatGPT

ChatGPT supports remote MCP servers (HTTP/SSE):

1. In ChatGPT, go to **Settings → Connectors → Add MCP Server**.
2. Enter your server URL: `https://your-app.up.railway.app/mcp`
3. The prompts will appear in your ChatGPT workspace.

---

## Running Locally

```bash
npm install
npm run dev          # Development with hot reload
# or
npm run build && npm start   # Production build
```

Server runs at `http://localhost:3000`. MCP endpoint: `http://localhost:3000/mcp`.

For local Claude Desktop use:
```json
{
  "mcpServers": {
    "emxai-studio-local": {
      "type": "http",
      "url": "http://localhost:3000/mcp"
    }
  }
}
```

---

## Using the Prompts

### In Claude Desktop
- Open the prompt picker (slash command or toolbar)
- Type the prompt name (e.g., `aias-advisor`)
- Optionally fill in parameters (e.g., subject: "Engineering", level: "undergraduate")
- The system prompt activates and you start your conversation normally

### In ChatGPT
- Access via the MCP connector toolbar
- Select a prompt and fill in any parameters
- Start your conversation

### Parameters Are Optional
All parameters are optional. Each prompt is designed to ask for the information it needs if you don't pre-fill it.

---

## Project Structure

```
src/
├── index.ts              # Express server + MCP prompt registration
└── content/
    ├── aias.ts           # AI Assessment Scale Advisor prompt
    ├── eml.ts            # EML Architect prompt + all reference docs
    ├── interactive-builder.ts   # Phase 1 & Phase 2 prompts
    ├── autonomy.ts       # Course Autonomy Coach prompt
    ├── engagement.ts     # Joyful Opener Designer prompt
    ├── passion.ts        # Passion Connector prompt
    └── optimizer.ts      # Prompt Optimizer + best practices
```

## Adding or Updating Prompts

1. Edit or add content in `src/content/`
2. Register the prompt in `src/index.ts` using `server.prompt(...)`
3. Run `npm run build` to compile
4. Redeploy (Railway auto-deploys on git push)

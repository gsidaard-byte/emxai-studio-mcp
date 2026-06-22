# Sid's EML Studio MCP

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

---

## Deployment (Railway — Recommended)

Railway provides a free tier with persistent server support needed for MCP streaming.

### Step 1: Push to GitHub

```bash
cd /path/to/MCP_EM
git init
git add .
git commit -m "Initial teaching prompts MCP server"
gh repo create sids-eml-studio-mcp --public --source=. --push
```

### Step 2: Deploy on Railway

1. Go to [railway.app](https://railway.app) and sign in with GitHub.
2. Click **New Project → Deploy from GitHub repo** and select `sids-eml-studio-mcp`.
3. Railway auto-detects the Dockerfile and deploys.
4. In your project settings, find the **public URL** (e.g., `https://sids-eml-studio-mcp.up.railway.app`).

Your MCP endpoint will be: `https://your-app.up.railway.app/mcp`

---

## Connecting to Claude (Desktop App)

Add to your Claude Desktop config file (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "sids-eml-studio": {
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
    "sids-eml-studio-local": {
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

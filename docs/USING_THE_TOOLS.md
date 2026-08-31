# Using the EMxAI Studio Tools — A Practical Guide

This guide shows how to invoke every tool, with example phrasings and what to expect back. It assumes the server is already connected (see `MCP_OVERVIEW.md` for connection setup).

## How invocation works

**In Claude** (Desktop or web with the connector added): type `/` in the message box and pick a prompt from the menu, e.g. `/em-list`. Claude fills in any parameters by asking you, then the tool's content becomes the operating instructions for the conversation. You can also just ask in plain language ("use the em_diagnostic tool") — both work.

**In ChatGPT** (with the connector enabled for the conversation): ask in plain language and name the tool, e.g. *"Use the `eml_architect` tool to reframe this problem: …"*. ChatGPT calls the tool, receives the instructions, and follows them for the rest of the conversation.

**General pattern:** most tools return a *persona plus procedure* — after calling one, simply talk to the assistant as if it were that specialist. All parameters are optional unless marked required; omitting them means the assistant will ask you for what it needs, which is often the better experience the first time.

---

## Group 1 — Teaching Prompts

### `aias_advisor` / `/aias-advisor` — redesign homework for the AI era

- **Use when:** you have an existing homework problem or assessment and need to decide what level of AI use to allow, and how to keep the assessment valid.
- **Say:** *"Use aias_advisor. Subject: mechanical engineering, level: sophomore. Here is my homework problem: [paste]"*
- **You get:** a full redesign across the five AIAS levels (No AI → AI Exploration): a diagnosis, a redesign table, a recommended level, student-facing instructions, a rubric outline, and integrity safeguards.
- **Tip:** have the learning objectives handy — the advisor's first question is always "what evidence of learning do you need?"

### `eml_architect` / `/eml-architect` — turn textbook problems into EM learning tasks

- **Use when:** you want a traditional problem to build entrepreneurial-mindset habits without losing technical rigor.
- **Say:** *"Use eml_architect with em_habits = Curiosity. Problems: [paste one or more numbered textbook problems]"* — or omit both and paste problems when asked.
- **You get:** for each problem, a card with a Mindset Opener (names the habit explicitly), a Reframed Technical Problem (same rigor, real-world narrative, no solutions), and a Mindset Closer (a tailored reflection). It offers to iterate on each part.
- **Tip:** it will not solve the problem or include equations that help solve it — that's by design.

### `interactive_builder_planning` / `/interactive-builder-planning` — design an educational web tool (phase 1)

- **Use when:** you have an idea (or just a friction point) for a small classroom web tool and want a buildable blueprint. No coding happens here.
- **Say:** *"Run interactive_builder_planning."* Then answer its interview one question at a time.
- **You get:** a `Final_Blueprint_Summary` — concept, user flow, interaction logic, privacy constraints, and instructions for a coding AI. Save this text.

### `interactive_builder_coding` / `/interactive-builder-coding` — build the web tool (phase 2)

- **Use when:** you have a blueprint from phase 1 (or a clear description) and want a working prototype.
- **Say:** *"Run interactive_builder_coding. Here is my blueprint: [paste]"*
- **You get:** a single self-contained `index.html` you can save and double-click to open — no server, accounts, or data collection. It builds a minimal version first and asks for feedback before expanding.

### `autonomy_coach` / `/autonomy-coach` — add student choice without chaos

- **Use when:** engagement or ownership is low and you want bounded student choice (formats, pacing, tools, grading paths).
- **Say:** *"Use autonomy_coach. Course: fluid mechanics, level: junior. My challenge: students only do the minimum."*
- **You get:** 2–3 strategies matched to your problem from a 20-strategy playbook, each with draft-ready syllabus language, assignment instructions, and guardrails (equity check, common rubric, 3–5 options max).

### `engagement_opener` / `/engagement-opener` — a 3-minute class opener

- **Use when:** you're introducing a concept and want a short, joyful hook (surprise, dissonance, or collaborative discovery) — not a generic icebreaker.
- **Say:** *"Use engagement_opener. Course: Statics, sophomore. Concept: free body diagrams."*
- **You get:** three options (A/B/C) with scripts timed to ≤180 seconds and ≤10 minutes prep; pick one (or say "remix") and it produces a copy-ready worksheet.

### `passion_connector` / `/passion-connector` — bring your passion into class

- **Use when:** you want a genuine 5-minute segment connecting something you love to what you teach.
- **Say:** *"Use passion_connector. Passion: rock climbing. Course: mechanics of materials."*
- **You get:** two low-prep segment ideas, each with a description, the course connection, why it reads as authentic rather than gimmicky, and a sentence starter.

### `prompt_optimizer` / `/prompt-optimizer` — upgrade a rough prompt

- **Use when:** you (or a colleague) have a rough prompt and want a precise, production-ready version for a specific model.
- **Say:** *"Use prompt_optimizer, target_model = Claude. Raw prompt: [paste]"*
- **You get:** one upgraded prompt in a code block — role, objective, steps, output format, acceptance criteria — tuned with model-specific best practices (Claude and GPT get an appended best-practices reference).

---

## Group 2 — EM × AI Field Guide

*The 18 KEEN habits and 7 workflows. If unsure where to start: `em_diagnostic`.*

### `em_list` / `/em-list` — the map

- **Say:** *"Call em_list."*
- **You get:** all 3 families, 18 habits (each with its one-line tension), and 7 workflows — a browsing index for the tools below.

### `em_habit` / `/em-habit` — everything about one habit

- **Say:** *"Use em_habit for Systems Thinking."* (Names are case- and punctuation-insensitive; a wrong name returns the valid list.)
- **You get:** the habit's family, definition, named frameworks, the AI-era move, how AI helps build it, the anti-pattern, the tension, a **Run it yourself** paste-ready prompt, and a **Run it with students** blueprint (Setup / AI's role / Assessed on).

### `em_coach` / `/em-coach` — just the practice prompt

- **Use when:** you want to practice one habit on your own work right now, without the full write-up.
- **Say:** *"Use em_coach for Risk Awareness"* — then paste the returned prompt into a fresh conversation (or tell the assistant to act on it directly), filling the [bracketed] slot with your project.

### `em_workflow` / `/em-workflow` — a guided multi-habit session

- **Use when:** you have a real task (a decision to pressure-test, a claim to verify, a repeated task to systematize) rather than one habit to drill.
- **Say:** *"Run em_workflow for Assumption Buster, and then facilitate it with me."*
- **You get:** the orchestration prompt (the assistant walks you through numbered steps, pausing after each for your response), plus the student blueprint and a *Prompt to build this activity* meta-prompt for creating a class version.
- **The 7 workflows:** EM × AI Diagnostic · Reality Check · Assumption Buster · Experiment Multiplier · Expertise to Files · System Builder · Value-Chain Climber.

### `em_diagnostic` / `/em-diagnostic` — where should I start?

- **Say:** *"Run em_diagnostic and interview me."*
- **You get:** a one-question-at-a-time assessment of your own AI practice across the 3 Cs, ending with a routing recommendation to the specific habit coach or workflow that fits your weakest spot.

---

## Group 3 — EM Assessment Toolkit

*Course-embedded assessment of the 18 habits. These tools assess demonstrated performance in specific artifacts — never personality. `NE` (not elicited) is always distinct from a score of `0`.*

**The recommended sequence:**

1. **Before assigning work** — `em_list_habits` to choose targets, then `em_plan_assessment` to align the assignment.
2. **Per submission** — `em_get_habit` to load the look-fors, judge the evidence yourself, then `em_score_evidence_episode` to apply the scoring rules.
3. **End of course** — `em_synthesize_profile` across all episodes; review before reporting.

### `em_list_habits` — discover and filter

- **Say:** *"Call em_list_habits with category = Creating Value"* or *"…search = stakeholder"*.
- **You get:** matching habits with their 3C category and core intellectual theme (the thing a student must actually do).

### `em_get_habit` — the assessment definition

- **Say:** *"Use em_get_habit for Experimentation."* (Unambiguous partial names work: "systems" resolves to Systems Thinking.)
- **You get:** the official description, core theme, **strong-evidence look-fors**, **do-not-count exclusions** (guards against crediting generic productivity or raw AI output), and related observable behaviors.

### `em_get_behavior_rubric` — the four anchors for one behavior

- **Say:** *"Use em_get_behavior_rubric for 'learns from failure'."*
- **You get:** the behavior's definition and four developmental anchors (0 Not yet evident → 3 Proficient). Use as a corroborating layer; do not average habit scores into a behavior score.

### `em_plan_assessment` — align an assignment before you give it

- **Say:** *"Use em_plan_assessment. Assignment: Bridge design memo. Artifact: design memo. Target habits: Risk Awareness, Systems Thinking. AI use: optional. Stakes: high."*
- **You get:** per-habit elicitation requirements and required evidence, a minimum evidence bundle, an AI-transparency requirement matched to your AI policy, and corroboration guidance (high stakes adds a second rater / oral defense).
- **Tip:** 1–3 habits only, and only ones the task *genuinely* requires — the tool refuses duplicates and the scoring layer will return NE if the task never elicited the habit.

### `em_score_evidence_episode` — score one piece of evidence

- **How it works:** *you* judge the evidence against `em_get_habit` first; the tool then converts your judgments into a defensible score. Encode your judgments as booleans:
- **Say:** *"Score this with em_score_evidence_episode: target_habit = Experimentation; elicited = true; attributable_to_student = true; sufficient_evidence = true; distinctive_move_attempted = true; supported_by_relevant_evidence = true; changed_decision_or_work = false; addressed_limitations_or_counterevidence = false; proactive_or_adaptive_transfer = false; evidence_locator = 'lab report §3'."*
- **You get:** a provisional rating (NE, 0, 1 Developing, 2 Advancing, or 3 Proficient) with confidence, rationale, and a concrete **next move** (what evidence would raise the score).
- **Easier path:** use the `review-em-evidence` prompt (below) and let the assistant walk the judgments with you.

### `em_synthesize_profile` — course-level screening

- **Say:** *"Use em_synthesize_profile with these episodes: [list each as construct, score, task_type, sequence, plus individual_evidence/novel_context where known]"*.
- **You get:** per-construct screening statuses (Insufficient evidence / Not yet evident / Developing / Advancing / Proficient candidate). "Proficient candidate" has strict gates: ≥3 valid occasions, ≥2 task types, ≥2 scores of 3, one individually attributable and one in a novel context.
- **Boundary:** the output is a screening status requiring instructor review — never an automatic grade.

### `review-em-evidence` (prompt) — guided single-artifact review

- **In Claude:** `/review-em-evidence`, then supply the habit and a brief evidence excerpt.
- **You get:** the assistant retrieves the habit definition, decides whether the task elicited the move, cites exact evidence, separates NE from 0, and calls the scoring tool — the guided version of the manual sequence above.

### Reference resources

MCP clients that support resources can attach `em://habits`, `em://observable-behaviors`, and `em://scoring-scale` for the raw definitions in JSON.

---

## Quick tips

- **Formats:** every assessment tool accepts `response_format = "json"` for machine-readable output (useful for Canvas/LMS pipelines); markdown is the default.
- **Names are forgiving:** habit/workflow lookups match regardless of case and punctuation, and errors always list the valid names.
- **Nothing is stored:** every call is stateless and read-only. Paste brief excerpts and locators, not whole submissions or student identifiers.
- **When in doubt, start with** `em_diagnostic` (for your own practice) or `em_list` (to browse).

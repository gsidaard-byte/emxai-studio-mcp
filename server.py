"""EMxAI Studio MCP Server (FastMCP / Python).

Serves curated teaching prompts and the EM x AI Field Guide for engineering
faculty. Every capability is exposed both as a tool (ChatGPT connector) and
as a prompt (Claude slash menu).

Content lives in content.json, generated from the TypeScript source of truth:
    npm run build && node scripts/dump-content.mjs

Run locally:      python server.py            (HTTP on port 3000, endpoint /mcp)
FastMCP Cloud:    entrypoint server.py:mcp
"""

import json
import os
import re
from pathlib import Path
from typing import Literal

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from em_assessment_data import BEHAVIORS, HABITS, SCORING_SCALE
from em_assessment_logic import resolve_name, score_episode, synthesize_profile
from em_assessment_models import EvidenceEpisodeInput, RatedEpisode

CONTENT = json.loads((Path(__file__).parent / "content.json").read_text(encoding="utf-8"))

mcp = FastMCP(name="emxai-studio-mcp")

READ_ONLY = {
    "readOnlyHint": True,
    "openWorldHint": False,
    "destructiveHint": False,
    "idempotentHint": True,
}

HABIT_NAMES = list(CONTENT["em"]["habits"].keys())
WORKFLOW_NAMES = list(CONTENT["em"]["workflows"].keys())


def _normalize(s: str) -> str:
    """Case- and punctuation-insensitive key (mirrors the TS implementation)."""
    s = re.sub(r"[\s_\-×x]+", "", s.lower())
    return re.sub(r"[^a-z0-9]", "", s)


def _find(table: dict, name: str) -> str | None:
    target = _normalize(name)
    for key in table:
        if _normalize(key) == target:
            return key
    return None


def _find_workflow(name: str) -> str | None:
    key = _find(CONTENT["em"]["workflows"], name)
    if key:
        return key
    aliases = {"diagnostic": "EM × AI Diagnostic"}
    return aliases.get(_normalize(name))


# ─── Teaching-prompt builders (shared by tools and prompts) ───────────────────

def build_aias(subject: str | None = None, level: str | None = None) -> str:
    prompt = CONTENT["aias"]
    if subject or level:
        ctx = " ".join(p for p in [level, subject] if p)
        prompt += f"\n\nContext note: The educator is working with a {ctx} course. Tailor your recommendations accordingly."
    return prompt


def build_eml(em_habits: str | None = None, problems: str | None = None) -> str:
    prompt = CONTENT["eml_full"]
    if em_habits:
        prompt = prompt.replace(
            "If the user specifies EM habits, use only those.",
            f"The instructor has specified these EM habits to focus on: {em_habits}. "
            "Use only these habits unless the user changes them.",
        )
    if problems:
        prompt += f"\n\n<PROBLEMS>\n{problems}\n</PROBLEMS>"
    return prompt


def build_autonomy(course_subject: str | None = None, course_level: str | None = None) -> str:
    prompt = CONTENT["autonomy"]
    if course_subject or course_level:
        ctx = " ".join(p for p in [course_level, course_subject] if p)
        prompt += f"\n\nContext note: The instructor is teaching a {ctx} course. Adapt all recommendations to this discipline and level."
    return prompt


def build_engagement(course_title: str | None = None, concept: str | None = None) -> str:
    prompt = CONTENT["engagement"]
    if course_title or concept:
        parts = []
        if course_title:
            parts.append(f"Course: {course_title}")
        if concept:
            parts.append(f"Concept: {concept}")
        prompt += f"\n\nContext note: Skip the intake question. {'; '.join(parts)}. Proceed directly to generating three options."
    return prompt


def build_passion(passion: str | None = None, course: str | None = None) -> str:
    prompt = CONTENT["passion"]
    if passion or course:
        parts = []
        if passion:
            parts.append(f"[X] = {passion}")
        if course:
            parts.append(f"[Y] = {course}")
        prompt += f"\n\nContext note: Skip the intake questions. {'; '.join(parts)}. Proceed directly to generating two classroom segment ideas."
    return prompt


def build_optimizer(
    target_model: str | None = None,
    raw_prompt: str | None = None,
    optional_context: str | None = None,
) -> str:
    prompt = CONTENT["optimizer"]["base"]
    if raw_prompt:
        prompt = prompt.replace("{{RAW_PROMPT}}", raw_prompt)
    if optional_context:
        prompt = prompt.replace("{{OPTIONAL_CONTEXT}}", optional_context)
    model = target_model or "model-agnostic"
    prompt = prompt.replace("{{TARGET_MODEL: Claude | Gemini | GPT | model-agnostic}}", model)
    m = model.lower()
    if "claude" in m:
        prompt += "\n\n" + CONTENT["optimizer"]["claude_bp"]
    elif "gpt" in m or "openai" in m:
        prompt += "\n\n" + CONTENT["optimizer"]["gpt_bp"]
    return prompt


def em_habit_text(name: str) -> str:
    key = _find(CONTENT["em"]["habits"], name)
    if not key:
        return f'No habit named "{name}". Valid habits are: {", ".join(HABIT_NAMES)}. Call em_list to see the full map.'
    return CONTENT["em"]["habits"][key]["full"]


def em_coach_text(habit: str) -> str:
    key = _find(CONTENT["em"]["habits"], habit)
    if not key:
        return f'No habit named "{habit}". Valid habits are: {", ".join(HABIT_NAMES)}. Call em_list to see the full map.'
    return CONTENT["em"]["habits"][key]["coach"]


def em_workflow_text(name: str) -> str:
    key = _find_workflow(name)
    if not key:
        return f'No workflow named "{name}". Valid workflows are: {", ".join(WORKFLOW_NAMES)}. Call em_list to see the full map.'
    return CONTENT["em"]["workflows"][key]["full"]


# ─── Tools (ChatGPT connector; annotations required) ──────────────────────────

@mcp.tool(annotations=READ_ONLY)
def aias_advisor(subject: str | None = None, level: str | None = None) -> str:
    """Returns a system prompt that turns the assistant into an AI Assessment Scale Advisor, helping educators redesign homework using the 5-level AIAS framework. Use the returned text as operating instructions for the rest of the conversation."""
    return build_aias(subject, level)


@mcp.tool(annotations=READ_ONLY)
def eml_architect(em_habits: str | None = None, problems: str | None = None) -> str:
    """Returns a system prompt that turns the assistant into an Entrepreneurial Mindset Learning Architect, converting textbook problems into EM learning tasks. Includes full reference materials (Habits of EM, Curiosity Methods, Mindset Methods, EM Openers, Adaptable EML Ideas)."""
    return build_eml(em_habits, problems)


@mcp.tool(annotations=READ_ONLY)
def interactive_builder_planning() -> str:
    """Returns a system prompt that guides faculty through designing a stateless, privacy-safe educational web-app. Produces a Final Blueprint Summary ready for the coding phase."""
    return CONTENT["interactive_builder_planning"]


@mcp.tool(annotations=READ_ONLY)
def interactive_builder_coding() -> str:
    """Returns a system prompt that takes a blueprint from the planning phase and builds a working single-file HTML prototype."""
    return CONTENT["interactive_builder_coding"]


@mcp.tool(annotations=READ_ONLY)
def autonomy_coach(course_subject: str | None = None, course_level: str | None = None) -> str:
    """Returns a system prompt that helps university instructors embed student autonomy into courses using 20 proven strategies."""
    return build_autonomy(course_subject, course_level)


@mcp.tool(annotations=READ_ONLY)
def engagement_opener(course_title: str | None = None, concept: str | None = None) -> str:
    """Returns a system prompt that creates a 3-minute classroom micro-experiment sparking curiosity through cognitive dissonance, sensory surprise, or collaborative discovery."""
    return build_engagement(course_title, concept)


@mcp.tool(annotations=READ_ONLY)
def passion_connector(passion: str | None = None, course: str | None = None) -> str:
    """Returns a system prompt that helps educators design a 5-minute classroom segment linking their personal passion to course content."""
    return build_passion(passion, course)


@mcp.tool(annotations=READ_ONLY)
def prompt_optimizer(
    target_model: Literal["Claude", "Gemini", "GPT", "model-agnostic"] | None = None,
    raw_prompt: str | None = None,
    optional_context: str | None = None,
) -> str:
    """Returns a system prompt that rewrites rough prompts into precise, production-ready prompts for Claude, Gemini, or GPT."""
    return build_optimizer(target_model, raw_prompt, optional_context)


@mcp.tool(annotations=READ_ONLY)
def em_list() -> str:
    """Returns the full map of the EM × AI Field Guide: the 3 families (Curiosity, Connections, Creating Value), all 18 KEEN habits with their one-line tensions, and the 7 workflows. Start here to see what's available, then call em_habit or em_workflow for full content."""
    return CONTENT["em"]["list"]


@mcp.tool(annotations=READ_ONLY)
def em_habit(name: str) -> str:
    """Returns the full content for one of the 18 KEEN entrepreneurial-mindset habits: its family, definition, named frameworks, the AI-era move, how AI helps build it, the anti-pattern, the one-line tension, the Run-it-yourself paste-ready prompt, and the Run-it-with-students blueprint. Valid habits: Inquisitiveness, Contrarian Thinking, Opportunity Seeking, Experimentation, Confronting Ambiguity, Future-Minded, Creativity, Systems Thinking, Knowledge Synthesis, Implications Thinking, Strategic Thinking, Risk Awareness, Value Awareness, Customer-Centric Thinking, Impact Thinking, Socially Minded, Persistence, Resourcefulness."""
    return em_habit_text(name)


@mcp.tool(annotations=READ_ONLY)
def em_coach(habit: str) -> str:
    """Returns just the Run-it-yourself paste-ready prompt for a habit (plus its framing: what it does, when to use it, what good output looks like). Use this when you want to run a habit on your own task right now. Valid habits: Inquisitiveness, Contrarian Thinking, Opportunity Seeking, Experimentation, Confronting Ambiguity, Future-Minded, Creativity, Systems Thinking, Knowledge Synthesis, Implications Thinking, Strategic Thinking, Risk Awareness, Value Awareness, Customer-Centric Thinking, Impact Thinking, Socially Minded, Persistence, Resourcefulness."""
    return em_coach_text(habit)


@mcp.tool(annotations=READ_ONLY)
def em_workflow(name: str) -> str:
    """Returns a full multi-habit workflow: the habits it composes, when to reach for it, the Run-it-yourself orchestration prompt (a system prompt with a pause-after-each-step contract), the Run-it-with-students blueprint, and the meta-prompt to build a class activity. Valid workflows: EM × AI Diagnostic, Reality Check, Assumption Buster, Experiment Multiplier, Expertise to Files, System Builder, Value-Chain Climber."""
    return em_workflow_text(name)


@mcp.tool(annotations=READ_ONLY)
def em_diagnostic() -> str:
    """Returns the EM × AI Diagnostic orchestration prompt. Start here when you don't yet know which habit or workflow you need — it assesses your AI practice across all three Cs and routes you to the right tool. Use the returned text as your operating instructions."""
    return CONTENT["em"]["workflows"]["EM × AI Diagnostic"]["pm"]


# ─── Prompts (Claude slash menu) ──────────────────────────────────────────────

@mcp.prompt(name="aias-advisor")
def p_aias(subject: str | None = None, level: str | None = None) -> str:
    """AI Assessment Scale Advisor — helps educators redesign homework and assessments using the 5-level AI Assessment Scale (AIAS). Produces full redesigns with student-facing instructions, rubrics, and safeguards."""
    return build_aias(subject, level)


@mcp.prompt(name="eml-architect")
def p_eml(em_habits: str | None = None, problems: str | None = None) -> str:
    """EML Architect — converts textbook problems into Entrepreneurial Mindset Learning tasks (includes all reference materials)."""
    return build_eml(em_habits, problems)


@mcp.prompt(name="interactive-builder-planning")
def p_ib1() -> str:
    """Interactive Builder Phase 1 — designs a privacy-safe educational web-app blueprint."""
    return CONTENT["interactive_builder_planning"]


@mcp.prompt(name="interactive-builder-coding")
def p_ib2() -> str:
    """Interactive Builder Phase 2 — builds a working single-file HTML prototype from the blueprint."""
    return CONTENT["interactive_builder_coding"]


@mcp.prompt(name="autonomy-coach")
def p_autonomy(course_subject: str | None = None, course_level: str | None = None) -> str:
    """Course Autonomy Coach — embeds student autonomy using 20 proven strategies."""
    return build_autonomy(course_subject, course_level)


@mcp.prompt(name="engagement-opener")
def p_engagement(course_title: str | None = None, concept: str | None = None) -> str:
    """Joyful Opener Designer — creates a 3-minute curiosity-sparking classroom micro-experiment."""
    return build_engagement(course_title, concept)


@mcp.prompt(name="passion-connector")
def p_passion(passion: str | None = None, course: str | None = None) -> str:
    """Passion Connector — links personal passion to course content in 5 minutes."""
    return build_passion(passion, course)


@mcp.prompt(name="prompt-optimizer")
def p_optimizer(
    target_model: str | None = None,
    raw_prompt: str | None = None,
    optional_context: str | None = None,
) -> str:
    """Prompt Optimizer — rewrites rough prompts into precise, production-ready prompts for Claude, Gemini, or GPT."""
    return build_optimizer(target_model, raw_prompt, optional_context)


@mcp.prompt(name="em-list")
def p_em_list() -> str:
    """EM Field Guide map — the 3 families, 18 KEEN habits with their tensions, and 7 workflows. Start here to browse what's available."""
    return CONTENT["em"]["list"]


@mcp.prompt(name="em-habit")
def p_em_habit(name: str) -> str:
    """Full content for one of the 18 KEEN entrepreneurial-mindset habits (frameworks, AI-era move, anti-pattern, Run-it-yourself prompt, Run-it-with-students blueprint)."""
    return em_habit_text(name)


@mcp.prompt(name="em-coach")
def p_em_coach(habit: str) -> str:
    """Just the Run-it-yourself paste-ready prompt for a habit, ready to run on your own task."""
    return em_coach_text(habit)


@mcp.prompt(name="em-workflow")
def p_em_workflow(name: str) -> str:
    """Full multi-habit workflow: orchestration prompt with pause-after-each-step contract, plus the Run-it-with-students blueprint and build-an-activity meta-prompt."""
    return em_workflow_text(name)


@mcp.prompt(name="em-diagnostic")
def p_em_diagnostic() -> str:
    """EM × AI Diagnostic — assesses your AI practice across all three Cs and routes you to the right habit or workflow. Start here if unsure where to begin."""
    return CONTENT["em"]["workflows"]["EM × AI Diagnostic"]["pm"]


# ─── EM Assessment Toolkit ────────────────────────────────────────────────────
# Source-grounded assessment of the 18 Habits of EM and 8 observable behaviors.
# Ported from EM_Assessment_Toolkit/mcp/em-assessment-mcp (data and scoring
# logic copied verbatim; see em_assessment_*.py). Assesses demonstrated
# performance in artifacts, never personality. NE (not elicited) is distinct
# from a score of 0.

ASSESSMENT_CHAR_LIMIT = 25_000


def _ajson(data) -> str:
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if len(text) <= ASSESSMENT_CHAR_LIMIT:
        return text
    return text[: ASSESSMENT_CHAR_LIMIT - 180] + "\n... Response truncated. Narrow the request or use pagination."


def _habit_markdown(name: str, record: dict) -> str:
    look_for = "\n".join(f"- {item}" for item in record["look_for"])
    behaviors = ", ".join(record["related_behaviors"])
    return f"""# {name}

**3C category:** {record['category']}
**Official description:** {record['official_description']}

## Core intellectual theme
{record['core_theme']}

## Strong evidence in student work
{look_for}

## Do not count
{record['do_not_count']}

## Related observable behavior(s)
{behaviors}
"""


@mcp.tool(annotations=READ_ONLY)
def em_list_habits(
    category: Literal["Curiosity", "Connections", "Creating Value"] | None = None,
    search: str | None = None,
    limit: int = 18,
    offset: int = 0,
    response_format: Literal["markdown", "json"] = "markdown",
) -> str:
    """List the 18 Habits of EM with optional category/search filters and pagination. Use this before selecting assessment targets or when a habit name is uncertain. Results include names, 3C categories, official descriptions, and core themes. This tool does not score student work."""
    rows = []
    needle = search.casefold() if search else None
    for name, record in HABITS.items():
        if category and record["category"] != category:
            continue
        haystack = " ".join([name, str(record["core_theme"]), " ".join(record["look_for"])]).casefold()
        if needle and needle not in haystack:
            continue
        rows.append({"name": name, "category": record["category"], "official_description": record["official_description"], "core_theme": record["core_theme"]})
    page = rows[offset : offset + limit]
    has_more = offset + len(page) < len(rows)
    payload = {"total": len(rows), "count": len(page), "offset": offset, "has_more": has_more, "next_offset": offset + len(page) if has_more else None, "habits": page}
    if response_format == "json":
        return _ajson(payload)
    lines = ["# Habits of Entrepreneurial Mindset", f"Showing {len(page)} of {len(rows)} matches.", ""]
    lines.extend(f"- **{row['name']}** ({row['category']}): {row['core_theme']}" for row in page)
    if has_more:
        lines.append(f"\nMore results are available; call again with offset={payload['next_offset']}.")
    return "\n".join(lines)


@mcp.tool(annotations=READ_ONLY)
def em_get_habit(habit: str, response_format: Literal["markdown", "json"] = "markdown") -> str:
    """Retrieve the assessment definition for one Habit of EM: official description, distinctive intellectual theme, strong evidence look-fors, exclusions that guard against generic productivity claims, and related observable behaviors. Use before judging alignment or student evidence. Partial names must be unambiguous."""
    try:
        name = resolve_name(habit, HABITS, "habit")
    except ValueError as error:
        return f"Error: {error}"
    if response_format == "json":
        return _ajson({"name": name, **HABITS[name]})
    return _habit_markdown(name, HABITS[name])


@mcp.tool(annotations=READ_ONLY)
def em_get_behavior_rubric(behavior: str, response_format: Literal["markdown", "json"] = "markdown") -> str:
    """Retrieve the four developmental anchors (0-3) for one of the eight observable EM behaviors. Use as a corroborating performance layer after determining what the assignment elicited. Do not mechanically infer a behavior score by averaging related habit scores."""
    try:
        name = resolve_name(behavior, BEHAVIORS, "observable behavior")
    except ValueError as error:
        return f"Error: {error}"
    record = BEHAVIORS[name]
    if response_format == "json":
        return _ajson({"name": name, "definition": record["definition"], "anchors": {str(i): t for i, t in enumerate(record["anchors"])}})
    anchors = "\n".join(f"- **{i} — {['Not yet evident', 'Developing', 'Advancing', 'Proficient'][i]}:** {t}" for i, t in enumerate(record["anchors"]))
    return f"# {name}\n\n{record['definition']}\n\n{anchors}\n\nUse NE—not 0—when the task did not elicit the behavior or evidence is insufficient."


@mcp.tool(annotations=READ_ONLY)
def em_plan_assessment(
    assignment_name: str,
    artifact_type: str,
    target_habits: list[str],
    ai_use: Literal["not_allowed", "optional", "required"] = "optional",
    stakes: Literal["practice", "low", "moderate", "high"] = "low",
    response_format: Literal["markdown", "json"] = "markdown",
) -> str:
    """Build an aligned assessment specification for one assignment. Select one to three habits genuinely required by the task. Returns habit-specific elicitation requirements, required evidence, non-examples, related behaviors, AI-transparency prompts, and stakes-appropriate corroboration. It does not write or change a course gradebook."""
    try:
        names = [resolve_name(item, HABITS, "habit") for item in target_habits]
    except ValueError as error:
        return f"Error: {error}"
    if not 1 <= len(names) <= 3:
        return "Error: choose one to three target habits."
    if len(set(names)) != len(names):
        return "Error: target_habits contains a duplicate. Choose one to three distinct habits."
    targets = []
    behaviors: list[str] = []
    for name in names:
        record = HABITS[name]
        targets.append({"habit": name, "learning_objective": record["core_theme"], "elicitation_requirement": f"Require the student to {str(record['core_theme'])[0].lower() + str(record['core_theme'])[1:]}", "required_evidence": record["look_for"], "do_not_count": record["do_not_count"]})
        behaviors.extend(record["related_behaviors"])
    unique_behaviors = list(dict.fromkeys(behaviors))[:2]
    ai_requirement = {
        "not_allowed": "State that generative AI is not permitted for this evidence occasion.",
        "optional": "If AI contributed, identify what it proposed, what was verified or rejected, why, and what changed in the work.",
        "required": "Require an AI decision trace: framing/constraint, verification, at least one accepted or rejected suggestion, rationale, and resulting revision.",
    }[ai_use]
    corroboration = "Add a second rater or brief oral defense and preserve an individual trace." if stakes == "high" else "Use a product locator plus a short process explanation when reasoning is not visible."
    payload = {"assignment_name": assignment_name, "artifact_type": artifact_type, "targets": targets, "observable_behaviors_for_optional_corroboration": unique_behaviors, "minimum_evidence_bundle": ["product evidence with an exact locator", "reasoning/process trace", "verification evidence when the habit calls for it", "individual evidence for individual claims"], "ai_transparency_requirement": ai_requirement, "corroboration": corroboration, "scoring_scale": SCORING_SCALE, "validity_check": "Use NE when the task did not elicit the construct or evidence is insufficient; never convert missing evidence to 0."}
    if response_format == "json":
        return _ajson(payload)
    sections = [f"# Assessment plan: {assignment_name}", f"**Artifact:** {artifact_type}", ""]
    for target in targets:
        sections.extend([f"## {target['habit']}", f"**Learning objective:** {target['learning_objective']}", f"**Elicitation:** {target['elicitation_requirement']}", "**Require evidence of:**", *[f"- {item}" for item in target["required_evidence"]], f"**Do not count:** {target['do_not_count']}", ""])
    sections.extend(["## Evidence and scoring", "- Product evidence with an exact locator", "- Reasoning/process trace", "- Verification evidence when the habit calls for it", "- Individual evidence for individual claims", f"\n**AI transparency:** {ai_requirement}", f"\n**Corroboration:** {corroboration}", "\nUse NE when the task did not elicit the construct or evidence is insufficient."])
    return "\n".join(sections)


@mcp.tool(annotations=READ_ONLY)
def em_score_evidence_episode(
    target_habit: str,
    elicited: bool,
    attributable_to_student: bool,
    sufficient_evidence: bool,
    distinctive_move_attempted: bool,
    supported_by_relevant_evidence: bool,
    changed_decision_or_work: bool,
    addressed_limitations_or_counterevidence: bool,
    proactive_or_adaptive_transfer: bool,
    individual_evidence: bool = True,
    novel_context: bool = False,
    evidence_locator: str | None = None,
    evidence_note: str | None = None,
    response_format: Literal["markdown", "json"] = "markdown",
) -> str:
    """Apply the common NE/0-3 decision rules to one structured evidence episode. The caller must judge the supplied evidence against em_get_habit first, then encode those judgments in the boolean fields. Distinguishes missing/not-elicited evidence (NE) from a true zero and returns a provisional score, confidence, rationale, and next move. It does not infer personality, authorship, or understanding from polished prose or AI output."""
    try:
        episode = EvidenceEpisodeInput(
            target_habit=target_habit,
            elicited=elicited,
            attributable_to_student=attributable_to_student,
            sufficient_evidence=sufficient_evidence,
            distinctive_move_attempted=distinctive_move_attempted,
            supported_by_relevant_evidence=supported_by_relevant_evidence,
            changed_decision_or_work=changed_decision_or_work,
            addressed_limitations_or_counterevidence=addressed_limitations_or_counterevidence,
            proactive_or_adaptive_transfer=proactive_or_adaptive_transfer,
            individual_evidence=individual_evidence,
            novel_context=novel_context,
            evidence_locator=evidence_locator,
            evidence_note=evidence_note,
        )
        result = score_episode(episode)
    except ValueError as error:
        return f"Error: {error}"
    if response_format == "json":
        return _ajson(result)
    return f"# Evidence episode: {result['habit']}\n\n**Provisional rating:** {result['score']} — {result['level']}  \n**Confidence:** {result['confidence']}  \n**Rationale:** {result['rationale']}  \n**Next move:** {result['next_move']}"


@mcp.tool(annotations=READ_ONLY)
def em_synthesize_profile(
    episodes: list[RatedEpisode],
    response_format: Literal["markdown", "json"] = "markdown",
) -> str:
    """Synthesize multiple rated episodes into course-level screening statuses. NE episodes remain visible but are excluded from numeric summaries. A Proficient candidate requires at least three valid occasions across two task types, two ratings of 3, one individually attributable 3, and one 3 in a novel/changed context. Every result requires instructor review before final reporting."""
    try:
        results = synthesize_profile(list(episodes))
    except ValueError as error:
        return f"Error: {error}"
    payload = {"profiles": results, "decision_note": "These are screening statuses, not automatic grades. Review the three most recent valid occasions and context before finalizing."}
    if response_format == "json":
        return _ajson(payload)
    lines = ["# EM course-level screening profile", ""]
    for row in results:
        lines.extend([f"## {row['construct']}", f"- **Status:** {row['screening_status']}", f"- **Valid evidence occasions:** {row['valid_n']} (NE excluded: {row['ne_n']})", f"- **Average:** {row['average'] if row['average'] is not None else '—'}", f"- **Recent valid scores:** {row['recent_scores']}", ""])
    lines.append("Instructor review is required before final reporting.")
    return "\n".join(lines)


@mcp.resource("em://habits")
def habits_resource() -> str:
    """Canonical habit definitions and assessment look-fors."""
    return _ajson(HABITS)


@mcp.resource("em://observable-behaviors")
def behaviors_resource() -> str:
    """Eight observable behavior definitions and developmental anchors."""
    return _ajson(BEHAVIORS)


@mcp.resource("em://scoring-scale")
def scoring_resource() -> str:
    """Common NE/0-3 scale and decision language."""
    return _ajson(SCORING_SCALE)


@mcp.prompt(name="review-em-evidence")
def p_review_em_evidence(habit: str, student_evidence: str) -> str:
    """Construct-aligned review of one student evidence excerpt against a Habit of EM, ending in a scored evidence episode."""
    return f"Review this student evidence for the Habit of EM '{habit}'. First call em_get_habit. Decide whether the task elicited the distinctive move; cite exact evidence; separate NE from 0; then call em_score_evidence_episode. Do not infer personality or reward AI-generated polish. Evidence: {student_evidence}"


# ─── Health check (browser-friendly, used by the Field Guide HTML) ────────────

@mcp.custom_route("/", methods=["GET"])
async def health(_request: Request) -> JSONResponse:
    return JSONResponse(
        {
            "name": "EMxAI Studio MCP Server",
            "version": "2.0.0",
            "mcp_endpoint": "/mcp",
            "tools": [
                "aias_advisor", "eml_architect", "interactive_builder_planning",
                "interactive_builder_coding", "autonomy_coach", "engagement_opener",
                "passion_connector", "prompt_optimizer", "em_list", "em_habit",
                "em_coach", "em_workflow", "em_diagnostic", "em_list_habits",
                "em_get_habit", "em_get_behavior_rubric", "em_plan_assessment",
                "em_score_evidence_episode", "em_synthesize_profile",
            ],
            "status": "ok",
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "3000"))
    mcp.run(transport="http", host="0.0.0.0", port=port)

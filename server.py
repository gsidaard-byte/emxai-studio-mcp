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
                "em_coach", "em_workflow", "em_diagnostic",
            ],
            "status": "ok",
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "3000"))
    mcp.run(transport="http", host="0.0.0.0", port=port)

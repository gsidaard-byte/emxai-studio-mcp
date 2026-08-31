"""Validated inputs and structured outputs for EM assessment tools."""

from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, populate_by_name=True)


class ResponseFormat(str, Enum):
    MARKDOWN = "markdown"
    JSON = "json"


class ListHabitsInput(StrictModel):
    category: Literal["Curiosity", "Connections", "Creating Value"] | None = Field(default=None, description="Optional 3C category filter.")
    search: str | None = Field(default=None, min_length=2, max_length=100, description="Optional case-insensitive search across habit names, themes, and evidence look-fors.")
    limit: int = Field(default=18, ge=1, le=18, description="Maximum habits to return.")
    offset: int = Field(default=0, ge=0, description="Number of matches to skip.")
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN, description="Human-readable markdown or machine-readable JSON.")


class HabitLookupInput(StrictModel):
    habit: str = Field(min_length=2, max_length=80, description="Habit name, such as Systems Thinking. Case-insensitive exact or unambiguous partial matches are accepted.")
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN, description="Human-readable markdown or machine-readable JSON.")


class BehaviorLookupInput(StrictModel):
    behavior: str = Field(min_length=3, max_length=120, description="Observable behavior name; unambiguous partial matches are accepted.")
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN, description="Human-readable markdown or machine-readable JSON.")


class AssessmentPlanInput(StrictModel):
    assignment_name: str = Field(min_length=2, max_length=160, description="Student-facing assignment name.")
    artifact_type: str = Field(min_length=2, max_length=100, description="Expected artifact, such as design memo, lab report, or in-class prototype.")
    target_habits: list[str] = Field(min_length=1, max_length=3, description="One to three habits genuinely required by the task.")
    ai_use: Literal["not_allowed", "optional", "required"] = Field(default="optional", description="Whether generative AI use is prohibited, optional, or required.")
    stakes: Literal["practice", "low", "moderate", "high"] = Field(default="low", description="Assessment stakes; high-stakes use triggers stronger corroboration guidance.")
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN, description="Human-readable markdown or machine-readable JSON.")


class EvidenceEpisodeInput(StrictModel):
    target_habit: str = Field(min_length=2, max_length=80, description="Habit being assessed.")
    elicited: bool = Field(description="Whether the task genuinely required the habit-specific intellectual move.")
    attributable_to_student: bool = Field(description="Whether the evidence can be attributed to this student rather than only a team or AI system.")
    sufficient_evidence: bool = Field(description="Whether enough product/process evidence exists to judge the move.")
    distinctive_move_attempted: bool = Field(description="Whether the student attempted the habit's distinctive move.")
    supported_by_relevant_evidence: bool = Field(description="Whether the move is supported by relevant data, sources, testing, or stakeholder evidence.")
    changed_decision_or_work: bool = Field(description="Whether the habit shaped a conclusion, revision, design, or decision.")
    addressed_limitations_or_counterevidence: bool = Field(description="Whether limitations, contradictory evidence, or credible alternatives were addressed.")
    proactive_or_adaptive_transfer: bool = Field(description="Whether the student used the move proactively/adaptively in a complex, new, or changed context and can explain transfer.")
    individual_evidence: bool = Field(default=True, description="Whether direct individual evidence is present.")
    novel_context: bool = Field(default=False, description="Whether this is a new or substantially changed context.")
    evidence_locator: str | None = Field(default=None, max_length=300, description="Page, section, cell, figure, code line, or observed moment.")
    evidence_note: str | None = Field(default=None, max_length=2000, description="Brief evidence-based rationale; do not paste an entire student submission.")
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN, description="Human-readable markdown or machine-readable JSON.")


class RatedEpisode(StrictModel):
    construct_name: str = Field(alias="construct", min_length=2, max_length=120, description="Habit or observable behavior name.")
    score: Literal["NE", 0, 1, 2, 3] = Field(description="Artifact-level rating.")
    task_type: str = Field(min_length=2, max_length=100, description="Artifact/task type used to check evidence diversity.")
    individual_evidence: bool = Field(default=True, description="Whether the episode is individually attributable.")
    novel_context: bool = Field(default=False, description="Whether the episode occurred in a new or substantially changed context.")
    sequence: int = Field(ge=1, le=1000, description="Chronological sequence number; larger values are more recent.")


class ProfileInput(StrictModel):
    episodes: list[RatedEpisode] = Field(min_length=1, max_length=100, description="Rated evidence episodes for one student; NE is retained but excluded from numeric synthesis.")
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN, description="Human-readable markdown or machine-readable JSON.")

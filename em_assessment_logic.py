"""Pure assessment logic, independent of MCP transport."""

from collections import defaultdict
from typing import Any, Iterable

from em_assessment_data import BEHAVIORS, HABITS
from em_assessment_models import EvidenceEpisodeInput, RatedEpisode


def resolve_name(query: str, choices: Iterable[str], kind: str) -> str:
    normalized = query.casefold().strip()
    choice_list = list(choices)
    exact = [name for name in choice_list if name.casefold() == normalized]
    if exact:
        return exact[0]
    partial = [name for name in choice_list if normalized in name.casefold()]
    if len(partial) == 1:
        return partial[0]
    if not partial:
        raise ValueError(f"Unknown {kind} '{query}'. Use the list tool to retrieve valid names.")
    raise ValueError(f"Ambiguous {kind} '{query}'. Matches: {', '.join(partial)}. Provide a more specific name.")


def score_episode(e: EvidenceEpisodeInput) -> dict[str, Any]:
    habit = resolve_name(e.target_habit, HABITS, "habit")
    if not e.elicited:
        score: str | int = "NE"
        rationale = "The task did not genuinely elicit the habit; absence cannot be interpreted as a low score."
        next_move = "Revise the task so the habit-specific move is necessary and identify the evidence students must leave."
    elif not e.attributable_to_student:
        score = "NE"
        rationale = "The evidence is not individually attributable to the student."
        next_move = "Add an individual annotation, process trace, brief defense, or contribution record."
    elif not e.sufficient_evidence:
        score = "NE"
        rationale = "The evidence bundle is insufficient to judge the student's reasoning."
        next_move = "Collect a product locator plus a process explanation or verification trace."
    elif not e.distinctive_move_attempted:
        score = 0
        rationale = "A valid opportunity was present, but the habit's distinctive move is not evident."
        next_move = f"Require the student to demonstrate: {HABITS[habit]['core_theme']}"
    elif not (e.supported_by_relevant_evidence and e.changed_decision_or_work):
        score = 1
        rationale = "The distinctive move is attempted, but support or consequence for the work is incomplete."
        missing = "relevant support" if not e.supported_by_relevant_evidence else "a documented effect on the decision or revision"
        next_move = f"Add {missing} and point to where it changes the work."
    elif not (e.addressed_limitations_or_counterevidence and e.proactive_or_adaptive_transfer):
        score = 2
        rationale = "The move is intentional, supported, and consequential, but proficient-level limitation handling and transfer are not both established."
        missing = []
        if not e.addressed_limitations_or_counterevidence:
            missing.append("address a limitation or credible counterevidence")
        if not e.proactive_or_adaptive_transfer:
            missing.append("explain proactive/adaptive use in a complex, new, or changed context")
        next_move = "To advance, " + " and ".join(missing) + "."
    else:
        score = 3
        rationale = "The evidence supports proactive, adaptive application with limitations/counterevidence and transfer."
        next_move = "Seek another occasion in a different task type before making a stable course-level claim."

    confidence = "high" if e.individual_evidence and e.evidence_locator and e.sufficient_evidence else ("medium" if e.attributable_to_student and e.sufficient_evidence else "low")
    return {"habit": habit, "score": score, "level": {"NE": "Not elicited / insufficient", 0: "Not yet evident", 1: "Developing", 2: "Advancing", 3: "Proficient"}[score], "confidence": confidence, "rationale": rationale, "next_move": next_move, "evidence_locator": e.evidence_locator, "individual_evidence": e.individual_evidence, "novel_context": e.novel_context}


def synthesize_profile(episodes: list[RatedEpisode]) -> list[dict[str, Any]]:
    grouped: dict[str, list[RatedEpisode]] = defaultdict(list)
    for episode in episodes:
        construct = resolve_name(episode.construct_name, list(HABITS) + list(BEHAVIORS), "construct")
        grouped[construct].append(episode)

    results: list[dict[str, Any]] = []
    for construct, items in grouped.items():
        valid = [item for item in items if item.score != "NE"]
        numeric = [int(item.score) for item in valid]
        score3 = [item for item in valid if item.score == 3]
        average = round(sum(numeric) / len(numeric), 2) if numeric else None
        task_types = {item.task_type.casefold() for item in valid}
        proficient = len(valid) >= 3 and len(score3) >= 2 and len(task_types) >= 2 and any(x.individual_evidence for x in score3) and any(x.novel_context for x in score3)
        if len(valid) < 2:
            status = "Insufficient evidence"
        elif proficient:
            status = "Proficient candidate"
        elif average is not None and average >= 2:
            status = "Advancing"
        elif average is not None and average >= 1:
            status = "Developing"
        else:
            status = "Not yet evident"
        recent = sorted(valid, key=lambda item: item.sequence, reverse=True)[:3]
        results.append({"construct": construct, "valid_n": len(valid), "ne_n": len(items) - len(valid), "average": average, "score_3_n": len(score3), "individual_3_n": sum(x.individual_evidence for x in score3), "novel_3_n": sum(x.novel_context for x in score3), "task_type_n": len(task_types), "screening_status": status, "recent_scores": [x.score for x in recent], "requires_instructor_review": True})
    return sorted(results, key=lambda row: row["construct"])

# screens/questionnaire.py
import streamlit as st
from typing import Dict, List

from tasks import get_filtered_tasks, group_by_pillar
from utils.ui import (
    step_header, learn_popover, safety_note, section_notes, tiny_hint, definition_box
)

# --------- Pillar labels + quick “set the scene” lines (unchanged vibe) ---------
PILLAR_LABELS: Dict[str, str] = {
    "anticipation": "Anticipating (noticing what’s needed soon)",
    "identification": "Identifying (what exactly needs doing)",
    "decision": "Deciding (who/when/how it gets done)",
    "monitoring": "Monitoring (following up & checking)",
    "emotional": "Emotional load (worrying, calming, caring)",
}

PILLAR_HINTS: Dict[str, str] = {
    "anticipation": "Looking ahead so things don’t fall through the cracks.",
    "identification": "Spelling out the parts of a job so it’s do-able.",
    "decision": "Choosing who, when, and how — and coordinating moving pieces.",
    "monitoring": "Keeping track and nudging so things actually happen.",
    "emotional": "Caring, soothing, remembering what matters to people.",
}

# --------- Slider labels + help (tweaked wording, same layout) ---------
RESP_LABEL = "Responsibility (0 = Partner A • 100 = Partner B)"
BURDEN_LABEL = "Burden (1–5) — how taxing it feels to the person who mostly leads it"
FAIRNESS_LABEL = "Fairness (1–5) — how fair this feels to both of you today"

RESP_HELP = (
    "Who mainly owns the noticing/planning/follow-ups for this right now? "
    "0 = Partner A, 100 = Partner B."
)
BURDEN_HELP = (
    "Rate the mental effort for the person who mostly leads this task at the moment. "
    "If you see it differently, jot both views in Notes — that’s useful data."
)
FAIRNESS_HELP = "Your shared sense of fairness today (not in theory). Low = doesn’t feel fair."

# --------- One task block (keeps your context-first card + same slider layout) ---------
def _task_response_block(task, default=None):
    """
    Renders one task with:
      - a context/definition card (broad explanation first)
      - responsibility / burden / fairness / N/A (same column layout as before)
      - optional example only if task.example exists
    Returns a dict to store in st.session_state.responses.
    """
    st.subheader(task.name)

    # Broad, guiding context (kept — small wording polish).
    definition = getattr(task, "definition", None) or (
        "Consider the whole invisible side: who notices, plans, coordinates and follows up — "
        "not just the visible doing."
    )
    what_counts = getattr(task, "what_counts", None)
    note = getattr(task, "note", None)
    example = getattr(task, "example", None)  # only show if it truly adds clarity

    definition_box(
        title=f"What this covers: {task.name}",
        definition=definition,
        what_counts=what_counts,
        note=note,
        example=example,         # will render only if provided
    )

    # Keep EXACT layout you liked: 3 sliders + N/A in a 2/2/2/1 grid.
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    with col1:
        responsibility = st.slider(
            RESP_LABEL,
            min_value=0, max_value=100, value=(default or {}).get("responsibility", 50),
            help=RESP_HELP,
            key=f"{task.id}_resp",
        )
        tiny_hint("If Partner A mostly leads, ~20–30. If Partner B mostly leads, ~70–80.")
    with col2:
        burden = st.slider(
            BURDEN_LABEL,
            min_value=1, max_value=5, value=(default or {}).get("burden", 3),
            help=BURDEN_HELP,
            key=f"{task.id}_burden",
        )
    with col3:
        fairness = st.slider(
            FAIRNESS_LABEL,
            min_value=1, max_value=5, value=(default or {}).get("fairness", 3),
            help=FAIRNESS_HELP,
            key=f"{task.id}_fair",
        )
    with col4:
        not_applicable = st.checkbox(
            "N/A",
            value=(default or {}).get("not_applicable", False),
            key=f"{task.id}_na",
        )

    return {
        "task_id": task.id,
        "responsibility": responsibility,
        "burden": burden,
        "fairness": fairness,
        "not_applicable": not_applicable,
    }

# --------- Main screen (chunked by pillar; same flow, gentler copy) ---------
def screen_questionnaire():
    # Persist chunked flow
    st.session_state.setdefault("q_pillar_index", 0)
    st.session_state.setdefault("responses", [])
    st.session_state.setdefault("notes_by_section", {})

    # Context → which tasks to show
    children = st.session_state.get("children", 0)
    household_type = st.session_state.get("household_type", "couple")
    is_emp_me = st.session_state.get("is_employed_me", True)
    is_emp_partner = st.session_state.get("is_employed_partner", True) if household_type == "couple" else False
    both_employed = (is_emp_me and is_emp_partner) if household_type == "couple" else is_emp_me

    tasks = get_filtered_tasks(children, both_employed)
    groups = group_by_pillar(tasks)

    # Fixed pillar order first, then any extras
    ordered = ["anticipation", "identification", "decision", "monitoring", "emotional"]
    pillar_keys: List[str] = [k for k in ordered if k in groups] + [k for k in groups.keys() if k not in ordered]

    # Header + progress + helpers (unchanged structure)
    total_sections = len(pillar_keys)
    i = st.session_state.q_pillar_index
    progress = int((i / max(total_sections, 1)) * 100)

    step_header(
        "Household Questionnaire",
        "Talk it through together. Take your time. You can pause and return any time.",
        progress=progress,
    )
    learn_popover()
    safety_note()

    if not pillar_keys:
        st.warning("No tasks available for your context. Try adjusting Setup.")
        if st.button("← Back to Setup"):
            st.session_state.stage = "setup"
        return

    # Current section
    pillar = pillar_keys[i]
    label = PILLAR_LABELS.get(pillar, pillar.capitalize())
    st.markdown(f"#### {label}")
    if PILLAR_HINTS.get(pillar):
        st.caption(PILLAR_HINTS[pillar])

    # Render tasks in this section (preserving previous answers)
    section_tasks = groups[pillar]
    updated = []
    for t in section_tasks:
        prev = next((r for r in st.session_state.responses if r["task_id"] == t.id), None)
        resp = _task_response_block(t, default=prev)
        updated.append(resp)
        st.divider()

    # Merge updates into responses
    other = [r for r in st.session_state.responses if r["task_id"] not in {t.id for t in section_tasks}]
    st.session_state.responses = other + updated

    # Notes for this section (kept; same spot)
    note_key = f"notes_{pillar}"
    existing_note = st.session_state.notes_by_section.get(pillar, "")
    st.session_state.notes_by_section[pillar] = section_notes(
        key=note_key,
        placeholder="Different views? What felt heavy? Any small idea to try this week?",
    ) or existing_note

    # Nav controls (unchanged behavior)
    colA, colB, colC = st.columns([1, 1, 2])
    with colA:
        if st.button("⬅️ Back", disabled=(i == 0)):
            if i > 0:
                st.session_state.q_pillar_index = i - 1
                st.rerun()
    with colB:
        if i < total_sections - 1:
            if st.button("Next ➡️"):
                st.session_state.q_pillar_index = i + 1
                st.rerun()
        else:
            if st.button("Finish & See Results"):
                if not st.session_state.responses:
                    st.warning("Please answer at least one task first.")
                else:
                    st.session_state.stage = "results"

    # Secondary actions
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏠 Home"):
            st.session_state.stage = "home"
    with c2:
        if st.button("📘 Learn more"):
            st.session_state.stage = "learn_more"

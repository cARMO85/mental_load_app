# screens/questionnaire.py
import streamlit as st
from typing import Dict, List

from tasks import get_filtered_tasks, group_by_pillar
from utils.ui import step_header, learn_popover, safety_note

# --------- Pillar context (conversational, research-grounded) ---------
PILLAR_INTRO: Dict[str, Dict[str, str]] = {
    "anticipation": {
        "title": "🔮 Anticipation: Thinking Ahead",
        "research": "Research identifies anticipation as one of four core dimensions of household cognitive labour (Daminger, 2019). This involves thinking ahead to what will be needed, often before anyone else notices.",
        "what_it_means": "This is the mental work of noticing what will be needed soon and planning for it before it becomes urgent.",
        "example": "Remembering the school form is due Friday, noticing you're low on milk, planning meals for the week."
    },
    "identification": {
        "title": "👁️ Identification: Noticing What Needs Doing",
        "research": "Identification refers to recognising what needs to be done and breaking it down into actionable tasks (Daminger, 2019). Studies show this 'noticing work' is often gendered and invisible to those not doing it.",
        "what_it_means": "This is the work of seeing what needs to happen and defining the actual tasks involved.",
        "example": "Spotting that the bathroom needs cleaning, recognising a child needs new shoes, seeing the light bulb is out."
    },
    "decision": {
        "title": "🤔 Decision-Making: Choosing How & When",
        "research": "Decision-making includes researching options, weighing trade-offs, and coordinating schedules (Daminger, 2019). This 'project management' work is often invisible yet cognitively demanding.",
        "what_it_means": "This is about making choices for the household - which doctor, what gift, how to handle a situation.",
        "example": "Choosing which childcare, deciding what to cook, picking a birthday gift, scheduling appointments."
    },
    "monitoring": {
        "title": "📋 Monitoring: Following Up & Tracking",
        "research": "Monitoring involves tracking whether tasks are completed and following up when needed (Daminger, 2019). Research emphasises this as a particularly invisible form of cognitive labour that can remain stressful even when tasks are delegated.",
        "what_it_means": "This is the work of tracking progress, remembering deadlines, and ensuring things don't fall through the cracks.",
        "example": "Checking if forms got submitted, following up on RSVPs, tracking when bills are due, reminding about tasks."
    },
    "emotional": {
        "title": "💝 Emotional Labour: The Caring Work",
        "research": "Emotional labour includes managing feelings, maintaining relationships, and creating household harmony (Dean, Churchill and Ruppanner, 2022). Research now recognises this as cognitive work, not simply 'being nice'.",
        "what_it_means": "This is about noticing and responding to others' feelings, maintaining family relationships, and creating a positive home environment.",
        "example": "Soothing upset children, remembering to call grandma, managing conflicts, creating special moments."
    }
}

# --------- Helper for task display ---------
def _render_task_card(task, default=None):
    """Simplified, conversation-focused task card"""
    
    # Task name as header
    st.markdown(f"### {task.name}")
    
    # Brief definition (not overwhelming)
    if task.definition:
        st.markdown(f"*{task.definition}*")
    
    # What counts (in a compact format)
    if task.what_counts:
        with st.expander("💡 What this includes"):
            for item in task.what_counts:
                st.markdown(f"• {item}")
    
    # Example if helpful
    if task.example:
        st.info(f"**Example:** {task.example}")
    
    st.markdown("")  # Spacing
    
    # Three questions, presented more conversationally
    st.markdown("**Answer these three questions together:**")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # 1. Responsibility
        st.markdown("**1. Who mainly handles this right now?**")
        responsibility = st.slider(
            "Slide toward the person who carries most of this mental work",
            min_value=0, 
            max_value=100, 
            value=(default or {}).get("responsibility", 50),
            key=f"{task.id}_resp",
            help="0 = Partner A does all of it, 50 = shared equally, 100 = Partner B does all of it",
            label_visibility="collapsed"
        )
        
        # Visual label
        if responsibility < 30:
            st.caption("← Partner A handles most of this")
        elif responsibility > 70:
            st.caption("Partner B handles most of this →")
        else:
            st.caption("↔️ Shared fairly evenly")
        
        st.markdown("")
        
        # 2. Burden
        st.markdown("**2. How mentally draining is this task?**")
        st.caption("For whoever mainly handles it - how heavy does it feel?")
        burden = st.slider(
            "Burden level",
            min_value=1, 
            max_value=5, 
            value=(default or {}).get("burden", 3),
            key=f"{task.id}_burden",
            help="1 = Easy/light, 5 = Very draining",
            label_visibility="collapsed"
        )
        
        # Visual feedback
        burden_labels = {1: "😌 Light", 2: "🙂 Manageable", 3: "😐 Moderate", 4: "😓 Heavy", 5: "😰 Very draining"}
        st.caption(burden_labels.get(burden, ""))
        
        st.markdown("")
        
        # 3. Fairness
        st.markdown("**3. Does this feel fair right now?**")
        st.caption("Your gut feeling - not what 'should' be fair, but how it actually feels")
        fairness = st.slider(
            "Fairness feeling",
            min_value=1, 
            max_value=5, 
            value=(default or {}).get("fairness", 3),
            key=f"{task.id}_fair",
            help="1 = Very unfair, 5 = Completely fair",
            label_visibility="collapsed"
        )
        
        # Visual feedback
        fairness_labels = {1: "😞 Feels unfair", 2: "😕 Not quite fair", 3: "😐 Neutral", 4: "🙂 Pretty fair", 5: "😊 Feels fair"}
        st.caption(fairness_labels.get(fairness, ""))
    
    with col2:
        st.markdown("**Not relevant?**")
        not_applicable = st.checkbox(
            "Skip this task",
            value=(default or {}).get("not_applicable", False),
            key=f"{task.id}_na",
            help="Check this if this task doesn't apply to your household"
        )
    
    return {
        "task_id": task.id,
        "responsibility": responsibility,
        "burden": burden,
        "fairness": fairness,
        "not_applicable": not_applicable,
    }


# --------- Main screen ---------
def screen_questionnaire():
    # Initialize state
    st.session_state.setdefault("q_pillar_index", 0)
    st.session_state.setdefault("responses", [])
    st.session_state.setdefault("notes_by_section", {})

    # Get context
    children = st.session_state.get("children", 0)
    household_type = st.session_state.get("household_type", "couple")
    is_emp_me = st.session_state.get("is_employed_me", True)
    is_emp_partner = st.session_state.get("is_employed_partner", True) if household_type == "couple" else False
    both_employed = (is_emp_me and is_emp_partner) if household_type == "couple" else is_emp_me

    tasks = get_filtered_tasks(children, both_employed)
    groups = group_by_pillar(tasks)

    # Pillar order
    ordered = ["anticipation", "identification", "decision", "monitoring", "emotional"]
    pillar_keys: List[str] = [k for k in ordered if k in groups] + [k for k in groups.keys() if k not in ordered]

    # Progress
    total_sections = len(pillar_keys)
    i = st.session_state.q_pillar_index
    progress = int((i / max(total_sections, 1)) * 100)

    # Header
    st.title("📝 Household Questionnaire")
    st.caption(f"Section {i+1} of {total_sections} • Talk it through together as you go")
    st.progress(progress)
    
    # Top navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.stage = "home"
            st.rerun()
    with col2:
        learn_popover()
    with col3:
        if st.button("💾 Save & Exit", use_container_width=True):
            st.info("Your progress is saved in this session. You can return anytime before closing the browser.")
            st.session_state.stage = "home"
            st.rerun()

    st.markdown("---")

    if not pillar_keys:
        st.warning("No tasks available for your context. Try adjusting Setup.")
        if st.button("← Back to Setup"):
            st.session_state.stage = "setup"
            st.rerun()
        return

    # Current pillar
    pillar = pillar_keys[i]
    pillar_info = PILLAR_INTRO.get(pillar, {})
    
    # Pillar introduction (research-grounded)
    st.markdown(f"## {pillar_info.get('title', pillar.capitalize())}")
    
    with st.expander("🎓 Why we're asking about this", expanded=(i == 0)):
        st.markdown(f"**What research shows:** {pillar_info.get('research', '')}")
        st.markdown(f"**What it means:** {pillar_info.get('what_it_means', '')}")
        st.markdown(f"**Example:** {pillar_info.get('example', '')}")
    
    st.markdown("---")
    
    # Gentle reminder
    if i == 0:
        st.info("💙 **Remember:** There are no right answers. Just your honest experience right now. Take breaks if you need them.")
    
    # Tasks in this section
    section_tasks = groups[pillar]
    st.markdown(f"### {len(section_tasks)} tasks in this section")
    st.caption("For each task, answer together. It's okay to disagree - note different perspectives at the bottom.")
    
    st.markdown("---")
    
    # Render tasks
    updated = []
    for idx, t in enumerate(section_tasks, 1):
        st.markdown(f"#### Task {idx} of {len(section_tasks)}")
        prev = next((r for r in st.session_state.responses if r["task_id"] == t.id), None)
        resp = _render_task_card(t, default=prev)
        updated.append(resp)
        st.markdown("---")

    # Merge updates
    other = [r for r in st.session_state.responses if r["task_id"] not in {t.id for t in section_tasks}]
    st.session_state.responses = other + updated

    # Notes for this section
    st.markdown("### 📝 Notes for this section (optional)")
    st.caption("Different perspectives? Something that felt particularly heavy? An idea to try? Jot it down.")
    
    note_key = f"notes_{pillar}"
    existing_note = st.session_state.notes_by_section.get(pillar, "")
    
    new_note = st.text_area(
        "Your notes:",
        value=existing_note,
        height=100,
        placeholder="E.g., 'Partner A didn't realize Partner B was tracking all the meal planning' or 'We both want to try meal-prepping on Sundays'",
        key=note_key,
        help="These notes stay in your browser session and can be exported with your results."
    )
    st.session_state.notes_by_section[pillar] = new_note

    # Navigation
    st.markdown("---")
    st.markdown("### Ready to continue?")
    
    colA, colB, colC = st.columns([1, 1, 2])
    with colA:
        if st.button("⬅️ Previous Section", disabled=(i == 0), use_container_width=True):
            if i > 0:
                st.session_state.q_pillar_index = i - 1
                st.rerun()
    with colB:
        if i < total_sections - 1:
            if st.button("Next Section ➡️", use_container_width=True, type="primary"):
                st.session_state.q_pillar_index = i + 1
                st.rerun()
        else:
            if st.button("See Results →", use_container_width=True, type="primary"):
                if not st.session_state.responses:
                    st.warning("Please answer at least one task first.")
                else:
                    st.session_state.results_prep_seen = False  # Force showing prep screen
                    st.session_state.stage = "results"
                    st.rerun()
    
    with colC:
        # Progress indicator
        completed = sum(1 for r in st.session_state.responses if not r.get("not_applicable", False))
        total_tasks = len(tasks)
        st.caption(f"📊 Progress: {completed} of {total_tasks} tasks completed")
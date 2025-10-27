# screens/questionnaire.py
import streamlit as st
from typing import Dict, List
from datetime import datetime

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
        # ========== QUESTION 1: RESPONSIBILITY (UNCHANGED) ==========
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
        
        # ========== QUESTION 2: BURDEN (NEW EXPLICIT WORDING) ==========
        st.markdown("**2. How mentally draining is this task?**")
        
        # Clarify whose burden to rate: the person who does most, or the typical experience if shared
        st.caption(
            "Please rate how mentally draining this task is for the person who does MOST of it (based on the slider). "
            "If you share it evenly, rate the typical experience or the average burden."
        )
        
        # Add visual guide based on responsibility slider
        if responsibility < 40:
            burden_caption = "Rate the burden experienced by Partner A (who handles most of this)"
        elif responsibility > 60:
            burden_caption = "Rate the burden experienced by Partner B (who handles most of this)"
        else:
            burden_caption = "Rate the typical/average burden when this is shared fairly evenly"
        
        st.caption(f"💭 *{burden_caption}*")
        
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
        burden_labels = {
            1: "😌 Light - barely think about it", 
            2: "🙂 Manageable - takes some mental energy", 
            3: "😐 Moderate - noticeable mental effort", 
            4: "😓 Heavy - quite draining", 
            5: "😰 Very draining - exhausting to manage"
        }
        st.caption(burden_labels.get(burden, ""))
        
        st.markdown("")
        
        # ========== QUESTION 3: FAIRNESS (NEW EXPLICIT WORDING) ==========
        st.markdown("**3. Does this current division feel fair to both of you?**")
        
        # NEW: Make fairness explicit and clarify what we're asking
        st.caption(
            "Even if one partner does more, it can still feel fair if both agree it makes sense. "
            "Rate how fair this current arrangement feels."
        )
        
        fairness = st.slider(
            "Fairness level",
            min_value=1, 
            max_value=5, 
            value=(default or {}).get("fairness", 3),
            key=f"{task.id}_fair",
            help="1 = Very unfair, 5 = Very fair",
            label_visibility="collapsed"
        )
        
        # Visual feedback with examples
        fairness_labels = {
            1: "😠 Very unfair - this really bothers us",
            2: "😕 Somewhat unfair - could be better",
            3: "😐 Neutral - it's okay for now",
            4: "🙂 Mostly fair - we're both comfortable with this",
            5: "😊 Very fair - we both feel good about how this is split"
        }
        st.caption(fairness_labels.get(fairness, ""))
        
        # Add helpful context
        st.caption(
            "💡 *Example: Partner A might do 80% of meal planning (high responsibility) "
            "but both partners think it's fair because Partner A enjoys it and Partner B "
            "handles other tasks. That would be rated 4-5 in fairness.*"
        )
        
        st.markdown("")
    
    with col2:
        # Not applicable checkbox
        not_applicable = st.checkbox(
            "This doesn't apply to us",
            value=(default or {}).get("not_applicable", False),
            key=f"{task.id}_na",
            help="Check this if this task is not relevant to your household"
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
    
    # Track start time (use .get to avoid KeyError if state wasn't initialised)
    if st.session_state.get('questionnaire_start_time') is None:
        st.session_state['questionnaire_start_time'] = datetime.now()

    # Get context
    children = st.session_state.get("children", 0)
    household_type = st.session_state.get("household_type", "couple")
    is_emp_me = st.session_state.get("is_employed_me", True)
    is_emp_partner = st.session_state.get("is_employed_partner", True) if household_type == "couple" else False
    both_employed = (is_emp_me and is_emp_partner) if household_type == "couple" else is_emp_me

    # Context flags (set in the Setup screen)
    has_pets = st.session_state.get('has_pets', False)
    has_vehicle = st.session_state.get('has_vehicle', False)

    tasks = get_filtered_tasks(children, both_employed, has_pets, has_vehicle)
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
            st.info("Your progress is saved in this session. You can return any time before closing the browser.")
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
        placeholder="E.g., 'Partner A didn't realise Partner B was tracking all the meal planning' or 'We both want to try meal-prepping on Sundays'",
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
                    # Calculate completion time
                    start = st.session_state.get('questionnaire_start_time')
                    if start:
                        completion_time = (datetime.now() - start).total_seconds()
                        st.session_state['completion_time_seconds'] = completion_time
                    
                    st.session_state.results_prep_seen = False
                    st.session_state.stage = "results"
                    st.rerun()
    
    with colC:
        # Progress indicator
        completed = sum(1 for r in st.session_state.responses if not r.get("not_applicable", False))
        total_tasks = len(tasks)
        st.caption(f"📊 Progress: {completed} of {total_tasks} tasks completed")
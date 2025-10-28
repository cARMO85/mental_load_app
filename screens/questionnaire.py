# screens/questionnaire.py
import streamlit as st
from typing import Dict, List

from tasks import get_filtered_tasks, group_by_pillar

# --------- Simple pillar headers ---------
PILLAR_INFO: Dict[str, Dict[str, str]] = {
    "anticipation": {
        "emoji": "🔮",
        "title": "Thinking Ahead",
        "description": "Noticing what will be needed soon and planning for it",
        "example": "Remembering the school form is due, noticing you're low on milk, planning meals"
    },
    "identification": {
        "emoji": "👁️",
        "title": "Noticing What Needs Doing",
        "description": "Spotting what needs to happen and defining the tasks",
        "example": "Seeing the bathroom needs cleaning, recognising a child needs new shoes"
    },
    "decision": {
        "emoji": "🤔",
        "title": "Choosing How & When",
        "description": "Making household choices and coordinating schedules",
        "example": "Deciding what to cook, choosing childcare, picking gifts, scheduling appointments"
    },
    "monitoring": {
        "emoji": "📋",
        "title": "Following Up & Tracking",
        "description": "Keeping track of progress and making sure nothing falls through the cracks",
        "example": "Checking if forms got submitted, following up on RSVPs, tracking bill due dates"
    },
    "emotional": {
        "emoji": "💝",
        "title": "The Caring Work",
        "description": "Noticing and responding to feelings, maintaining relationships",
        "example": "Soothing upset children, remembering to call grandma, managing conflicts"
    }
}

PILLAR_ORDER = ["anticipation", "identification", "decision", "monitoring", "emotional"]

def screen_questionnaire():
    """Simple questionnaire - all sections visible, just scroll through"""
    # Top-right Home button
    top_col1, top_col2 = st.columns([6, 1])
    with top_col2:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.stage = "home"
            st.rerun()  
    # Header
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 style='font-size: 2rem; font-weight: 700; margin-bottom: 8px;'>Your household tasks</h1>
        <p style='font-size: 1.1rem; color: #64748b;'>Answer these together • Scroll through all sections • Take your time</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick instructions
    with st.expander("📖 How to use this questionnaire"):
        st.markdown("""
        **For each task, answer three questions:**
        1. **Who mainly handles this?** (Slider: Partner A ← → Partner B)
        2. **How mentally draining is this?** (1 = light, 5 = very draining)
        3. **Does this feel fair?** (1 = very unfair, 5 = very fair)
        
        **Tips:**
        - If a task doesn't apply to you, tick "Not applicable"
        - Think about the *mental work* (planning, remembering), not just the physical doing
        - Be honest about how things are, not how you wish they were
        - Take breaks if you need to
        """)
    
    st.info("💭 **Remember:** No right or wrong answers. This is about understanding, not blame.")
    st.markdown("---")
    
    # Get filtered tasks
    children = st.session_state.get("children", 0)
    both_employed = st.session_state.get("is_employed_me", True) and st.session_state.get("is_employed_partner", True)
    has_pets = st.session_state.get("has_pets", False)
    has_vehicle = st.session_state.get("has_vehicle", False)
    tasks = get_filtered_tasks(children, both_employed, has_pets, has_vehicle)
    pillars = group_by_pillar(tasks)
    
    # Initialize responses dict
    if "responses_dict" not in st.session_state:
        st.session_state.responses_dict = {}
    
    # Progress at top
    total_tasks = len(tasks)
    completed_tasks = len(st.session_state.responses_dict)
    
    if total_tasks > 0:
        progress_pct = (completed_tasks / total_tasks) * 100
        col1, col2 = st.columns([3, 1])
        with col1:
            st.progress(progress_pct / 100)
        with col2:
            st.caption(f"**{completed_tasks} / {total_tasks}**")
    
    st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
    
    # Loop through pillars - all visible
    for pillar_key in PILLAR_ORDER:
        if pillar_key not in pillars:
            continue
        
        info = PILLAR_INFO[pillar_key]
        pillar_tasks = pillars[pillar_key]
        
        # Section header - simple and clear
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%); 
                    border-left: 5px solid #6366f1; padding: 20px; border-radius: 12px; margin: 40px 0 25px 0;'>
            <h2 style='margin: 0 0 8px 0; font-size: 1.6rem;'>
                {info['emoji']} {info['title']}
            </h2>
            <p style='margin: 0 0 10px 0; color: #475569; font-size: 1.05rem;'>
                {info['description']}
            </p>
            <p style='margin: 0; color: #64748b; font-size: 0.95rem;'>
                <strong>Examples:</strong> {info['example']}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Render each task
        for task in pillar_tasks:
            render_task(task)
            st.markdown("---")
        
        # Optional section notes
        st.markdown("##### 📝 Notes on this section (optional)")
        notes_key = f"notes_{pillar_key}"
        if "notes_by_section" not in st.session_state:
            st.session_state.notes_by_section = {}
        
        st.session_state.notes_by_section[pillar_key] = st.text_area(
            "Section notes",
            value=st.session_state.notes_by_section.get(pillar_key, ""),
            height=70,
            placeholder="Any thoughts or observations about this section...",
            key=notes_key,
            label_visibility="collapsed"
        )
    
    # Convert dict to list for compatibility
    st.session_state.responses = list(st.session_state.responses_dict.values())
    
    # Bottom navigation
    st.markdown("<div style='margin: 50px 0 30px 0;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Check how many completed
    actual_completed = sum(1 for r in st.session_state.responses_dict.values() 
                          if not r.get("not_applicable", False))
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("← Back to setup", use_container_width=True):
            st.session_state.stage = "setup"
            st.rerun()
    
    with col2:
        if actual_completed < 5:
            st.button(
                "See results →", 
                type="primary", 
                disabled=True,
                use_container_width=True
            )
            st.caption(f"⚠️ Please answer at least 5 tasks ({actual_completed}/5)")
        else:
            if st.button("See results →", type="primary", use_container_width=True):
                st.session_state.stage = "results"
                st.rerun()
            st.caption(f"✅ {actual_completed} tasks answered")


def render_task(task):
    """Render a single task with its three questions"""
    
    # Get existing response
    existing = st.session_state.responses_dict.get(task.id, {})
    
    # Task header
    st.markdown(f"### {task.name}")
    
    if task.definition:
        st.caption(task.definition)
    
    # Optional details
    if task.what_counts or task.example:
        with st.expander("💡 What counts?"):
            if task.what_counts:
                for item in task.what_counts:
                    st.write(f"• {item}")
            if task.example:
                st.info(f"**Example:** {task.example}")
    
    # Create columns for main questions and N/A checkbox
    col_main, col_na = st.columns([4, 1])
    
    with col_main:
        # Question 1: Responsibility
        st.markdown("**Who mainly handles this?**")
        st.caption("Slide towards Partner A or Partner B to indicate who takes primary responsibility for this task.")
        responsibility = st.slider(
            "Responsibility",
            min_value=0, 
            max_value=100, 
            value=existing.get("responsibility", 50),
            key=f"{task.id}_resp",
            label_visibility="collapsed"
        )
        
        # Feedback
        if responsibility < 30:
            st.caption("← Mostly Partner A")
        elif responsibility > 70:
            st.caption("Mostly Partner B →")
        else:
            st.caption("↔️ Shared fairly equally")
        
        st.markdown("")
        
        # Question 2: Burden
        st.markdown("**How mentally draining is this?**")
        st.caption("Even if a task seems small, it can still feel mentally or emotionally tiring — this question captures that sense of strain.")
        burden = st.slider(
            "Mental burden",
            min_value=1, 
            max_value=5, 
            value=existing.get("burden", 3),
            key=f"{task.id}_burden",
            format="%d",
            label_visibility="collapsed"
        )
        
        burden_emoji = {1: "😌", 2: "🙂", 3: "😐", 4: "😓", 5: "😰"}
        burden_text = {1: "Very light", 2: "Manageable", 3: "Moderate", 4: "Heavy", 5: "Very draining"}
        st.caption(f"{burden_emoji.get(burden, '')} {burden_text.get(burden, '')}")
        
        st.markdown("")
        
        # Question 3: Fairness
        st.markdown("**Does this feel fair?**")
        st.caption("Sometimes one person does more, but both partners still feel the split is fair — that’s not a problem. This is about how fair it feels, not whether it’s equal.")
        fairness = st.slider(
            "Fairness",
            min_value=1, 
            max_value=5, 
            value=existing.get("fairness", 3),
            key=f"{task.id}_fair",
            format="%d",
            label_visibility="collapsed"
        )
        
        fairness_emoji = {1: "😟", 2: "😕", 3: "😐", 4: "🙂", 5: "😊"}
        fairness_text = {1: "Very unfair", 2: "Somewhat unfair", 3: "Neutral", 4: "Mostly fair", 5: "Very fair"}
        st.caption(f"{fairness_emoji.get(fairness, '')} {fairness_text.get(fairness, '')}")
    
    with col_na:
        st.markdown("**N/A?**")
        not_applicable = st.checkbox(
            "Not applicable",
            value=existing.get("not_applicable", False),
            key=f"{task.id}_na",
            label_visibility="collapsed"
        )
    
    # Save response if changed from defaults
    has_changed = (
        existing  # Already exists
        or not_applicable  # N/A checked
        or responsibility != 50  # Moved
        or burden != 3  # Moved
        or fairness != 3  # Moved
    )
    
    if has_changed:
        st.session_state.responses_dict[task.id] = {
            "task_id": task.id,
            "responsibility": responsibility,
            "burden": burden,
            "fairness": fairness,
            "not_applicable": not_applicable,
        }
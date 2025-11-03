# screens/questionnaire.py
import streamlit as st
from typing import Dict, List

from tasks import get_filtered_tasks, group_by_pillar
from components.navigation import render_navigation

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
    """Simple questionnaire with navigation"""
    
    # NAVIGATION HEADER
    render_navigation(
        show_back=True,
        back_stage="setup",
        back_label="← Back to setup",
        show_home=True,
        show_restart=False,
        page_title="Questionnaire"
    )
    
    # Header
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 style='font-size: 2rem; font-weight: 700; margin-bottom: 8px;'>Your household tasks</h1>
        <p style='font-size: 1.1rem; color: #64748b;'>Answer these together • Take your time</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick instructions
    with st.expander("📖 How to use this questionnaire"):
        st.markdown("""
        **For each task, answer three questions:**
        1. **Who mainly handles this?** (Slider: Partner A ← → Partner B)
           - A coloured bar below shows which side you're on
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
        
        # Section header
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
    
    # Bottom navigation - ONLY FORWARD BUTTON
    st.markdown("<div style='margin: 50px 0 30px 0;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Check how many completed
    actual_completed = sum(1 for r in st.session_state.responses_dict.values() 
                          if not r.get("not_applicable", False))
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
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


# Callback functions to update state
def update_responsibility(task_id):
    """Update responsibility when slider changes"""
    value = st.session_state[f"{task_id}_resp"]
    if task_id not in st.session_state.responses_dict:
        st.session_state.responses_dict[task_id] = {
            "task_id": task_id,
            "responsibility": 50,
            "burden": 3,
            "fairness": 3,
            "not_applicable": False,
        }
    st.session_state.responses_dict[task_id]["responsibility"] = value


def update_burden(task_id):
    """Update burden when slider changes"""
    value = st.session_state[f"{task_id}_burden"]
    if task_id not in st.session_state.responses_dict:
        st.session_state.responses_dict[task_id] = {
            "task_id": task_id,
            "responsibility": 50,
            "burden": 3,
            "fairness": 3,
            "not_applicable": False,
        }
    st.session_state.responses_dict[task_id]["burden"] = value


def update_fairness(task_id):
    """Update fairness when slider changes"""
    value = st.session_state[f"{task_id}_fair"]
    if task_id not in st.session_state.responses_dict:
        st.session_state.responses_dict[task_id] = {
            "task_id": task_id,
            "responsibility": 50,
            "burden": 3,
            "fairness": 3,
            "not_applicable": False,
        }
    st.session_state.responses_dict[task_id]["fairness"] = value


def update_not_applicable(task_id):
    """Update N/A when checkbox changes"""
    value = st.session_state[f"{task_id}_na"]
    if task_id not in st.session_state.responses_dict:
        st.session_state.responses_dict[task_id] = {
            "task_id": task_id,
            "responsibility": 50,
            "burden": 3,
            "fairness": 3,
            "not_applicable": False,
        }
    st.session_state.responses_dict[task_id]["not_applicable"] = value


def render_task(task):
    """Render task with on_change callbacks for smooth updates"""
    
    # Get existing response or use defaults
    existing = st.session_state.responses_dict.get(task.id, {
        "task_id": task.id,
        "responsibility": 50,
        "burden": 3,
        "fairness": 3,
        "not_applicable": False,
    })
    
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
    
    st.markdown("")
    
    # Create columns
    col_main, col_na = st.columns([4, 1])
    
    with col_main:
        # Question 1: Responsibility
        st.markdown("**Who mainly handles this?**")
        
        responsibility = st.slider(
            "Responsibility",
            min_value=0, 
            max_value=100, 
            value=existing.get("responsibility", 50),
            key=f"{task.id}_resp",
            label_visibility="collapsed",
            on_change=update_responsibility,
            args=(task.id,)
        )
        
        # Colour bar indicator
        if responsibility < 30:
            bar_colour = "#0072B2"
            bar_text = "🔵 Mostly Partner A"
            bar_width = "35%"
            bar_align = "left"
        elif responsibility < 50:
            bar_colour = "#5DADE2"
            bar_text = "🔵 Leaning Partner A"
            bar_width = "25%"
            bar_align = "left"
        elif responsibility == 50:
            bar_colour = "#94a3b8"
            bar_text = "↔️ Exactly equal"
            bar_width = "15%"
            bar_align = "center"
        elif responsibility <= 70:
            bar_colour = "#F5B041"
            bar_text = "Leaning Partner B 🟠"
            bar_width = "25%"
            bar_align = "right"
        else:
            bar_colour = "#E69F00"
            bar_text = "Mostly Partner B 🟠"
            bar_width = "35%"
            bar_align = "right"
        
        st.markdown(f"""
        <div style='display: flex; justify-content: {bar_align}; margin: 8px 0 12px 0;'>
            <div style='background-color: {bar_colour}; 
                        padding: 8px 16px; 
                        border-radius: 6px; 
                        width: {bar_width};
                        text-align: center;
                        font-weight: 600;
                        color: white;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                {bar_text}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        
        # Question 2: Burden
        st.markdown("**How mentally draining is this?**")
        st.caption("For whoever mainly handles it")
        
        burden = st.slider(
            "Mental burden",
            min_value=1, 
            max_value=5, 
            value=existing.get("burden", 3),
            key=f"{task.id}_burden",
            format="%d",
            label_visibility="collapsed",
            on_change=update_burden,
            args=(task.id,)
        )
        
        burden_emoji = {1: "😌", 2: "🙂", 3: "😐", 4: "😓", 5: "😰"}
        burden_text = {1: "Very light", 2: "Manageable", 3: "Moderate", 4: "Heavy", 5: "Very draining"}
        st.caption(f"{burden_emoji.get(burden, '')} {burden_text.get(burden, '')}")
        
        st.markdown("")
        
        # Question 3: Fairness
        st.markdown("**Does this feel fair to BOTH of you?**")
        st.caption("⚠️ Discuss together and agree on one rating")
        
        fairness = st.slider(
            "Fairness",
            min_value=1, 
            max_value=5, 
            value=existing.get("fairness", 3),
            key=f"{task.id}_fair",
            format="%d",
            label_visibility="collapsed",
            on_change=update_fairness,
            args=(task.id,)
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
            label_visibility="collapsed",
            on_change=update_not_applicable,
            args=(task.id,)
        )
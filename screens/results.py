# screens/results.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List

from state import reset_state
from tasks import TASK_LOOKUP
from models import Response
from logic import Calculator

A_COL = "#0072B2"  # Okabe–Ito blue (Partner A)
B_COL = "#E69F00"  # Okabe–Ito orange (Partner B)
GRID = "rgba(0,0,0,0.08)"

PILLAR_ORDER = ["anticipation", "identification", "decision", "monitoring", "emotional"]
PILLAR_LABELS = {
    "anticipation": "Anticipation",
    "identification": "Identification",
    "decision": "Decision",
    "monitoring": "Monitoring",
    "emotional": "Emotional",
}

# ---------- utils ----------
def _to_response_objects(response_dicts):
    objs = []
    for r in response_dicts:
        task = TASK_LOOKUP.get(r["task_id"])
        if not task:
            continue
        objs.append(
            Response(
                task=task,
                responsibility=int(r["responsibility"]),
                burden=int(r["burden"]),
                fairness=int(r["fairness"]),
                not_applicable=bool(r.get("not_applicable", False)),
            )
        )
    return objs

def _ensure_all_pillars(scores: Dict[str, List[float]]) -> Dict[str, List[float]]:
    """Guarantee all five pillars exist; fill missing with zeros."""
    out = {}
    for k in PILLAR_ORDER:
        out[k] = list(scores.get(k, [0.0, 0.0]))
        if len(out[k]) != 2:
            out[k] = [0.0, 0.0]
    return out

def _plain_reason(raw: str) -> str:
    s = raw or ""
    s = s.replace("Responsibility imbalance (≥30 pts)", "One partner is handling most of this")
    s = s.replace("High burden", "This feels particularly draining")
    s = s.replace("Low perceived fairness", "This doesn't feel fair to one or both partners")
    return s

def _reason_to_question(reasons: str) -> str:
    """Convert reasons into conversation questions"""
    r = (reasons or "").lower()
    if "lopsided" in r or "imbalance" in r or "handling most" in r:
        return "How did this become one person's responsibility? Was it a deliberate choice?"
    if "doesn't feel fair" in r or "fairness" in r:
        return "What would 'fair' look like to each of you for this task?"
    if "heavy" in r or "burden" in r or "draining" in r:
        return "What makes this task feel so heavy? Could part of it be shared or simplified?"
    return "What's one small thing that might make this easier?"

def _add_notes_section(page_name: str):
    """Add optional notes section with clear privacy messaging"""
    with st.expander("📝 Add notes from your conversation (optional)"):
        st.info("""
        **Privacy promise:** 
        - These notes are ONLY stored in your browser's temporary session
        - They're included in your CSV export if you download it
        - Nothing is sent to any server or saved anywhere else
        - When you close this browser tab, they're gone forever
        """)
        
        # Initialize notes dict if it doesn't exist
        if "results_notes" not in st.session_state:
            st.session_state.results_notes = {}
        
        # Get existing note for this page
        existing_note = st.session_state.results_notes.get(page_name, "")
        
        note = st.text_area(
            "Your notes:",
            value=existing_note,
            height=120,
            placeholder="Jot down insights, agreements, or things to try...",
            key=f"note_{page_name}",
            help="These notes are only stored temporarily in your browser and included in your export."
        )
        
        # Save note to session state
        st.session_state.results_notes[page_name] = note

# ---------- visuals ----------
def comparison_bars(a_val: int, b_val: int, max_val: int = 100, label_a="Partner A", label_b="Partner B"):
    """Simple horizontal comparison bars"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=[label_a, label_b],
        x=[a_val, b_val],
        orientation='h',
        marker=dict(color=[A_COL, B_COL]),
        text=[f"{a_val}", f"{b_val}"],
        textposition='outside',
        textfont=dict(size=20, color='black'),
    ))
    
    fig.update_layout(
        height=150,
        margin=dict(l=120, r=60, t=10, b=10),
        xaxis=dict(range=[0, max_val], showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
    )
    
    return fig

def pillar_grouped_bar(pillar_scores: Dict[str, List[float]]) -> go.Figure:
    scores = _ensure_all_pillars(pillar_scores)
    rows = []
    for k in PILLAR_ORDER:
        a, b = scores[k]
        rows.append({"Pillar": PILLAR_LABELS[k], "Partner": "A", "Score": a})
        rows.append({"Pillar": PILLAR_LABELS[k], "Partner": "B", "Score": b})
    df = pd.DataFrame(rows)
    df["Pillar"] = pd.Categorical(df["Pillar"], categories=[PILLAR_LABELS[k] for k in PILLAR_ORDER], ordered=True)

    fig = px.bar(
        df.sort_values("Pillar"),
        x="Pillar", y="Score", color="Partner",
        barmode="group", template="simple_white",
        color_discrete_map={"A": A_COL, "B": B_COL},
    )
    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=1.08, x=0.0),
    )
    fig.update_xaxes(showgrid=False, ticks="")
    fig.update_yaxes(gridcolor=GRID, zeroline=False, title="")
    return fig

# ---------- CSV export ----------
def _export_csv(responses, results, hotspots):
    df = pd.DataFrame(responses)
    csv = df.to_csv(index=False)

    summary = pd.DataFrame(
        {
            "Metric": [
                "Partner A load (0–100)",
                "Partner B load (0–100)",
                "Partner A invisible share (%)",
                "Partner B invisible share (%)",
            ],
            "Value": [
                results["my_intensity"],
                results["partner_intensity"],
                results["my_share_pct"],
                results["partner_share_pct"],
            ],
        }
    )
    csv += "\n\nSUMMARY\n" + summary.to_csv(index=False)

    p = _ensure_all_pillars(results.get("pillar_scores", {}))
    p_rows = [{"Pillar": PILLAR_LABELS[k], "Partner A sum": round(v[0], 2), "Partner B sum": round(v[1], 2)} for k, v in p.items()]
    csv += "\n\nPILLAR BREAKDOWN\n" + pd.DataFrame(p_rows).to_csv(index=False)

    if hotspots:
        hs_rows = [{"Task": h.get("task", ""), "Why it matters": _plain_reason(h.get("reasons", "")), "Question to discuss": _reason_to_question(h.get("reasons", ""))} for h in hotspots]
        csv += "\n\nCONVERSATION STARTERS\n" + pd.DataFrame(hs_rows).to_csv(index=False)

    # Include conversation notes if any exist
    notes = st.session_state.get("results_notes", {})
    if any(v.strip() for v in notes.values()):
        csv += "\n\nYOUR CONVERSATION NOTES\n"
        notes_rows = []
        for page, note in notes.items():
            if note.strip():
                notes_rows.append({"Page": page, "Notes": note.strip()})
        if notes_rows:
            csv += pd.DataFrame(notes_rows).to_csv(index=False)

    return csv

# ---------- conversation prep screen ----------
def screen_before_results():
    """Pre-results conversation guide"""
    st.title("💬 Before You See Your Results")
    st.markdown("### A few minutes to prepare for a productive conversation")
    
    st.markdown("""
    You're about to see data about mental load in your household. This can bring up big feelings - 
    that's completely normal and actually a sign you're both invested in your partnership.
    """)
    
    st.markdown("---")
    
    st.markdown("### 🎓 What Research Tells Us")
    st.info("""
    **Mental load** (also called cognitive labor) is the invisible work of managing a household: 
    anticipating needs, making decisions, tracking details, and coordinating family life.
    
    Research consistently shows:
    - This work is often invisible to the person not doing it
    - In heterosexual couples, women typically carry 70-80% of this load
    - It's **not about time spent** - it's about the mental energy of being "on call"
    - Even in couples who split visible tasks 50/50, mental load is often imbalanced
    - The biggest predictor of relationship satisfaction isn't perfect equality - it's feeling **heard and understood**
    """)
    
    st.markdown("### 🤝 Ground Rules for This Conversation")
    st.success("""
    **Do:**
    - Assume good intentions
    - Listen to understand, not to defend
    - Notice what surprises you
    - Acknowledge the other person's feelings as valid
    - Take breaks if it gets intense
    
    **Don't:**
    - Keep score or bring up past grievances  
    - Interrupt or dismiss
    - Try to "win" the conversation
    - Expect to solve everything today
    """)
    
    st.markdown("### 🎯 The Goal of This Exercise")
    st.markdown("""
    The point isn't to create perfect 50/50 splits or to prove who's right. 
    
    **The goal is to:**
    1. Make invisible work visible
    2. Understand each other's experience
    3. Find 1-2 small changes you both agree to try
    4. Build a habit of checking in together
    """)
    
    st.markdown("---")
    
    st.markdown("### ✋ Before You Continue")
    st.warning("""
    **Pause here if:**
    - Either of you is tired, hungry, or stressed right now
    - You've been arguing about this recently
    - One of you isn't ready to have this conversation
    
    This tool will be here when you're both ready. There's no rush.
    """)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to questionnaire", use_container_width=True):
            st.session_state.stage = "questionnaire"
            st.rerun()
    with col2:
        if st.button("We're ready - show results →", use_container_width=True, type="primary"):
            st.session_state.results_page = 1
            st.session_state.stage = "results_main"
            st.rerun()

# ---------- PAGINATED RESULTS SECTIONS ----------

def _results_page_1_share(results, hotspots):
    """Page 1: The Big Picture - Who's Carrying What"""
    st.title("📊 Your Results: The Big Picture")
    st.caption("💙 Remember: This is about understanding, not blame.")
    st.progress(20)  # 1 of 5 pages
    
    st.markdown("---")
    
    st.markdown("## 📚 Context: What Research Shows")
    
    with st.expander("📖 Click to read about mental load patterns in households"):
        st.markdown("""
        Studies of household labor consistently find:
        
        - **Visible vs. Invisible Split:** Even when couples split physical tasks evenly, the invisible work 
          (planning, remembering, coordinating) is often held by one partner
        - **The "Manager-Helper" Dynamic:** One partner acts as the household manager who delegates, 
          while the other helps when asked - but doesn't carry the mental burden of anticipating needs
        - **Gendered Patterns:** In heterosexual couples, research shows women typically carry 2-3x 
          more cognitive labor, regardless of employment status
        - **Why It Matters:** Unacknowledged mental load is strongly linked to resentment, burnout, 
          and relationship dissatisfaction
        - **Good News:** Simply naming and discussing mental load improves outcomes, even before changes are made
        """)
    
    st.markdown("### 🔍 Your Household's Snapshot")
    st.markdown("Here's what your responses show about mental load distribution right now.")
    
    a_share, b_share = results["my_share_pct"], results["partner_share_pct"]
    
    # Share percentages
    st.markdown("**Mental load share (who's carrying the invisible work):**")
    st.plotly_chart(comparison_bars(a_share, b_share, 100, "Partner A", "Partner B"), use_container_width=True)
    
    # Research context for their numbers
    diff = abs(a_share - b_share)
    if diff <= 15:
        st.success("✅ **Your household shows relatively balanced mental load.** Research suggests 60/40 or closer is associated with higher relationship satisfaction.")
    elif diff <= 30:
        st.info("📊 **Your split is common.** About 60% of couples show this pattern. The question is: does it feel sustainable to both of you?")
    else:
        st.warning("📊 **This pattern is common but can lead to burnout.** Research shows splits beyond 70/30 often predict resentment over time - but this is changeable.")
    
    # Discussion prompt
    st.markdown("---")
    st.markdown("### 💭 Pause & Reflect")
    st.markdown("""
    **Questions to discuss together:**
    - Does this percentage match how it *feels* in daily life?
    - What surprises you about this number?
    - What might explain this pattern in your household?
    """)
    
    # Optional notes
    st.markdown("---")
    _add_notes_section("Page 1: The Big Picture")


def _results_page_2_burden(results):
    """Page 2: How Heavy Does It Feel"""
    st.title("📊 How Heavy Does It Feel?")
    st.caption("💙 Understanding the emotional weight of invisible work")
    st.progress(40)  # 2 of 5 pages
    
    st.markdown("---")
    
    st.markdown("## 😰 Personal Burden")
    st.markdown("""
    **Personal burden (0-100):** This isn't about how much time tasks take - it's about how draining 
    the mental work feels.
    
    Research shows mental load burden comes from:
    - Being "on call" mentally even during downtime
    - The invisible work of anticipating others' needs
    - Carrying responsibility without recognition
    """)
    
    a_int, b_int = results["my_intensity"], results["partner_intensity"]
    st.plotly_chart(comparison_bars(a_int, b_int, 100, "Partner A", "Partner B"), use_container_width=True)
    
    # Research context
    load_diff = abs(a_int - b_int)
    if load_diff <= 15:
        st.success("Both partners report similar burden levels - this suggests the mental energy feels fairly distributed.")
    elif load_diff <= 30:
        heavier = "Partner A" if a_int > b_int else "Partner B"
        st.info(f"📊 {heavier} reports feeling more burdened. This is worth exploring - sometimes visible task-sharing doesn't capture invisible stress.")
    else:
        heavier = "Partner A" if a_int > b_int else "Partner B"
        st.warning(f"⚠️ {heavier}'s burden score is notably higher. Research links sustained high burden to burnout and relationship strain.")
    
    # Discussion prompt
    st.markdown("---")
    st.markdown("### 💭 Pause & Reflect")
    st.markdown("""
    **Questions to discuss together:**
    - For the person with higher burden: What makes it feel heavy? Is it the tasks themselves, or the mental energy of managing them?
    - For the person with lower burden: Does this surprise you? What might you not be seeing?
    - Are there times of day or week when burden peaks for each of you?
    """)
    
    # Optional notes
    st.markdown("---")
    _add_notes_section("Page 2: How Heavy Does It Feel")


def _results_page_3_pillars(results):
    """Page 3: The Five Pillars"""
    st.title("📊 Where the Mental Load Lives")
    st.caption("💙 Breaking down the five types of invisible work")
    st.progress(60)  # 3 of 5 pages
    
    st.markdown("---")
    
    st.markdown("## 🏛️ The Five Pillars of Mental Load")
    st.markdown("""
    Research identifies five types of cognitive labor in households. This chart shows which 
    partner is carrying more of each type.
    """)
    
    with st.expander("ℹ️ What these five pillars mean (click to expand)"):
        st.markdown("""
        Based on research in household labor and emotional work:
        
        - **Anticipation:** Thinking ahead to what will be needed (meal planning, remembering appointments, 
          anticipating when supplies run low)
        - **Identification:** Noticing what needs doing (seeing the mess, recognizing when something's broken, 
          spotting when someone needs support)
        - **Decision-Making:** Researching options and making choices (which doctor, what gift, how to handle 
          a situation)
        - **Monitoring:** Tracking progress and following up (did the form get submitted? Is the kids' project 
          done? Are we running low on groceries?)
        - **Emotional Labor:** Managing feelings, maintaining relationships, providing support, creating 
          household harmony
        
        **Key finding:** The monitoring and anticipation pillars are often most invisible to the partner not doing them.
        """)
    
    pillar_scores = _ensure_all_pillars(results.get("pillar_scores", {}))
    st.plotly_chart(pillar_grouped_bar(pillar_scores), use_container_width=True)
    
    # Discussion prompt
    st.markdown("---")
    st.markdown("### 💭 Pause & Reflect")
    st.markdown("""
    **Questions to discuss together:**
    - Which pillar shows the biggest difference between you?
    - Is there a pillar where one person didn't realize how much the other was doing?
    - Research shows "monitoring" is often invisible - does that resonate?
    """)
    
    # Optional notes
    st.markdown("---")
    _add_notes_section("Page 3: The Five Pillars")


def _results_page_4_hotspots(hotspots):
    """Page 4: Conversation Starters"""
    st.title("📊 Conversation Starters")
    st.caption("💙 Topics worth exploring together")
    st.progress(80)  # 4 of 5 pages
    
    st.markdown("---")
    
    st.markdown("## 💬 Areas to Explore")
    st.markdown("""
    These aren't "problems to fix" - they're **topics worth exploring together**. 
    
    Research shows that couples who regularly discuss mental load (even without making immediate changes) 
    report higher satisfaction than those who don't talk about it.
    """)
    
    if hotspots:
        st.info(f"📌 We've identified {len(hotspots)} areas where responses suggest an imbalance, high burden, or fairness concern. Start with one.")
        
        # Show top 3 as conversation starters
        for i, h in enumerate(hotspots[:3], 1):
            with st.container():
                st.markdown(f"### {i}. {h.get('task', 'Task')}")
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    plain = _plain_reason(h.get("reasons", ""))
                    st.markdown(f"**Why it came up:** {plain}")
                
                with col2:
                    question = _reason_to_question(h.get("reasons", ""))
                    st.markdown(f"**💭 Discuss:** {question}")
                
                st.markdown("")
        
        # Remaining in expander
        if len(hotspots) > 3:
            with st.expander(f"📋 See {len(hotspots) - 3} more conversation starters"):
                for i, h in enumerate(hotspots[3:], 4):
                    st.markdown(f"**{i}. {h.get('task', 'Task')}**")
                    st.markdown(f"*{_plain_reason(h.get('reasons', ''))}*")
                    st.markdown(f"💭 *{_reason_to_question(h.get('reasons', ''))}*")
                    st.markdown("")
    else:
        st.success("""
        🎉 **No major conversation starters detected!** 
        
        Your responses suggest relatively balanced mental load distribution. This is worth celebrating!
        
        Still, research recommends checking in periodically - life circumstances change, and what works 
        now might need adjustment later.
        """)
    
    # Optional notes
    st.markdown("---")
    _add_notes_section("Page 4: Conversation Starters")


def _results_page_5_action():
    """Page 5: What's Next"""
    st.title("📊 What's Next")
    st.caption("💙 Building from strengths and trying small experiments")
    st.progress(100)  # 5 of 5 pages
    
    st.markdown("---")
    
    # ====== WHAT'S WORKING ======
    st.markdown("## ✨ What's Working Well")
    st.markdown("""
    Research on couple interventions shows that building from strengths is more effective than 
    only focusing on problems.
    """)
    
    # Find areas of relative balance
    balanced_areas = []
    for task_response in st.session_state.responses:
        resp_diff = abs(task_response.get("responsibility", 50) - 50)
        if resp_diff <= 20 and task_response.get("burden", 50) < 60:
            task = TASK_LOOKUP.get(task_response["task_id"])
            if task:
                balanced_areas.append(task.name)
    
    if balanced_areas:
        st.success(f"**Areas showing good balance:** {', '.join(balanced_areas[:5])}")
        st.markdown("💭 **Discuss:** What makes these areas work well? Can you apply that pattern elsewhere?")
    else:
        st.info("**Every household has strengths.** What's one thing you're both proud of in how you manage your home together?")
    
    st.markdown("---")
    
    # ====== EXPERIMENT ======
    st.markdown("## 🧪 Try One Small Experiment")
    st.markdown("""
    Research on behavior change shows that small, time-bound experiments work better than big overhauls.
    
    **The invitation:** Pick ONE thing from your conversation starters. Agree to try a small change 
    for one week, then check in.
    """)
    
    st.info("""
    **What makes a good experiment:**
    - Specific (not "help more" but "Partner B will plan meals Tuesday-Thursday")
    - Time-bound (try for one week)
    - Agreed by both (not imposed on one person)
    - Reversible (you can always go back)
    """)
    
    st.markdown("---")
    st.markdown("## 🎉 You've Completed the Journey")
    st.success("""
    You've taken an important step toward understanding mental load in your household. 
    
    **Next steps:**
    - Add any final notes below
    - Download your results (including all your notes)
    - Try your small experiment for one week
    - Check in together next weekend
    - Return to this tool in a month to see how things have shifted
    """)
    
    # Optional notes
    st.markdown("---")
    _add_notes_section("Page 5: Action Plan & Experiment")


# ---------- main results navigation ----------
def screen_results_main():
    """Main results with pagination"""
    
    if not st.session_state.get("responses"):
        st.warning("No results yet. Please complete the questionnaire first.")
        return

    # compute results once
    response_objs = _to_response_objects(st.session_state.responses)
    calc = Calculator(response_objs)
    results = calc.compute()
    hotspots = Calculator.detect_hotspots(response_objs)

    # Initialize page if not set
    if "results_page" not in st.session_state:
        st.session_state.results_page = 1
    
    current_page = st.session_state.results_page
    
    # Header navigation (always visible)
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.caption(f"Page {current_page} of 5")
    with col2:
        if st.button("🔁 Start Over", use_container_width=True):
            reset_state()
            st.session_state.stage = "home"
            st.rerun()
    with col3:
        csv_data = _export_csv(st.session_state.responses, results, hotspots)
        st.download_button(
            "📥 Export",
            data=csv_data,
            file_name="mental_load_results.csv",
            mime="text/csv",
            use_container_width=True,
        )
    
    st.markdown("---")
    
    # Render current page
    if current_page == 1:
        _results_page_1_share(results, hotspots)
    elif current_page == 2:
        _results_page_2_burden(results)
    elif current_page == 3:
        _results_page_3_pillars(results)
    elif current_page == 4:
        _results_page_4_hotspots(hotspots)
    elif current_page == 5:
        _results_page_5_action()
    
    # Show note count if any notes exist
    notes = st.session_state.get("results_notes", {})
    note_count = sum(1 for v in notes.values() if v.strip())
    if note_count > 0:
        st.info(f"📝 You have notes on {note_count} page(s) - they'll be included in your export")
    
    # Navigation footer (always at bottom)
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if current_page > 1:
            if st.button("← Previous", use_container_width=True):
                st.session_state.results_page -= 1
                st.rerun()
        else:
            st.button("← Previous", disabled=True, use_container_width=True)
    
    with col2:
        # Page indicators
        dots = ""
        for i in range(1, 6):
            if i == current_page:
                dots += "🔵 "
            else:
                dots += "⚪ "
        st.markdown(f"<div style='text-align: center; padding: 8px;'>{dots}</div>", unsafe_allow_html=True)
    
    with col3:
        if current_page < 5:
            if st.button("Next →", use_container_width=True, type="primary"):
                st.session_state.results_page += 1
                st.rerun()
        else:
            if st.button("🏠 Finish", use_container_width=True, type="primary"):
                st.session_state.stage = "home"
                st.rerun()
    
    st.markdown("---")
    st.caption("""
    💙 **Remember:** This is one snapshot in time. Mental load shifts with life circumstances. 
    The healthiest couples check in regularly, not just once.
    """)


# ---------- Main entry point ----------
def screen_results():
    """Route to either prep screen or main results"""
    # First time seeing results? Show prep screen
    if not st.session_state.get("results_prep_seen", False):
        screen_before_results()
        st.session_state.results_prep_seen = True
    else:
        # They've seen prep, show paginated results
        screen_results_main()
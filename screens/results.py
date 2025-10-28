# screens/results.py
import streamlit as st
import streamlit.components.v1 as components
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
    """Convert a hotspot reason string into a conversation question."""
    if not reasons:
        return "What's one small thing that might make this easier?"
    
    r_lower = reasons.lower()
    
    # Priority combo
    if "priority" in r_lower and "imbalanced" in r_lower and "unfair" in r_lower:
        return "This feels both imbalanced and unfair. What would need to change for it to feel better?"
    
    # Imbalance
    if "imbalance" in r_lower or "handling most" in r_lower:
        return "How did this pattern develop? Would a different split work better?"
    
    # High burden
    if "draining" in r_lower or "burden" in r_lower:
        return "What makes this feel so heavy? Is it the task itself or the mental energy around it?"
    
    # Fairness
    if "fair" in r_lower:
        return "What would make this feel fairer to both of you?"
    
    # Default
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
        
        # Initialise notes dict if it doesn't exist
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
        margin=dict(l=10, r=10, t=10),
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
                "Partner A burden (0–100)",
                "Partner B burden (0–100)",
                "Partner A invisible share (%)",
                "Partner B invisible share (%)",
            ],
            "Value": [
                results["my_burden"],
                results["partner_burden"],
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

    # Include QUESTIONNAIRE section notes (from when they filled it in)
    questionnaire_notes = st.session_state.get("notes_by_section", {})
    if any(v.strip() for v in questionnaire_notes.values()):
        csv += "\n\nQUESTIONNAIRE SECTION NOTES\n"
        notes_rows = []
        for section, note in questionnaire_notes.items():
            if note.strip():
                notes_rows.append({"Section": section, "Notes": note.strip()})
        if notes_rows:
            csv += pd.DataFrame(notes_rows).to_csv(index=False)

    # Include RESULTS conversation notes (from results pages)
    results_notes = st.session_state.get("results_notes", {})
    if any(v.strip() for v in results_notes.values()):
        csv += "\n\nRESULTS CONVERSATION NOTES\n"
        notes_rows = []
        for page, note in results_notes.items():
            if note.strip():
                notes_rows.append({"Page": page, "Notes": note.strip()})
        if notes_rows:
            csv += pd.DataFrame(notes_rows).to_csv(index=False)

    return csv

# ---------- conversation prep screen ----------
def screen_before_results():
    """Minimal prep before viewing results"""
    # Top-right Home button
    _pre_l, _pre_r = st.columns([6, 1])
    with _pre_r:
        if st.button("Home", use_container_width=True, key="pre_home"):
            st.session_state.stage = "home"
            st.rerun()

    st.title("💬 Before You See Your Results")
    st.caption("Quick prep for a productive conversation")
    
    st.markdown("""
    You're about to see data about mental load in your household. This can bring up feelings - 
    that's normal and shows you're both invested.
    """)
    
    st.markdown("---")
    
    # Ground rules - CONDENSED
    st.success("""
    **🤝 Quick ground rules:**
    - **Do:** Listen to understand, acknowledge feelings, take breaks if needed
    - **Don't:** Keep score, interrupt, or try to "win"
    """)
    
    # Key insight - ONE LINE
    st.info("""
    **💡 Research shows:** Feeling heard matters more than perfect equality. Just discussing mental load improves relationships.
    """)
    
    # Pause warning
    st.warning("⏸️ **Pause if** either of you is tired, stressed, or not ready. This can wait.")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.stage = "questionnaire"
            st.rerun()
    with col2:
        if st.button("Show results →", use_container_width=True, type="primary"):
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
        Studies of household labour consistently find:
        
        - **Visible vs. Invisible Split:** Even when couples split physical tasks evenly, the invisible work 
          (planning, remembering, coordinating) is often held by one partner
        - **The "Manager-Helper" Dynamic:** One partner acts as the household manager who delegates, 
          while the other helps when asked - but doesn't carry the mental burden of anticipating needs
        - **Gendered Patterns:** In heterosexual couples, research shows women typically carry 2-3x 
          more cognitive labour, regardless of employment status
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
        st.success("✅ **Your household shows a relatively balanced mental load.** Research on household cognitive labour shows large asymmetries are common, so a near-even split represents a more balanced pattern than is typically observed.")
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
    
    # --- Added: heading with info button next to "Personal Burden" ---
    col_left, col_right = st.columns([0.8, 0.2])
    with col_left:
        st.markdown("## 😰 Personal Burden")
    with col_right:
        try:
            with st.popover("ℹ️ What does 'Burden' mean?"):
                st.write(
                    "Burden is the mental side of household work — thinking ahead, remembering, "
                    "planning and coordinating. It’s not just minutes doing a chore, but the headspace it takes."
                )
        except Exception:
            with st.expander("ℹ️ What does 'Burden' mean?"):
                st.write(
                    "Burden is the mental side of household work — thinking ahead, remembering, "
                    "planning and coordinating. It’s not just minutes doing a chore, but the headspace it takes."
                )
    
    # --- Added: super dummy-friendly explainer of how the score is made and why it makes sense ---
    st.success(
        "**In plain terms:** For each task we combine three things — (1) who mostly carries it, "
        "(2) how draining it feels, and (3) how fair it feels. "
        "If you carry more of a task *and* it feels heavy or unfair, your Burden score goes up. "
        "We add that across tasks to show each person’s overall mental load. This makes sense because "
        "both responsibility and how it feels day-to-day shape the real ‘weight’ you experience."
    )
    
    st.markdown("""
    **Personal burden (0-100):** This isn't about how much time tasks take - it's about how draining 
    the mental work feels.
    
    Research shows mental load burden comes from:
    - Being "on call" mentally even during downtime
    - The invisible work of anticipating others' needs
    - Carrying responsibility without recognition
    """)
    
    a_burden, b_burden = results["my_burden"], results["partner_burden"]
    st.plotly_chart(comparison_bars(a_burden, b_burden, 100, "Partner A", "Partner B"), use_container_width=True)
    
    # Research context
    burden_diff = abs(a_burden - b_burden)
    if burden_diff <= 15:
        st.success("Both partners report similar burden levels - this suggests the mental energy feels fairly distributed.")
    elif burden_diff <= 30:
        heavier = "Partner A" if a_burden > b_burden else "Partner B"
        st.info(f"📊 {heavier} reports feeling more burdened. This is worth exploring - sometimes visible task-sharing doesn't capture invisible stress.")
    else:
        heavier = "Partner A" if a_burden > b_burden else "Partner B"
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
    Research identifies five types of cognitive labour in households. This chart shows which 
    partner is carrying more of each type.
    """)
    
    with st.expander("ℹ️ What these five pillars mean (click to expand)"):
        st.markdown("""
        Based on research in household labour and emotional work:
        
        - **Anticipation:** Thinking ahead to what will be needed (meal planning, remembering appointments, 
          anticipating when supplies run low)
        - **Identification:** Noticing what needs doing (seeing the mess, recognising when something's broken, 
          spotting when someone needs support)
        - **Decision-Making:** Researching options and making choices (which doctor, what gift, how to handle 
          a situation)
        - **Monitoring:** Tracking progress and following up (did the form get submitted? Is the kids' project 
          done? Are we running low on groceries?)
        - **Emotional Labour:** Managing feelings, maintaining relationships, providing support, creating 
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
    - Is there a pillar where one person didn't realise how much the other was doing?
    - Research shows "monitoring" is often invisible - does that resonate?
    """)
    
    # Optional notes
    st.markdown("---")
    _add_notes_section("Page 3: The Five Pillars")


def _results_page_4_hotspots(hotspots):
    """Page 4: Conversation Starters - REDUCED TO TOP 5 ONLY"""
    st.title("📊 Conversation Starters")
    st.caption("💙 Focus on just a few key topics")
    st.progress(80)  # 4 of 5 pages
    
    st.markdown("---")
    
    st.markdown("## 💬 Areas to Explore")
    st.markdown("""
    These aren't "problems to fix" - they're **topics worth exploring together**. 
    
    Research shows that couples who regularly discuss mental load (even without making immediate changes) 
    report higher satisfaction than those who don't talk about it.
    
    **We've focused on just the top few areas** to keep your conversation manageable and productive.
    """)
    
    if hotspots:
        # LIMIT TO TOP 5 MAXIMUM
        top_hotspots = hotspots[:5]
        
        st.info(f"📌 We've identified {len(top_hotspots)} priority {'area' if len(top_hotspots) == 1 else 'areas'} to discuss. Pick one or two to start with.")
        
        # Show all selected hotspots fully expanded
        for i, h in enumerate(top_hotspots, 1):
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
        
        # Note about focusing on just a few
        if len(hotspots) > 5:
            st.info(f"💡 **Note:** There were {len(hotspots)} total areas flagged, but we're showing only the top 5 to help you focus. You can always revisit this tool to explore others later.")
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
    # ====== CRITICAL: SURVEY LINK ======
    st.markdown("## 📋 Essential: Quick Survey")
    st.error("""
    **⚠️ Please complete this 5-minute survey now - it's crucial for the research!**
    
    Your feedback helps us understand if the tool was useful.
    This directly impacts the validity of the thesis research.
    """)
    
    survey_url = "https://forms.office.com/e/jM0DXUg1vV"
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.link_button(
            "📋 Complete survey now (5 min) →",
            survey_url,
            use_container_width=True,
            type="primary"
        )
        st.caption("⭐ Essential for research • Completely anonymous")
    
    st.markdown("---")
    
    # Done
    st.success("""
    **🎉 You've completed the tool!**
    
    **Next steps:**
    1. ✅ Complete the survey above
    2. 📥 Download your results if you want a copy(button at top)
    3. 🧪 Try your one-week experiment
    4. 🔄 Check in next week
    """)
    
    st.markdown("---")
    _add_notes_section("Page 5: Action Plan")


# ---------- main results navigation ----------
def screen_results_main():
    """Main results with pagination"""

    if not st.session_state.get("responses"):
        st.warning("No results yet. Please complete the questionnaire first.")
        return

    # Compute results once
    response_objs = _to_response_objects(st.session_state.responses)
    calc = Calculator(response_objs)
    results = calc.compute()
    hotspots = Calculator.detect_hotspots(response_objs)

    # Initialise page if not set
    if "results_page" not in st.session_state:
        st.session_state.results_page = 1

    current_page = st.session_state.results_page

    # ----- TOP NAVIGATION -----
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        # Previous button
        if current_page > 1:
            if st.button("← Previous", key="top_prev", use_container_width=True):
                st.session_state.results_page -= 1
                st.rerun()
        else:
            st.button("← Previous", key="top_prev_disabled", disabled=True, use_container_width=True)

    with col2:
        # Next or Finish button
        if current_page < 5:
            if st.button("Next →", key="top_next", use_container_width=True, type="primary"):
                st.session_state.results_page += 1
                st.rerun()
        else:
            if st.button("🏠 Finish", key="top_finish", use_container_width=True, type="primary"):
                st.session_state.stage = "home"
                st.rerun()

    with col3:
        # NEW: Home button (Escape option)
        if st.button("Home", key="top_home", use_container_width=True):
            st.session_state.stage = "home"
            st.rerun()

    with col4:
        # Export button stays far right
        csv_data = _export_csv(st.session_state.responses, results, hotspots)
        st.download_button(
            "📥 Export",
            data=csv_data,
            file_name="mental_load_results.csv",
            mime="text/csv",
            use_container_width=True,
            key="top_export"
        )

    # Page number indicator
    st.caption(f"Page {current_page} of 5")
    st.markdown("---")

    # ----- RENDER CURRENT PAGE -----
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

    # ----- NOTES COUNT -----
    questionnaire_notes = st.session_state.get("notes_by_section", {})
    results_notes = st.session_state.get("results_notes", {})
    questionnaire_note_count = sum(1 for v in questionnaire_notes.values() if v.strip())
    results_note_count = sum(1 for v in results_notes.values() if v.strip())
    total_note_count = questionnaire_note_count + results_note_count

    if total_note_count > 0:
        st.info(
            f"📝 You have notes on {total_note_count} page(s) "
            f"({questionnaire_note_count} from questionnaire, {results_note_count} from results) "
            "- they'll be included in your export."
        )

    # ----- PAGE INDICATORS -----
    st.markdown("---")
    dots = ""
    for i in range(1, 6):
        dots += "🔵 " if i == current_page else "⚪ "
    st.markdown(f"<div style='text-align: center; padding: 8px;'>{dots}</div>", unsafe_allow_html=True)

    st.caption("""
    💙 **Remember:** This is one snapshot in time. Mental load shifts with life circumstances. 
    The healthiest couples check in regularly, not just once.
    """)


# ---------- Main entry point ----------
def screen_results():
    """Route to either prep screen or main results"""
    # First time seeing results? Show prep screen
    if not st.session_state.get("results_prep_seen", False):
        st.session_state.results_prep_seen = True
        screen_before_results()
    else:
        screen_results_main()

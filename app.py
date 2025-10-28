import streamlit as st
from pathlib import Path

from state import init_state, reset_state
from screens.home import screen_home
from screens.consent import screen_consent
from screens.setup import screen_setup
from screens.questionnaire import screen_questionnaire
from screens.results import screen_results
from screens.learnmore import screen_learn_more

st.set_page_config(page_title="Mental Load Coach", page_icon="🧠", layout="wide")

# ---- CSS ----
def load_css():
    css_path = Path("assets/style.css")
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
load_css()

# ---- Init ----
init_state()

# ---- CONDITIONAL NAVIGATION (best practice: hide during conversion moments) ----
stage = st.session_state.stage

# Only show full navigation on non-critical stages
if stage not in ["questionnaire", "results", "results_main"]:
    with st.sidebar:
        st.markdown("### Navigation")
        if st.button("🏠 Home"):             st.session_state.stage = "home"
        if st.button("✅ Consent"):          st.session_state.stage = "consent"
        if st.button("⚙️ Setup"):           st.session_state.stage = "setup"
        if st.button("📝 Questionnaire"):    st.session_state.stage = "questionnaire"
        if st.button("📊 Results"):          st.session_state.stage = "results"
        st.divider()
        if st.button("🔁 Start again"):
            reset_state()
            st.session_state.stage = "home"
        
        st.caption("You can return here at any time.")
else:
    # Minimal sidebar during critical stages - just emergency exit
    with st.sidebar:
        st.markdown("### 🧠 Mental Load Coach")
        st.caption("Working through the questionnaire...")
        st.markdown("---")
        st.caption("⚠️ **Important:** Try to complete in one go for best results.")
        st.markdown("")
        if st.button("🚪 Exit & restart", type="secondary", use_container_width=True):
            if st.session_state.get('confirm_exit', False):
                reset_state()
                st.session_state.stage = "home"
                st.rerun()
            else:
                st.session_state.confirm_exit = True
                st.warning("Click again to confirm - you'll lose your progress")
        
        if st.session_state.get('confirm_exit', False):
            st.caption("☝️ Click exit button again to confirm")

# ---- Router ----
if stage == "home":
    screen_home()
elif stage == "consent":
    screen_consent()
elif stage == "setup":
    screen_setup()
elif stage == "questionnaire":
    screen_questionnaire()
elif stage == "results" or stage == "results_main":
    screen_results()
elif stage == "learn_more":
    screen_learn_more()
else:
    st.session_state.stage = "home"
    screen_home()
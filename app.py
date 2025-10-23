import streamlit as st
from pathlib import Path

from state import init_state, reset_state
from screens.home import screen_home
from screens.consent import screen_consent
from screens.setup import screen_setup
from screens.questionnaire import screen_questionnaire
from screens.results import screen_results
from screens.learnmore import screen_learn_more
from utils.dev_mode import toggle_dev_mode, is_dev_mode, dev_mode_widget

st.set_page_config(page_title="Mental Load Coach", page_icon="🧠", layout="wide")

# ---- CSS ----
def load_css():
    css_path = Path("assets/style.css")
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
load_css()

# ---- Init + sidebar nav ----
init_state()

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
    
    # Dev mode toggle at bottom
    st.divider()
    dev_mode_enabled = is_dev_mode()
    if st.button(
        f"{'🛠️ Dev Mode: ON' if dev_mode_enabled else '🔧 Dev Mode: OFF'}", 
        use_container_width=True,
        type="primary" if dev_mode_enabled else "secondary"
    ):
        toggle_dev_mode()
        st.rerun()
    
    # Show dev controls if enabled
    dev_mode_widget()
    
    st.caption("You can return here at any time.")

# ---- Router ----
stage = st.session_state.stage
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
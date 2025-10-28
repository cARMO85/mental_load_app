import streamlit as st
from pathlib import Path

from state import init_state, reset_state
from screens.home import screen_home
from screens.consent import screen_consent
from screens.setup import screen_setup
from screens.questionnaire import screen_questionnaire
from screens.results import screen_results
from screens.learnmore import screen_learn_more

# ----- PAGE CONFIG -----
st.set_page_config(
    page_title="Mental Load Helper",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----- HIDE SIDEBAR AND NAVBAR -----
HIDE_SIDEBAR_CSS = """
<style>
[data-testid="stSidebar"] {display: none !important;}
[data-testid="stSidebarNav"] {display: none !important;}
button[kind="header"] {display: none !important;}
</style>
"""
st.markdown(HIDE_SIDEBAR_CSS, unsafe_allow_html=True)

# ----- LOAD CUSTOM CSS -----
def load_css():
    css_path = Path("assets/style.css")
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
load_css()

# ----- INIT -----
init_state()

# ----- ROUTER -----
stage = st.session_state.stage

if stage == "home":
    screen_home()
elif stage == "consent":
    screen_consent()
elif stage == "setup":
    screen_setup()
elif stage == "questionnaire":
    screen_questionnaire()
elif stage in ["results", "results_main"]:
    screen_results()
elif stage == "learn_more":
    screen_learn_more()
else:
    st.session_state.stage = "home"
    screen_home()

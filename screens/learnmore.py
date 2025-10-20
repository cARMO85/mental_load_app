import streamlit as st

def screen_learn_more():
    st.header("Learn more — how this works")
    st.write("Plain-English overview of the science and design choices.")
    st.markdown("""
- **What we measure:** visible time and the *invisible* planning/monitoring/emotional work.
- **Why a quick estimate:** enough to surface patterns and start a caring conversation.
- **Fairness & care:** This isn’t a test. It’s a helper to agree small, practical changes.
    """)
    st.info("We’ll publish a methods note with sources as your thesis progresses.")

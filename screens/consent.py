import streamlit as st

def screen_consent():
    st.header("Before we start — a quick agreement")
    st.write("This tool is for kind conversations, not blame. You can stop at any time.")

    kind = st.checkbox("We agree to be kind and pause if it gets tough.")
    consent = st.checkbox("We consent to answer and view results together.")

    st.info("We don’t collect names or emails. Nothing is shared.")
    disabled = not (kind and consent)
    if st.button("Continue to setup →", disabled=disabled):
        st.session_state.stage = "setup"

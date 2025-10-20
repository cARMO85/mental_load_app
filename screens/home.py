import streamlit as st
from utils.ui import learn_popover

def screen_home():
    st.title("Mental Load Coach 🧠")
    st.markdown(
        "<div class='hero'><h3>You can’t share the load if it’s invisible.</h3>"
        "<p>This short, private tool helps couples see both the visible and the <em>invisible</em> work "
        "— and pick one small change to try for 7 days.</p>"
        "<ul><li>10 minutes, together</li><li>No sign-in, no names</li><li>Evidence-informed; kind by design</li></ul></div>",
        unsafe_allow_html=True,
    )

    c1,c2 = st.columns([2,2])
    with c1:
        st.subheader("How it works (3 steps)")
        st.write("1) Consent • 2) Answer short questions • 3) See results and agree a 7-day experiment")
        st.success("Start when you’re both ready. You can pause any time.")
        if st.button("Start • Consent →", use_container_width=True):
            st.session_state.stage = "consent"
    with c2:
        st.subheader("What you’ll get")
        st.write("- Who’s carrying what (clear chart)")
        st.write("- Top hotspot and a 10-minute next step")
        st.write("- A one-line plan you can export")
        learn_popover()

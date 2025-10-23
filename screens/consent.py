import streamlit as st
from datetime import datetime

def screen_consent():
    st.title("Participant Information & Consent")

    st.markdown("""
    ### Study Information

    **Research Title:** Mental Load Coach - Tool Evaluation Study
    **Researcher:** Paul [ADD YOUR SURNAME]
    **Institution:** [ADD YOUR UNIVERSITY NAME]
    **Programme:** Master's Thesis
    **Supervisor:** [ADD SUPERVISOR NAME]

    ### What is this study?

    This tool helps couples discuss household mental load. You'll:
    - Answer questions about household tasks (15-20 minutes)
    - See personalised results
    - Complete a brief feedback survey afterwards

    ### Your data

    - **In the tool:** No data is stored. Everything stays in your browser and is deleted when you close the tab.
    - **In the survey:** You'll be asked to complete a separate feedback survey. That data will be stored securely and used only for this research.

    ### Voluntary participation

    - You can stop at any time
    - You can skip any questions
    - No penalties for withdrawing

    ### Risks & benefits

    - **Risks:** Discussing household labour may bring up difficult emotions. Pause if needed.
    - **Benefits:** Increased awareness and structured conversations about mental load.

    ### Not a substitute for therapy

    This is a research tool, not clinical intervention. If you need relationship support, please seek professional help.

    ### Questions or concerns?

    Contact: [ADD YOUR EMAIL]

    ---

    ### Consent

    Please confirm:
    """)

    col1, col2 = st.columns([1, 4])

    consent_items = {}

    with col2:
        consent_items['read'] = st.checkbox(
            "I have read and understood the information above",
            key="consent_read"
        )
        consent_items['participate'] = st.checkbox(
            "I agree to participate in this research",
            key="consent_participate"
        )
        consent_items['data'] = st.checkbox(
            "I understand that no personal data is stored in the tool",
            key="consent_data"
        )
        consent_items['withdraw'] = st.checkbox(
            "I understand I can withdraw at any time",
            key="consent_withdraw"
        )
        consent_items['both'] = st.checkbox(
            "Both partners consent to participate together",
            key="consent_both"
        )

    all_consented = all(consent_items.values())

    st.markdown("---")

    if st.button("Continue to Study →", disabled=not all_consented, type="primary", use_container_width=True):
        st.session_state.consented = True
        st.session_state.consent_timestamp = datetime.now().isoformat()
        st.session_state.stage = "setup"
        st.rerun()

    if not all_consented:
        st.caption("Please tick all boxes to continue")

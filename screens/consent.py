import streamlit as st

def screen_consent():
    """
    Research consent screen with proper ethics information
    Replace [YOUR_EMAIL], [YOUR_UNIVERSITY], and [SUPERVISOR_NAME] with actual details
    """
    st.title("📋 Participant Information & Consent")
    st.caption("Research Study: Evaluating a Digital Tool for Mental Load Conversations")
    
    st.markdown("---")
    
    # Study information
    st.markdown("## About This Study")
    st.markdown("""
    You are invited to participate in a pilot study evaluating a digital tool designed to facilitate 
    conversations about mental load in cohabiting couples.
    
    **Principal Investigator:** Paul [YOUR_LAST_NAME]  
    **Institution:** [YOUR_UNIVERSITY]  
    **Supervisor:** [SUPERVISOR_NAME]  
    **Study Type:** Master's thesis pilot study
    """)
    
    st.markdown("---")
    
    # What participation involves
    with st.expander("📖 What does participation involve?"):
        st.markdown("""
        **Time commitment:** Approximately 30-40 minutes total
        
        **Activities:**
        1. **Pre-survey** (5 minutes): Complete individually before using the tool
        2. **Tool usage** (15-20 minutes): Complete the questionnaire together as a couple
        3. **Post-survey** (5-10 minutes): Complete individually after using the tool
        
        **What we're evaluating:**
        - Whether the tool is easy to use
        - Whether it facilitates productive conversations
        - Whether the results feel accurate and helpful
        
        **Important:** This study evaluates the tool itself, not your relationship or mental load patterns.
        """)
    
    # Privacy and data
    with st.expander("🔒 Privacy & Data Protection"):
        st.markdown("""
        **What data is collected:**
        - Your responses to pre- and post-surveys (stored in Google Forms)
        - Your questionnaire responses (only if you export the CSV)
        - No identifying information is collected
        
        **The tool itself stores NO data:**
        - Everything in the tool stays in your browser session
        - Data is deleted when you close the browser tab
        - Nothing is sent to any server
        
        **Survey data protection:**
        - Surveys use anonymous Couple IDs you create
        - No names, emails, or identifying information collected
        - Data stored securely in compliance with GDPR
        - Only the researcher and supervisor have access
        - Data will be deleted after thesis completion
        
        **Your Couple ID:**
        You'll create a unique code (like "BlueWhale42") to link your surveys without revealing your identity.
        """)
    
    # Rights
    with st.expander("✋ Your Rights"):
        st.markdown("""
        **Participation is completely voluntary:**
        - You can withdraw at any time without explanation
        - You can skip any questions you're uncomfortable with
        - You can stop using the tool at any point
        
        **No consequences for withdrawing:**
        - There is no penalty or disadvantage for not participating
        - You can request your data be deleted (using your Couple ID)
        
        **Contact information:**
        - Questions about the study: [YOUR_EMAIL]
        - Concerns about ethics: [UNIVERSITY_ETHICS_CONTACT if available]
        """)
    
    # Potential benefits and risks
    with st.expander("⚖️ Potential Benefits & Risks"):
        st.markdown("""
        **Potential benefits:**
        - Gain insight into mental load distribution in your household
        - Have structured conversations about invisible work
        - Receive research-backed conversation prompts
        - Contribute to research on household labour
        
        **Potential risks:**
        - Conversations about household labour may be sensitive
        - You might discover differences in perception
        - Discussions could bring up disagreements
        
        **Safeguards:**
        - The tool encourages kindness and pausing if needed
        - This is NOT a substitute for couples therapy
        - You can stop at any time
        - No pressure to complete if either partner feels uncomfortable
        """)
    
    st.markdown("---")
    
    # Important notes
    st.warning("""
    ⚠️ **This tool is for research purposes and is NOT:**
    - A diagnostic tool for relationship problems
    - A substitute for couples therapy or counselling
    - Professional psychological or medical advice
    
    If you're experiencing relationship distress, please seek support from a qualified professional.
    """)
    
    st.markdown("---")
    
    # Consent checkboxes
    st.markdown("## 🤝 Consent")
    st.markdown("Please confirm the following to participate:")
    
    consent_1 = st.checkbox(
        "I have read and understood the participant information above",
        key="consent_read"
    )
    
    consent_2 = st.checkbox(
        "I understand that participation is voluntary and I can withdraw at any time",
        key="consent_voluntary"
    )
    
    consent_3 = st.checkbox(
        "I understand how my data will be collected, stored, and used",
        key="consent_data"
    )
    
    consent_4 = st.checkbox(
        "I agree to participate in this research study",
        key="consent_participate"
    )
    
    consent_5 = st.checkbox(
        "My partner and I agree to complete this tool together in a respectful manner",
        key="consent_kind"
    )
    
    st.markdown("---")
    
    # Privacy reminder
    st.info("""
    🔒 **Privacy reminder:** This tool stores nothing. All data stays in your browser session. 
    Only the separate surveys (which you'll complete before and after) collect any information.
    """)
    
    # Navigation
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Back to Home", use_container_width=True):
            st.session_state.stage = "home"
            st.rerun()
    
    with col2:
        all_consents_given = all([consent_1, consent_2, consent_3, consent_4, consent_5])
        
        if st.button(
            "Continue to Setup →", 
            disabled=not all_consents_given,
            use_container_width=True,
            type="primary"
        ):
            st.session_state.stage = "setup"
            st.rerun()
        
        if not all_consents_given:
            st.caption("Please confirm all items above to continue")
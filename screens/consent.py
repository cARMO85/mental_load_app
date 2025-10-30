import streamlit as st

def screen_consent():
    """Streamlined consent following layered information model - key info only"""

    # Top-right Home button
    _c1, _c2 = st.columns([6, 1])
    with _c2:
        if st.button("Home", use_container_width=True):
            st.session_state.stage = "home"
            st.rerun()

    # Clear, friendly header
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 style='font-size: 2.2rem; font-weight: 700; margin-bottom: 8px;'>Quick agreement</h1>
        <p style='font-size: 1.1rem; color: #64748b;'>Two things to know before starting</p>
    </div>
    """, unsafe_allow_html=True)

    # Two-column key info - SCANNABLE
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style='background: #f0fdf4; border: 2px solid #86efac; border-radius: 12px; padding: 20px; height: 100%;'>
            <h3 style='font-size: 1rem; margin-bottom: 12px; color: #166534;'>What you'll do</h3>
            <ul style='margin: 0; padding-left: 20px; color: #334155; font-size: 0.95rem;'>
                <li style='margin-bottom: 6px;'><strong>10–15 minutes</strong> answering together</li>
                <li style='margin-bottom: 6px;'><strong>5-page results</strong> to discuss</li>
                <li style='margin-bottom: 0;'><strong>One experiment</strong> to agree on</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background: #fffbeb; border: 2px solid #fde047; border-radius: 12px; padding: 20px; height: 100%;'>
            <h3 style='font-size: 1rem; margin-bottom: 12px; color: #854d0e;'>Your data</h3>
            <ul style='margin: 0; padding-left: 20px; color: #334155; font-size: 0.95rem;'>
                <li style='margin-bottom: 6px;'>Stays in <strong>your browser only</strong></li>
                <li style='margin-bottom: 6px;'><strong>Nothing sent</strong> to any server</li>
                <li style='margin-bottom: 0;'><strong>Gone</strong> when you close the tab</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin: 30px 0 20px;'></div>", unsafe_allow_html=True)

    st.warning("This is for constructive conversations, not blame or therapy. Pause if either of you feels upset. You can stop anytime.")

    st.markdown("<div style='margin: 25px 0 15px;'></div>", unsafe_allow_html=True)

    # Simple agreement checkboxes 
    survey = st.checkbox("We have each completed a pre survey", key="consent_info")
    kind = st.checkbox("We'll be kind and pause if it gets difficult", key="consent_kind")
    consent = st.checkbox("We consent to answer questions and view results together", key="consent_agree")

    st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)

    with st.expander("Full details (optional)"):
        st.markdown("""
        ### About this tool
        **Purpose:** Master's thesis research tool to help couples visualise household mental load and agree a small experiment.  
        **What we collect:** Nothing. All data stays in your browser. No names or emails.  
        **Voluntary:** You can stop at any time.  
        **Risks:** Minimal; choose a good headspace.  
        **Benefits:** Personalised insights and prompts.  
        **Research basis:** Daminger (2019), Dean et al. (2022), Barigozzi et al. (2025).  
        **Contact:** w23045813@northumbrai.ac.uk
        """)

    st.markdown("<div style='margin: 30px 0 10px;'></div>", unsafe_allow_html=True)

    # Big CTA - SINGLE ACTION
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        disabled = not (kind and consent and survey)
        if st.button("Let's begin →", disabled=disabled, use_container_width=True, type="primary"):
            st.session_state.stage = "setup"
            st.rerun()
        st.caption("Tick all three boxes to continue" if disabled else "Ready to start • ~15 minutes together")

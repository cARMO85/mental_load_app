import streamlit as st

def screen_consent():
    """Streamlined consent following layered information model - key info only"""
    
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
            <h3 style='font-size: 1rem; margin-bottom: 12px; color: #166534;'>✅ What you'll do</h3>
            <ul style='margin: 0; padding-left: 20px; color: #334155; font-size: 0.95rem;'>
                <li style='margin-bottom: 6px;'><strong>10-15 minutes</strong> answering together</li>
                <li style='margin-bottom: 6px;'><strong>5-page results</strong> to discuss</li>
                <li style='margin-bottom: 0;'><strong>One experiment</strong> to agree on</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #fffbeb; border: 2px solid #fde047; border-radius: 12px; padding: 20px; height: 100%;'>
            <h3 style='font-size: 1rem; margin-bottom: 12px; color: #854d0e;'>🔒 Your data</h3>
            <ul style='margin: 0; padding-left: 20px; color: #334155; font-size: 0.95rem;'>
                <li style='margin-bottom: 6px;'>Stays in <strong>your browser only</strong></li>
                <li style='margin-bottom: 6px;'><strong>Nothing sent</strong> to any server</li>
                <li style='margin-bottom: 0;'><strong>Gone</strong> when you close the tab</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 30px 0 20px;'></div>", unsafe_allow_html=True)
    
    # Safety note - PROMINENT
    st.warning("""
    ⏸️ **This is for constructive conversations, not blame or therapy.** Pause if either of you feels upset. You can stop anytime.
    """)
    
    st.markdown("<div style='margin: 25px 0 15px;'></div>", unsafe_allow_html=True)
    
    # Simple agreement checkboxes - MINIMAL
    kind = st.checkbox("**We'll be kind and pause if it gets difficult**", key="consent_kind")
    consent = st.checkbox("**We consent to answer questions and view results together**", key="consent_agree")
    
    st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
    
    # Optional details in expander - LAYERED INFO
    with st.expander("📋 Full details (optional - click to read more)"):
        st.markdown("""
        ### About this tool
        
        **Purpose:** This is a research tool developed for a Master's thesis at a Danish university. It helps couples visualise household mental load and agree on small experiments.
        
        **What we collect:** Nothing. All data stays in your browser. We don't collect names, emails, or any identifiable information.
        
        **Voluntary participation:** You can stop at any time and close the browser. There's no penalty for stopping.
        
        **Risks:** Minimal. Some couples may find the questions bring up sensitive topics. We recommend doing this when you're both in a good headspace.
        
        **Benefits:** You'll get personalised insights about your household mental load distribution and research-backed conversation prompts.
        
        **Research basis:** Based on academic research by Daminger (2019), Dean et al. (2022), and Barigozzi et al. (2025) on household cognitive labour.
        
        **Questions?** This tool is not a substitute for couples therapy or counselling. If you're experiencing relationship difficulties, please seek professional support.
        
        **Contact:** [Insert your university email here]
        """)
    
    st.markdown("<div style='margin: 30px 0 10px;'></div>", unsafe_allow_html=True)
    
    # Big CTA - SINGLE ACTION
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        disabled = not (kind and consent)
        if st.button("Let's begin →", disabled=disabled, use_container_width=True, type="primary"):
            st.session_state.stage = "setup"
            st.rerun()
        
        if disabled:
            st.caption("✓ Tick both boxes above to continue")
        else:
            st.caption("Ready to start • 15 minutes together")
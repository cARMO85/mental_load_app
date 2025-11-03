# screens/consent.py
import streamlit as st
from components.navigation import render_navigation


def screen_consent():
    """Consent page with navigation"""
    
    # NAVIGATION HEADER
    render_navigation(
        show_back=False,
        show_home=True,
        show_restart=False
    )
    
    # Simple header
    st.markdown("""
    <div style='text-align: center; margin-bottom: 25px;'>
        <h1 style='font-size: 2rem; font-weight: 700; margin-bottom: 8px;'>Before we start</h1>
        <p style='font-size: 1rem; color: #64748b;'>Quick agreement</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Two key boxes - MINIMAL
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: #f0fdf4; border: 2px solid #86efac; border-radius: 10px; padding: 16px;'>
            <h3 style='font-size: 0.95rem; margin-bottom: 8px; color: #166534;'>✅ What you'll do</h3>
            <p style='margin: 0; color: #334155; font-size: 0.9rem;'>
                <strong>15 minutes</strong> answering together<br/>
                <strong>5-page results</strong> to discuss<br/>
                <strong>One experiment</strong> to try
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #fffbeb; border: 2px solid #fde047; border-radius: 10px; padding: 16px;'>
            <h3 style='font-size: 0.95rem; margin-bottom: 8px; color: #854d0e;'>🔒 Your privacy</h3>
            <p style='margin: 0; color: #334155; font-size: 0.9rem;'>
                Data stays <strong>in your browser</strong><br/>
                <strong>Nothing sent</strong> to any server<br/>
                <strong>Deleted</strong> when you close the tab
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
    
    # Simple agreement
    st.warning("⏸️ This is for constructive conversations, not blame. Pause if it gets difficult.")
    
    st.markdown("<div style='margin: 18px 0 12px;'></div>", unsafe_allow_html=True)
    
    kind = st.checkbox("We'll be kind and pause if needed", key="consent_kind")
    consent = st.checkbox("We consent to answer questions together", key="consent_agree")
    
    st.markdown("<div style='margin: 18px 0;'></div>", unsafe_allow_html=True)
    
    # Optional full details - FIXED TYPO AND ADDED CONTACT
    with st.expander("📋 Full details (optional)"):
        st.markdown("""
        **Purpose:** Research tool for Master thesis. Helps couples visualise mental load and agree on experiments.
        
        **Data:** Nothing collected. All stays in your browser. No names, emails, or tracking.
        
        **Voluntary:** Stop anytime. No penalties.
        
        **Risks:** Minimal. May bring up sensitive topics. Do this when you're both in a good headspace.
        
        **Benefits:** Personalised insights and research-backed conversation prompts.
        
        **Research:** Based on Daminger (2019), Dean et al. (2022), Barigozzi et al. (2025).
        
        **Not a substitute for:** Couples therapy or counselling.
        
        **Contact:** w23056813@northumbria.ac.uk (REPLACE WITH YOUR ACTUAL EMAIL)
        """)
    
    st.markdown("<div style='margin: 22px 0 8px;'></div>", unsafe_allow_html=True)
    
    # CTA
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        disabled = not (kind and consent)
        if st.button("Let's begin →", disabled=disabled, use_container_width=True, type="primary"):
            st.session_state.stage = "setup"
            st.rerun()
        
        if disabled:
            st.caption("✓ Tick both boxes to continue")
        else:
            st.caption("15 minutes • Do it together")
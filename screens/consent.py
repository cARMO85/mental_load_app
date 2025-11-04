# screens/consent.py
import streamlit as st
from components.navigation import render_navigation


def screen_consent():
    """Consent page with navigation"""
    render_navigation(show_back=False, show_home=True, show_restart=False)

    st.markdown("""
    <div style='text-align:center;margin-bottom:20px;'>
      <h1 style='font-size:2rem;font-weight:700;margin-bottom:6px;'>Before we start</h1>
      <p style='font-size:1rem;color:#64748b;'>Please review and confirm the points below</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style='background:#f0fdf4;border:2px solid #86efac;border-radius:10px;padding:16px;'>
          <h3 style='font-size:0.95rem;margin-bottom:8px;color:#166534;'>✅ What you'll do</h3>
          <p style='margin:0;color:#334155;font-size:0.9rem;'>
            <strong>Pre-survey (5 min each)</strong> — completed separately<br/>
            <strong>Use this tool together (15–20 min)</strong><br/>
            <strong>Post-survey (5 min each)</strong> — completed separately
          </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background:#fffbeb;border:2px solid #fde047;border-radius:10px;padding:16px;'>
          <h3 style='font-size:0.95rem;margin-bottom:8px;color:#854d0e;'>🔒 Your privacy</h3>
          <p style='margin:0;color:#334155;font-size:0.9rem;'>
            <strong>This tool</strong>: processes responses locally to show results; it does not store personal identifiers.<br/>
            <strong>Surveys</strong>: completed in Microsoft Forms, configured <em>not</em> to collect names/emails/IPs; responses are stored anonymously in the researcher's university OneDrive.<br/>
            Data are handled in line with <strong>UK GDPR / DPA 2018</strong> and deleted <strong>one month</strong> after project completion.
          </p>
        </div>
        """, unsafe_allow_html=True)

    st.warning("⏸️ This is for constructive conversations, not blame. Pause if it gets difficult.")

    st.markdown("### Consent checklist")

    consent_items = [
        "I have read the Participant Information email that was sent to my inbox (PIS) and understand the study.",
        "I understand participation is voluntary and I may stop any time before submitting my responses.",
        "I understand the surveys are anonymous and no names, emails, or identifiers are collected.",
        "I understand my responses will be processed in accordance with UK GDPR and the Data Protection Act 2018, stored securely, and deleted one month after project completion.",
        "I understand this tool may surface sensitive topics; we will pause if needed.",
        "I consent to take part in this study."
    ]

    ticks = []
    for i, text in enumerate(consent_items):
        ticks.append(st.checkbox(text, key=f"consent_{i}"))

    with st.expander("📋 View the Participant Information Sheet (summary)"):
        st.markdown("""
        **Purpose:** Evaluate a prototype that visualises household mental load to support fairer conversations.  
        **What you'll do:** Pre-survey → use tool together → post-survey.  
        **Risks/benefits:** Minimal risk; may feel sensitive. Potential benefits include insight and improved dialogue.  
        **Data & GDPR:** Anonymous surveys; no identifiers collected. Stored on Northumbria University systems (EU data zone), encrypted; deleted one month post-project. Complies with UK GDPR / DPA 2018.  
        **Contacts:** Researcher: w23056813@northumbria.ac.uk · Supervisor: Dr. Naveed Anwar (Northumbria University)
        """)

    # Optional: link the full PIS PDF you distribute with ethics pack
    st.caption("Docs: PIS v1.0 (Nov 2025) · Consent Form v1.0 (Nov 2025)")

    st.markdown("---")
    all_checked = all(ticks)

    colA, colB, colC = st.columns([1, 2, 1])
    with colB:
        if st.button("I agree — start the tool →", disabled=not all_checked, use_container_width=True, type="primary"):
            st.session_state.stage = "setup"
            st.rerun()
        if not all_checked:
            st.caption("✓ Please review and tick all consent items to continue.")

    st.markdown("<div style='text-align:center;color:#64748b;'>Version 2.0 · November 2025</div>", unsafe_allow_html=True)

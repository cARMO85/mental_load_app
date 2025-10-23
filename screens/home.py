# screens/home.py
import streamlit as st

def screen_home():
    # Hero section
    st.markdown("""
    <div style='text-align: center; padding: 60px 20px 40px;'>
        <h1 style='font-size: 3.5rem; font-weight: 800; margin-bottom: 1rem;'>
            Mental Load Coach
        </h1>
        <p style='font-size: 1.4rem; color: #64748b; margin-bottom: 0.5rem; font-weight: 500;'>
            Make invisible household work visible
        </p>
        <p style='font-size: 1.1rem; color: #94a3b8;'>
            A research tool to help couples discuss cognitive labour
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Three benefits
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 30px 20px;'>
            <div style='font-size: 2.5rem; margin-bottom: 15px; opacity: 0.3;'>📊</div>
            <h3 style='font-size: 1.2rem; margin-bottom: 10px;'>See the Distribution</h3>
            <p style='font-size: 0.95rem; color: #64748b; margin: 0;'>
                Understand who carries which cognitive tasks
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 30px 20px;'>
            <div style='font-size: 2.5rem; margin-bottom: 15px; opacity: 0.3;'>💬</div>
            <h3 style='font-size: 1.2rem; margin-bottom: 10px;'>Start Conversations</h3>
            <p style='font-size: 0.95rem; color: #64748b; margin: 0;'>
                Research-backed discussion prompts
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 30px 20px;'>
            <div style='font-size: 2.5rem; margin-bottom: 15px; opacity: 0.3;'>🔬</div>
            <h3 style='font-size: 1.2rem; margin-bottom: 10px;'>Evidence-Based</h3>
            <p style='font-size: 0.95rem; color: #64748b; margin: 0;'>
                Built on NASA-TLX and mental load research
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin: 50px 0 40px;'></div>", unsafe_allow_html=True)

    # How it works
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h2 style='font-size: 2rem; font-weight: 700; margin-bottom: 10px;'>How It Works</h2>
        <p style='font-size: 1.1rem; color: #64748b;'>Three steps, approximately 20 minutes</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style='padding: 20px;'>
            <div style='width: 50px; height: 50px; background: #3b82f6; color: white; border-radius: 8px;
                        display: flex; align-items: center; justify-content: center; font-size: 1.3rem;
                        font-weight: bold; margin-bottom: 15px;'>1</div>
            <h3 style='font-size: 1.1rem; margin-bottom: 8px;'>Answer Together</h3>
            <p style='color: #64748b; font-size: 0.9rem; margin: 0;'>
                Rate 20-25 household tasks on responsibility, burden, and fairness
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='padding: 20px;'>
            <div style='width: 50px; height: 50px; background: #8b5cf6; color: white; border-radius: 8px;
                        display: flex; align-items: center; justify-content: center; font-size: 1.3rem;
                        font-weight: bold; margin-bottom: 15px;'>2</div>
            <h3 style='font-size: 1.1rem; margin-bottom: 8px;'>Review Results</h3>
            <p style='color: #64748b; font-size: 0.9rem; margin: 0;'>
                Navigate through five pages of personalised insights
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style='padding: 20px;'>
            <div style='width: 50px; height: 50px; background: #10b981; color: white; border-radius: 8px;
                        display: flex; align-items: center; justify-content: center; font-size: 1.3rem;
                        font-weight: bold; margin-bottom: 15px;'>3</div>
            <h3 style='font-size: 1.1rem; margin-bottom: 8px;'>Provide Feedback</h3>
            <p style='color: #64748b; font-size: 0.9rem; margin: 0;'>
                Complete a brief survey about your experience
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin: 60px 0 40px;'></div>", unsafe_allow_html=True)

    # Research context
    st.markdown("## About This Research")
    st.info("""
    **Study Purpose:** This tool is being developed as part of a Master's thesis to explore
    whether digital interventions can facilitate productive dialogue about household cognitive labour.

    **What We're Testing:** Whether this tool helps couples understand and discuss mental load,
    not whether it measures or reduces mental load itself.

    **Your Role:** By participating, you're helping evaluate the tool's usability and effectiveness.
    """)

    # Key info boxes
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style='background: #f0fdf4; border: 2px solid #86efac; border-radius: 12px; padding: 25px;'>
            <h3 style='font-size: 1.1rem; margin-bottom: 15px; color: #166534;'>What You'll Get</h3>
            <ul style='margin: 0; padding-left: 20px; color: #334155; line-height: 1.8;'>
                <li>Responsibility distribution analysis</li>
                <li>Perceived burden assessment</li>
                <li>Research-backed discussion questions</li>
                <li>Downloadable results summary</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background: #fffbeb; border: 2px solid #fde047; border-radius: 12px; padding: 25px;'>
            <h3 style='font-size: 1.1rem; margin-bottom: 15px; color: #854d0e;'>Privacy Guarantee</h3>
            <ul style='margin: 0; padding-left: 20px; color: #334155; line-height: 1.8;'>
                <li>No account or email required</li>
                <li>Data processed in your browser only</li>
                <li>Nothing sent to any server</li>
                <li>Data deleted when you close the tab</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin: 60px 0 30px;'></div>", unsafe_allow_html=True)

    # Important notes
    st.warning("""
    **Please Note:**
    - This is a research tool, not a clinical instrument
    - Not a substitute for couples therapy or counselling
    - Results are based on your subjective perceptions
    - Pause if discussions become difficult
    """)

    st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)

    # CTA
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Begin Study →", use_container_width=True, type="primary"):
            st.session_state.stage = "consent"
            st.rerun()
        st.caption("Approximately 20 minutes • Complete together • Research participation")

    st.markdown("<div style='margin: 60px 0 20px;'></div>", unsafe_allow_html=True)

    # Expandable details
    col1, col2 = st.columns(2)

    with col1:
        with st.expander("Research Information"):
            st.markdown("""
            **Researcher:** Paul Carmody
            **Institution:** Northumbria University
            **Programme:** Master's in [ADD PROGRAMME NAME]
            **Supervisor:** [ADD SUPERVISOR NAME]

            This study has received ethical approval.

            Based on academic research:
            - Daminger (2019): Cognitive dimensions of household labour
            - Hart & Staveland (1988): NASA-TLX workload assessment
            - Dean et al. (2022): Mental load and emotional labour
            """)

    with col2:
        with st.expander("Who Can Participate?"):
            st.markdown("""
            **Inclusion Criteria:**
            - Cohabiting couples (any gender)
            - Both partners present and consenting
            - Able to complete in English
            - Access to computer/tablet

            **Not Suitable For:**
            - Couples in crisis
            - Those seeking clinical intervention
            - Single-person households
            """)

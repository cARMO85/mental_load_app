# screens/home.py
import streamlit as st

def screen_home():
    # Hero section - BIG and clear
    st.markdown("""
    <div style='text-align: center; padding: 60px 20px 40px;'>
        <h1 style='font-size: 3.5rem; font-weight: 800; margin-bottom: 1rem; line-height: 1.1;'>
            You can't share the load<br/>if it's invisible
        </h1>
        <p style='font-size: 1.4rem; color: #64748b; margin-bottom: 2rem; font-weight: 500;'>
            A 20-minute tool to make household mental work visible
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick value props (visual cards) - ORIGINAL GRADIENTS
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 30px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 12px; color: white; min-height: 180px; display: flex; flex-direction: column; justify-content: center;'>
            <div style='font-size: 3rem; margin-bottom: 15px;'>📊</div>
            <h3 style='font-size: 1.2rem; margin-bottom: 10px; color: white;'>See the split</h3>
            <p style='font-size: 0.95rem; margin: 0; opacity: 0.95;'>
                Who's carrying the invisible work?
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 30px 20px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    border-radius: 12px; color: white; min-height: 180px; display: flex; flex-direction: column; justify-content: center;'>
            <div style='font-size: 3rem; margin-bottom: 15px;'>💬</div>
            <h3 style='font-size: 1.2rem; margin-bottom: 10px; color: white;'>Talk it through</h3>
            <p style='font-size: 0.95rem; margin: 0; opacity: 0.95;'>
                Questions, not accusations
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 30px 20px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    border-radius: 12px; color: white; min-height: 180px; display: flex; flex-direction: column; justify-content: center;'>
            <div style='font-size: 3rem; margin-bottom: 15px;'>🧪</div>
            <h3 style='font-size: 1.2rem; margin-bottom: 10px; color: white;'>Try one change</h3>
            <p style='font-size: 0.95rem; margin: 0; opacity: 0.95;'>
                Small experiments, not overhauls
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 50px 0 40px;'></div>", unsafe_allow_html=True)
    
    # How it works - PROFESSIONAL VERSION
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h2 style='font-size: 2rem; font-weight: 700; margin-bottom: 10px;'>How It Works</h2>
        <p style='font-size: 1.1rem; color: #64748b;'>Three steps, approximately 20 minutes</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Three steps - ORIGINAL CIRCLES
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <div style='width: 60px; height: 60px; background: #3b82f6; color: white; border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center; font-size: 1.5rem; 
                        font-weight: bold; margin: 0 auto 15px;'>1</div>
            <h3 style='font-size: 1.1rem; margin-bottom: 8px;'>Answer Together</h3>
            <p style='color: #64748b; font-size: 0.9rem; margin: 0;'>
                Rate 20-25 household tasks on responsibility, burden, and fairness
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <div style='width: 60px; height: 60px; background: #8b5cf6; color: white; border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center; font-size: 1.5rem; 
                        font-weight: bold; margin: 0 auto 15px;'>2</div>
            <h3 style='font-size: 1.1rem; margin-bottom: 8px;'>Review Results</h3>
            <p style='color: #64748b; font-size: 0.9rem; margin: 0;'>
                Navigate through five pages of personalised insights
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <div style='width: 60px; height: 60px; background: #10b981; color: white; border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center; font-size: 1.5rem; 
                        font-weight: bold; margin: 0 auto 15px;'>3</div>
            <h3 style='font-size: 1.1rem; margin-bottom: 8px;'>Provide Feedback</h3>
            <p style='color: #64748b; font-size: 0.9rem; margin: 0;'>
                Complete a brief survey about your experience
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 60px 0 40px;'></div>", unsafe_allow_html=True)
    
    # NEW: Research context section
    st.markdown("## About This Research")
    st.info("""
    **Study Purpose:** This tool is being developed as part of a Master's thesis to explore 
    whether digital interventions can facilitate productive dialogue about household cognitive labour.
    
    **What We're Testing:** Whether this tool helps couples understand and discuss mental load, 
    not whether it measures or reduces mental load itself.
    
    **Your Role:** By participating, you're helping evaluate the tool's usability and effectiveness.
    """)
    
    st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)
    
    # Key promises - ORIGINAL BOXES
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: #f0fdf4; border: 2px solid #86efac; border-radius: 12px; padding: 25px;'>
            <h3 style='font-size: 1.1rem; margin-bottom: 15px; color: #166534;'>✅ What you'll get</h3>
            <ul style='margin: 0; padding-left: 20px; color: #334155;'>
                <li style='margin-bottom: 8px;'>Clear view of who's carrying what</li>
                <li style='margin-bottom: 8px;'>Research-backed conversation questions</li>
                <li style='margin-bottom: 8px;'>Personalised insights you can export</li>
                <li style='margin-bottom: 0;'>One actionable next step</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #fffbeb; border: 2px solid #fde047; border-radius: 12px; padding: 25px;'>
            <h3 style='font-size: 1.1rem; margin-bottom: 15px; color: #854d0e;'>🔒 Privacy promise</h3>
            <ul style='margin: 0; padding-left: 20px; color: #334155;'>
                <li style='margin-bottom: 8px;'>No account or email required</li>
                <li style='margin-bottom: 8px;'>Data stays in your browser only</li>
                <li style='margin-bottom: 8px;'>Nothing sent to any server</li>
                <li style='margin-bottom: 0;'>Gone when you close the tab</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 60px 0 30px;'></div>", unsafe_allow_html=True)
    
    # NEW: Important notes section
    st.warning("""
    **Please Note:**
    - This is a research tool, not a clinical instrument
    - Not a substitute for couples therapy or counselling
    - Results are based on your subjective perceptions
    - Pause if discussions become difficult
    """)
    
    # Pause warning - ORIGINAL
    st.warning("""
    ⏸️ **Pause if either of you is tired, stressed, or hungry right now.** This works best when you're both in a good headspace.
    """)
    
    st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
    
    # CTA - BIG button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Begin Study →", use_container_width=True, type="primary"):
            st.session_state.stage = "consent"
            st.rerun()
        st.caption("20 minutes together • No data stored • Research-based")
    
    st.markdown("<div style='margin: 60px 0 20px;'></div>", unsafe_allow_html=True)
    
    # NEW: Research details and eligibility in expanders
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("🎓 Research Information"):
            st.markdown("""
            **Researcher:** Paul Carmody
            **Institution:** University of Northumbria
            **Programme:** Master's in Computer Science with Data Analytics
            **Supervisor:** Dr. Naveed Anwar

            This study has received ethical approval.
            
            **Based on academic research:**
            - Daminger (2019): Cognitive dimensions of household labour
            - Hart & Staveland (1988): NASA-TLX workload assessment
            - Dean et al. (2022): Mental load and emotional labour
            """)
    
    with col2:
        with st.expander("❓ Who Can Participate?"):
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
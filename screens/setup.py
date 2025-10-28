import streamlit as st
from tasks import get_filtered_tasks

def screen_setup():
    """Clean setup page with better layout"""
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 25px;'>
        <h1 style='font-size: 2rem; font-weight: 700; margin-bottom: 8px;'>Quick setup</h1>
        <p style='font-size: 1rem; color: #64748b;'>Tell us about your household so we show relevant tasks</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 30px 0 20px;'></div>", unsafe_allow_html=True)
    
    # SECTION 1: Children
    st.markdown("### 👨‍👩‍👧‍👦 Children")
    children = st.number_input(
        "How many children live in your household?", 
        min_value=0, 
        max_value=10, 
        step=1, 
        value=st.session_state.get("children", 0),
        help="We'll show child-related tasks if you have children"
    )
    st.session_state.children = children
    
    st.markdown("<div style='margin: 25px 0;'></div>", unsafe_allow_html=True)
    
    # SECTION 2: Employment (side by side)
    st.markdown("### 💼 Employment")
    col1, col2 = st.columns(2)
    
    with col1:
        is_employed_me = st.checkbox(
            "Partner A employed?",
            value=st.session_state.get("is_employed_me", True),
            help="Tick if Partner A has paid employment"
        )
        st.session_state.is_employed_me = is_employed_me
    
    with col2:
        is_employed_partner = st.checkbox(
            "Partner B employed?",
            value=st.session_state.get("is_employed_partner", True),
            help="Tick if Partner B has paid employment"
        )
        st.session_state.is_employed_partner = is_employed_partner
    
    st.markdown("<div style='margin: 25px 0;'></div>", unsafe_allow_html=True)
    
    # SECTION 3: Pets and Vehicle (side by side)
    st.markdown("### 🐾 Pets & 🚗 Vehicle")
    col1, col2 = st.columns(2)
    
    with col1:
        has_pets = st.checkbox(
            "Do you have pets?",
            value=st.session_state.get("has_pets", False),
            help="We'll include pet care tasks"
        )
        st.session_state.has_pets = has_pets
    
    with col2:
        has_vehicle = st.checkbox(
            "Do you have a car/vehicle?",
            value=st.session_state.get("has_vehicle", False),
            help="We'll include vehicle maintenance tasks"
        )
        st.session_state.has_vehicle = has_vehicle
    
    st.markdown("<div style='margin: 30px 0 20px;'></div>", unsafe_allow_html=True)
    
    # Show task count - SIMPLER MESSAGE
    both_employed = is_employed_me and is_employed_partner
    filtered = get_filtered_tasks(children, both_employed, has_pets, has_vehicle)
    
    st.success(f"✅ **{len(filtered)} tasks** selected based on your answers")
    
    st.markdown("<div style='margin: 25px 0;'></div>", unsafe_allow_html=True)
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.stage = "consent"
            st.rerun()
    
    with col2:
        if st.button("Start questionnaire →", type="primary", use_container_width=True):
            # Reset questionnaire state
            st.session_state.responses_dict = {}
            st.session_state.responses = []
            st.session_state.notes_by_section = {}
            st.session_state.stage = "questionnaire"
            st.rerun()
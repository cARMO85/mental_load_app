# screens/setup.py
import streamlit as st
from tasks import get_filtered_tasks
from components.navigation import render_navigation


def screen_setup():
    """Setup page with navigation and +/- buttons for children"""
    
    # NAVIGATION HEADER
    render_navigation(
        show_back=True,
        back_stage="consent",
        back_label="← Back to agreement",
        show_home=True,
        show_restart=False,
        page_title="Setup"
    )
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 25px;'>
        <h1 style='font-size: 2rem; font-weight: 700; margin-bottom: 8px;'>Quick setup</h1>
        <p style='font-size: 1rem; color: #64748b;'>Tell us about your household so we show relevant tasks</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 30px 0 20px;'></div>", unsafe_allow_html=True)
    
    # SECTION 1: Children - CUSTOM +/- BUTTONS
    st.markdown("### 👨‍👩‍👧‍👦 Children")
    
    # Initialize if not set
    if "children" not in st.session_state:
        st.session_state.children = 0
    
    # Create columns for the +/- controls
    col1, col2, col3, col4 = st.columns([1, 1, 2, 3])
    
    with col1:
        if st.button("➖", key="children_minus", use_container_width=True):
            if st.session_state.children > 0:
                st.session_state.children -= 1
                st.rerun()
    
    with col2:
        if st.button("➕", key="children_plus", use_container_width=True):
            if st.session_state.children < 10:
                st.session_state.children += 1
                st.rerun()
    
    with col3:
        # Display the current number prominently
        children_display = st.session_state.children
        if children_display == 0:
            display_text = "No children"
        elif children_display == 1:
            display_text = "1 child"
        else:
            display_text = f"{children_display} children"
        
        st.markdown(f"""
        <div style='background: #f1f5f9; 
                    padding: 8px 16px; 
                    border-radius: 6px; 
                    text-align: center;
                    font-size: 1.1rem;
                    font-weight: 600;
                    margin-top: 4px;'>
            {display_text}
        </div>
        """, unsafe_allow_html=True)
    
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
    
    # Show task count
    both_employed = is_employed_me and is_employed_partner
    filtered = get_filtered_tasks(st.session_state.children, both_employed, has_pets, has_vehicle)
    
    st.success(f"✅ **{len(filtered)} tasks** selected based on your answers")
    
    st.markdown("<div style='margin: 25px 0;'></div>", unsafe_allow_html=True)
    
    # Navigation - ONLY FORWARD BUTTON AT BOTTOM
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("Start questionnaire →", type="primary", use_container_width=True):
            # Reset questionnaire state
            st.session_state.responses_dict = {}
            st.session_state.responses = []
            st.session_state.notes_by_section = {}
            st.session_state.stage = "questionnaire"
            st.rerun()
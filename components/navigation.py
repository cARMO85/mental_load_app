# components/navigation.py
# Reusable navigation header for all pages

import streamlit as st
from state import reset_state

def render_navigation(
    show_back=False, 
    back_stage=None, 
    back_label="← Back",
    show_home=True,
    show_restart=False,
    page_title=None
):
    """
    Render consistent navigation header across all pages
    
    Args:
        show_back: Whether to show back button
        back_stage: Which stage to go back to (e.g., "consent", "setup", "questionnaire")
        back_label: Text for back button
        show_home: Whether to show home button
        show_restart: Whether to show restart button (useful in results)
        page_title: Optional page title to show in center
    """
    
    # Create navigation bar with light background
    st.markdown("""
    <style>
    .nav-container {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 12px 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Determine column layout based on what buttons to show
    if show_back and show_restart:
        cols = st.columns([1, 1, 2, 1])
    elif show_back or show_restart:
        cols = st.columns([1, 2, 1])
    else:
        cols = st.columns([3, 1])
    
    col_index = 0
    
    # Back button
    if show_back and back_stage:
        with cols[col_index]:
            if st.button(back_label, key="nav_back", use_container_width=True):
                st.session_state.stage = back_stage
                st.rerun()
        col_index += 1
    
    # Restart button (mainly for results page)
    if show_restart:
        with cols[col_index]:
            if st.button("🔁 Start Over", key="nav_restart", use_container_width=True):
                if st.session_state.get("confirm_restart", False):
                    reset_state()
                    st.session_state.stage = "home"
                    st.rerun()
                else:
                    st.session_state.confirm_restart = True
                    st.rerun()
        col_index += 1
        
        # Show confirmation if restart was clicked
        if st.session_state.get("confirm_restart", False):
            st.warning("⚠️ Click 'Start Over' again to confirm. This will erase all your answers.")
    
    # Page title (if provided) or spacer
    if page_title:
        with cols[col_index]:
            st.markdown(f"""
            <div style='text-align: center; padding: 8px 0;'>
                <span style='font-weight: 600; color: #475569; font-size: 1rem;'>{page_title}</span>
            </div>
            """, unsafe_allow_html=True)
    col_index += 1
    
    # Home button
    if show_home:
        with cols[-1]:
            if st.button("🏠 Home", key="nav_home", use_container_width=True, type="secondary"):
                # Confirm if they have progress
                if st.session_state.get("responses_dict") and len(st.session_state.responses_dict) > 0:
                    if st.session_state.get("confirm_home", False):
                        st.session_state.stage = "home"
                        st.rerun()
                    else:
                        st.session_state.confirm_home = True
                        st.rerun()
                else:
                    st.session_state.stage = "home"
                    st.rerun()
        
        # Show confirmation if home was clicked with progress
        if st.session_state.get("confirm_home", False):
            st.warning("⚠️ You have unsaved progress. Click 'Home' again to confirm.")
    
    # Reset confirmation flags after showing warning
    if not (show_home or show_restart):
        st.session_state.confirm_home = False
        st.session_state.confirm_restart = False
    
    st.markdown("---")


def render_simple_navigation(current_page, total_pages=None):
    """
    Simpler navigation for results pages with page counter
    
    Args:
        current_page: Current page number
        total_pages: Total number of pages (optional)
    """
    
    cols = st.columns([1, 2, 1])
    
    with cols[0]:
        if st.button("🏠 Home", key="simple_nav_home", use_container_width=True):
            st.session_state.stage = "home"
            st.rerun()
    
    with cols[1]:
        if total_pages:
            st.markdown(f"""
            <div style='text-align: center; padding: 8px 0;'>
                <span style='font-weight: 600; color: #475569;'>Page {current_page} of {total_pages}</span>
            </div>
            """, unsafe_allow_html=True)
    
    with cols[2]:
        if st.button("🔁 Restart", key="simple_nav_restart", use_container_width=True):
            reset_state()
            st.session_state.stage = "home"
            st.rerun()
    
    st.markdown("---")
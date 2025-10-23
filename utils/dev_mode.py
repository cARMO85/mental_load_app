# utils/dev_mode.py
import random
import streamlit as st
from tasks import get_filtered_tasks

def is_dev_mode():
    """Check if dev mode is enabled"""
    return st.session_state.get("dev_mode", False)

def toggle_dev_mode():
    """Toggle dev mode on/off"""
    st.session_state.dev_mode = not st.session_state.get("dev_mode", False)

def generate_sample_responses(scenario="balanced"):
    """
    Generate sample responses for testing
    
    Scenarios:
    - "balanced": Fairly even split (45-55 range)
    - "imbalanced": One partner carries most (70-90 range)
    - "mixed": Mix of balanced and imbalanced tasks
    - "random": Completely random
    """
    children = st.session_state.get("children", 0)
    both_employed = st.session_state.get("is_employed_me", True) and st.session_state.get("is_employed_partner", True)
    
    tasks = get_filtered_tasks(children, both_employed)
    responses = []
    
    for task in tasks:
        if scenario == "balanced":
            # Fairly balanced household
            responsibility = random.randint(40, 60)
            burden = random.randint(2, 4)
            fairness = random.randint(3, 5)
            
        elif scenario == "imbalanced":
            # Partner A carries most of the load
            responsibility = random.randint(10, 35)  # Partner A doing most
            burden = random.randint(3, 5)  # Higher burden
            fairness = random.randint(1, 3)  # Lower fairness
            
        elif scenario == "mixed":
            # Some balanced, some not
            if random.random() < 0.3:  # 30% imbalanced
                responsibility = random.choice([random.randint(10, 30), random.randint(70, 90)])
                burden = random.randint(3, 5)
                fairness = random.randint(2, 4)
            else:  # 70% balanced
                responsibility = random.randint(40, 60)
                burden = random.randint(2, 4)
                fairness = random.randint(3, 5)
                
        else:  # random
            responsibility = random.randint(0, 100)
            burden = random.randint(1, 5)
            fairness = random.randint(1, 5)
        
        responses.append({
            "task_id": task.id,
            "responsibility": responsibility,
            "burden": burden,
            "fairness": fairness,
            "not_applicable": False,
        })
    
    return responses

def populate_dev_data(scenario="balanced"):
    """Populate session state with dev data"""
    st.session_state.responses = generate_sample_responses(scenario)
    st.session_state.notes_by_section = {
        "anticipation": "Dev mode note: This section felt heavy",
        "emotional": "Dev mode note: Lots to discuss here",
    }
    st.success(f"✅ Dev mode: Populated {len(st.session_state.responses)} tasks with '{scenario}' scenario")

def dev_mode_widget():
    """Display dev mode controls in sidebar"""
    if not is_dev_mode():
        return
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🛠️ Dev Mode")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.sidebar.button("Balanced", use_container_width=True):
            populate_dev_data("balanced")
            st.rerun()
    
    with col2:
        if st.sidebar.button("Imbalanced", use_container_width=True):
            populate_dev_data("imbalanced")
            st.rerun()
    
    col3, col4 = st.sidebar.columns(2)
    
    with col3:
        if st.sidebar.button("Mixed", use_container_width=True):
            populate_dev_data("mixed")
            st.rerun()
    
    with col4:
        if st.sidebar.button("Random", use_container_width=True):
            populate_dev_data("random")
            st.rerun()
    
    if st.sidebar.button("Clear All Data", use_container_width=True):
        st.session_state.responses = []
        st.session_state.notes_by_section = {}
        st.success("✅ Cleared all data")
        st.rerun()
    
    st.sidebar.caption(f"📊 {len(st.session_state.get('responses', []))} tasks populated")
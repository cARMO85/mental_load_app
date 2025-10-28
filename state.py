import streamlit as st

def init_state():
    defaults = dict(
        stage="home",
        # setup
        household_type="couple",
        children=0,
        is_employed_me=True,
        is_employed_partner=True,
        has_pets=False, 
        has_vehicle=False, 
        # questionnaire progress
        q_section_index=0,
        q_task_index=0,
        responses=[],
        notes_by_section={},
        questionnaire_start_time=None,
    )
    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def reset_state():
    keys = list(st.session_state.keys())
    for k in keys:
        del st.session_state[k]
    init_state()


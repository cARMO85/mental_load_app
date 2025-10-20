import streamlit as st

def init_state():
    defaults = dict(
        stage="home",
        # setup
        household_type="couple",
        children=0,
        is_employed_me=True,
        is_employed_partner=True,
        # questionnaire progress
        q_section_index=0,
        q_task_index=0,
        responses=[],              # list of dicts {task_id, responsibility, burden, fairness, not_applicable}
        notes_by_section={},       # pillar -> str
    )
    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def reset_state():
    keys = list(st.session_state.keys())
    for k in keys:
        del st.session_state[k]
    init_state()

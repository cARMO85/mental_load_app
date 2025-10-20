import streamlit as st
from tasks import get_filtered_tasks

def screen_setup():
    st.header("Household context (for couples)")
    st.caption("We ask only what’s needed to tailor the questionnaire.")

    c1,c2,c3 = st.columns([2,1,1])
    with c1:
        children = st.number_input("Number of children", min_value=0, max_value=10, step=1, value=st.session_state.children)
        st.session_state.children = children
    with c2:
        st.session_state.is_employed_me = st.checkbox("Partner A employed?", value=st.session_state.is_employed_me)
    with c3:
        st.session_state.is_employed_partner = st.checkbox("Partner B employed?", value=st.session_state.is_employed_partner)

    both_employed = st.session_state.is_employed_me and st.session_state.is_employed_partner
    filtered = get_filtered_tasks(st.session_state.children, both_employed)
    st.success(f"{len(filtered)} items selected for your context. Child-related items only show if you have children; some work items only if both are employed.")

    if st.button("Start questionnaire →", type="primary"):
        st.session_state.q_section_index = 0
        st.session_state.q_task_index = 0
        st.session_state.responses = []
        st.session_state.notes_by_section = {}
        st.session_state.stage = "questionnaire"

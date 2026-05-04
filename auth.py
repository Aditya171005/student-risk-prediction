import streamlit as st

def login():
    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        username = st.text_input("Username")
        if st.button("Login"):
            st.session_state.user = username
            st.success(f"Welcome {username}")
            st.rerun()
        return False
    return True
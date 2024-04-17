import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Midnight Mission Data Dashboard")

st.sidebar.success("Select a page above.")

st.markdown(
    """
    Choose a page on the sidebar to generate charts from data files.
"""
)
import streamlit as st
from functions2 import generate_star_chart, main

st.set_page_config(
    page_title="AstroBoard Events",
    page_icon=":last_quarter_moon:",
    layout="wide",
)   

st.sidebar.header('Filters:')
st.markdown("<h1 style='text-align: center; color: black;'>AstroBoard Events</h1>", unsafe_allow_html=True)


main()


import streamlit as st
from functions import main

st.set_page_config(
    page_title="AstroBoard",
    page_icon=":waning_crescent_moon:",
    layout="wide",
)   

st.sidebar.header('Filters:')
st.markdown("<h1 style='text-align: center; color: black;'>AstroBoard</h1>", unsafe_allow_html=True)

main()

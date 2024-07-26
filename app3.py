import streamlit as st
from functions3 import main

st.set_page_config(
    page_title="AstroBoard Gallery",
    page_icon=":full_moon:",
    layout="wide",
)   
st.markdown("<h1 style='text-align: center; color: black;'>AstroBoard Gallery</h1>", unsafe_allow_html=True)

main()


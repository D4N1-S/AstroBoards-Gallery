import streamlit as st
import pandas as pd
import requests
import altair as alt
from datetime import datetime, timezone
import numpy as np
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import streamlit.components.v1 as components
import json
import base64
from datetime import datetime, timedelta
from PIL import Image
import os
import streamlit as st
from PIL import Image
import os



def load_images_from_folder(folder):
    images = []
    image_files = [f for f in os.listdir(folder) if f.endswith((".jpg", ".png", ".jpeg"))]
    
    # Sort image files by modification time (newest first)
    image_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)), reverse=True)
    
    for filename in image_files:
        img_path = os.path.join(folder, filename)
        img = Image.open(img_path)
        images.append(img)
    
    return images

def display_images(images):
    if images:
        st.write(f"Found {len(images)} images.")
        for img in images:
            st.image(img, use_column_width=True)
    else:
        st.write("No images found in the directory.")

def main():
    st.sidebar.title("Gallery")

    # Dictionary for Wikipedia URLs
    wikipedia_urls = {
        'Rosette Nebula': 'https://en.wikipedia.org/wiki/Rosette_Nebula',
        'Soul Nebula': 'https://en.wikipedia.org/wiki/Soul_Nebula',
        'Horsehead Nebula': 'https://en.wikipedia.org/wiki/Horsehead_Nebula',
        

        'Andromeda Galaxy': 'https://en.wikipedia.org/wiki/Andromeda_Galaxy',
        'M101 (SN 2023ixf)': 'https://en.wikipedia.org/wiki/Pinwheel_Galaxy',


        'Jupiter': 'https://en.wikipedia.org/wiki/Jupiter',
        'Saturn': 'https://en.wikipedia.org/wiki/Saturn'
    }

    # Initialize session state
    if 'selected_folder' not in st.session_state:
        st.session_state.selected_folder = None
        st.session_state.wikipedia_url = None
        st.session_state.show_wikipedia = False

    # Nebula
    with st.sidebar.expander("Nebulae", expanded=False):
        if st.button('Rosette Nebula', key='rosette_nebula'):
            st.session_state.selected_folder = r"J:\Astronomy\Deepsky images (2023)\Esprit 100ED\Nebula\Rosette Nebula"
            st.session_state.wikipedia_url = wikipedia_urls['Rosette Nebula']
            st.session_state.show_wikipedia = False
        
        if st.button('Soul Nebula', key='soul_nebula'):
            st.session_state.selected_folder = r"J:\Astronomy\Deepsky images (2023)\Esprit 100ED\Nebula\Soul Nebula"
            st.session_state.wikipedia_url = wikipedia_urls['Soul Nebula']
            st.session_state.show_wikipedia = False
        
        if st.button('Horsehead Nebula', key='horsehead_nebula'):
            st.session_state.selected_folder = r"J:\Astronomy\Deepsky images (2023)\Esprit 100ED\Nebula\Horsehead Nebula"
            st.session_state.wikipedia_url = wikipedia_urls['Horsehead Nebula']
            st.session_state.show_wikipedia = False

    # Galaxies
    with st.sidebar.expander("Galaxies", expanded=False):
        if st.button('Andromeda Galaxy', key='andromeda_galaxy'):
            st.session_state.selected_folder = r"J:\Astronomy\Deepsky images (2023)\Esprit 100ED\Galaxies\M31 Andromeda"
            st.session_state.wikipedia_url = wikipedia_urls['Andromeda Galaxy']
            st.session_state.show_wikipedia = False
        
        if st.button('M101 (SN 2023ixf)', key='M101 (SN 2023ixf)'):
            st.session_state.selected_folder = r"J:\Astronomy\Deepsky images (2023)\Esprit 100ED\Galaxies\M101 (SN 2023ixf)"
            st.session_state.wikipedia_url = wikipedia_urls['M101 (SN 2023ixf)']
            st.session_state.show_wikipedia = False

    # Planets
    with st.sidebar.expander("Planets", expanded=False):
        if st.button('Jupiter', key='jupiter'):
            st.session_state.selected_folder = r"J:\Astronomy\Deepsky images (2023)\Esprit 100ED\Planets\Jupiter"
            st.session_state.wikipedia_url = wikipedia_urls['Jupiter']
            st.session_state.show_wikipedia = False
        
        if st.button('Saturn', key='saturn'):
            st.session_state.selected_folder = r"J:\Astronomy\Deepsky images (2023)\Esprit 100ED\Planets\Saturn"
            st.session_state.wikipedia_url = wikipedia_urls['Saturn']
            st.session_state.show_wikipedia = False

    # "More Info" button to show/hide Wikipedia iframe
    if st.session_state.selected_folder:
        #st.write("### More Info")
        if st.button('Object Information'):
            # Toggle the visibility of the Wikipedia widget
            st.session_state.show_wikipedia = not st.session_state.show_wikipedia
        
        if st.session_state.show_wikipedia and st.session_state.wikipedia_url:
            st.markdown(f'<iframe src="{st.session_state.wikipedia_url}" width="100%" height="600"></iframe>', unsafe_allow_html=True)
        
        images = load_images_from_folder(st.session_state.selected_folder)
        display_images(images)
    else:
        st.write("Select a category and image set from the sidebar.")

if __name__ == "__main__":
    main()


























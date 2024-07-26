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


def generate_star_chart(latitude, longitude, date, style=None, view_type=None, view_parameters=None):
    url = "https://api.astronomyapi.com/api/v2/studio/star-chart"

    # Encode the application ID and application secret using Base64
    application_id = "9e1af404-eea9-4ee2-91b1-09aeef7ad290"
    application_secret = "e1cf68ed69cee7f0c1c1f4dee5429ae8de1e63a2afdf220878a7eae63b889158891eaba924173717936dda378c837ff35e2f77248866ceacbcd1d9cdd538b4734a16cb6845c56f4f239a4e183cadf19a780f00d42609d9616127879cf7efb3f73ae2b210639599f16159a77f2ddf5133"
    credentials = f"{application_id}:{application_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    # Set up the headers with the Authorization header
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }

    # Create the request body
    request_body = {
        "style": style,
        "observer": {
            "latitude": latitude,
            "longitude": longitude,
            "date": date
        },
        "view": {
            "type": view_type,
            "parameters": view_parameters
        }
    }

    # Send the POST request to the API
    response = requests.post(url, headers=headers, json=request_body)

    if response.status_code == 200:
        data = response.json()
        return data["data"]["imageUrl"]
    else:
        st.error(f"Error: {response.status_code}")
        return None

def main():
    latitude = 0  # Default latitude
    longitude = 0  # Default longitude
    date = "2024-06-02"
    style = "inverted"
    view_type = "constellation"
    view_parameters = {"constellation": "ori"}

    st.title("Generate Star Chart")

    # Define locations with latitude and longitude
    locations = {
        "Duizel": (51.373, 5.303),
        "Autry": (50.04, 4.91),
        "Kirchlotheim": (50.08, 9.14),
        "La Palma": (28.67, -17.78)
    }

    # Create a selectbox in the sidebar for the user to select a location
    selected_location = st.sidebar.selectbox("Select Location", list(locations.keys()))

    # Get latitude and longitude based on the selected location
    latitude, longitude = locations[selected_location]

    # Generate star chart
    star_chart_url = generate_star_chart(latitude, longitude, date, style, view_type, view_parameters)
    if star_chart_url:
        st.success("Star chart generated successfully:")
        st.image(star_chart_url)
    else:
        st.error("Failed to generate star chart.")

if __name__ == "__main__":
    main()

























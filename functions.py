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
#from bs4 import BeautifulSoup
#from io import BytesIO
#from PIL import Image
#import urllib.parse


locations = {
    "Duizel": {
        "satellite": "https://widgets.meteox.com/en-GB/widgets/radar/location/8877/satellite",
        "rain": "https://widgets.meteox.com/en-GB/widgets/radar/location/8877/rain"
    },
    "Autry": {
        "satellite": "https://widgets.meteox.com/en-GB/widgets/radar/location/3022874/satellite",
        "rain": "https://widgets.meteox.com/en-GB/widgets/radar/location/3022874/rain"
    },
    "Kirchlotheim": {
        "satellite": "https://widgets.meteox.com/en-GB/widgets/radar/location/2879766/satellite",
        "rain": "https://widgets.meteox.com/en-GB/widgets/radar/location/2879766/rain"
    },
    "La Palma": {
        "satellite": "https://widgets.meteox.com/en-GB/widgets/radar/location/8000097/satellite",
        "rain": "https://widgets.meteox.com/en-GB/widgets/radar/location/8000097/rain"
    },
}

locations2 = {
        "Duizel": (51.373, 5.303),
        "Autry": (50.04, 4.91),
        "Kirchlotheim": (50.08, 9.14),
        "La Palma": (28.67, -17.78)
    }

targets = {
        "NGC 7129": (),
        "Cocoon Nebula": (),
        "": (),
        "": ()
    }

def apply_color_cloud(val):
    if val >= 50:
        color = 'red'
    elif val >= 20:
        color = 'orange'
    else:
        color = 'green'
    return f'background-color: {color}'

def apply_color_humidity(val):
    if val >= 90:
        color = 'red'
    elif val >= 75:
        color = 'orange'
    else:
        color = 'green'
    return f'background-color: {color}'

def apply_color_windspeed(val):
    if val >= 15:
        color = 'red'
    elif val >= 10:
        color = 'orange'
    else:
        color = 'green'
    return f'background-color: {color}'

def apply_color_visibility(val):
    if val >= 10:
        color = 'green'
    elif val >= 5:
        color = 'orange'
    else:
        color = 'red'
    return f'background-color: {color}'

def highlight_time_T00(val):
    if 'T00:00' in val:
        return 'background-color: yellow'
    return ''

# Function to get Moon Phase data for a given date
def get_moon_phase(date):
    try:
        url = f"https://api.usno.navy.mil/moon/phase?date={date}&nump=1"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        phase = data['phasedata'][0]['phase']
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching Moon Phase data: {e}")
        phase = "Unknown"
    return phase


def main():

    # Create a selectbox in the sidebar for the user to select a location
    selected_location = st.sidebar.selectbox("Location Maps", list(locations.keys()))
    selected_location2 = st.sidebar.selectbox("Location Info", list(locations2.keys()))

    # Get the iframe URLs for the selected location
    satellite_url = locations[selected_location]["satellite"]
    rain_url = locations[selected_location]["rain"]

    # Create two columns
    col1, col2 = st.columns(2)

    # Embed the first iframe in the first column
    with col1:
        components.html(
            f"""
            <iframe sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox" src="{satellite_url}" 
            style="width:100%; height:600px; border:none; padding:0; margin:0;" scrolling="no" frameborder="0"></iframe>
            """,
            height=600
        )

    # Embed the second iframe in the second column
    with col2:
        components.html(
            f"""
            <iframe sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox" src="{rain_url}" 
            style="width:100%; height:600px; border:none; padding:0; margin:0;" scrolling="no" frameborder="0"></iframe>
            """,
            height=600
        )

    # Define your API key and endpoint for Open-Meteo API
    latitude, longitude = locations2[selected_location2]
    api_endpoint = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relative_humidity_2m,dew_point_2m,precipitation_probability,precipitation,rain,cloud_cover,cloud_cover_low,cloud_cover_mid,cloud_cover_high,visibility,wind_speed_10m,wind_direction_10m"
    
    # Fetch data from Open-Meteo API
    response = requests.get(api_endpoint)
    
    # Check if request was successful
    if response.status_code == 200:
        data = response.json()
        hourly_forecast = data.get('hourly', [])
        
        # Extract relevant data
        df = pd.DataFrame(hourly_forecast)
        df = df[['time', 'cloud_cover', 'cloud_cover_low', 'cloud_cover_mid', 'cloud_cover_high', 'precipitation_probability', 'precipitation', 'rain', 'relative_humidity_2m', 'wind_speed_10m', 'visibility', 'temperature_2m']]
        df['visibility'] = df['visibility'] / 1000

        # Rename columns
        df = df.rename(columns={
            'time': 'Time & Date',
            'temperature_2m': 'Temperature (°C)',
            'relative_humidity_2m': 'Relative Humidity (%)',
            'dew_point_2m': 'Dew Point (°C)',
            'precipitation_probability': 'Precipitation Probability (%)',
            'precipitation': 'Precipitation (mm)',
            'rain': 'Rain (mm)',
            'cloud_cover': 'Total Cloud Cover (%)',
            'cloud_cover_low': 'Low Cloud Cover (%)',
            'cloud_cover_mid': 'Mid Cloud Cover (%)',
            'cloud_cover_high': 'High Cloud Cover (%)',
            'visibility': 'Visibility (km)',
            'wind_speed_10m': 'Wind Speed (m/s)'
        })

        # Apply color to specific columns
        color_columns_cloud = ['Total Cloud Cover (%)', 'Low Cloud Cover (%)', 'Mid Cloud Cover (%)', 'High Cloud Cover (%)']
        color_columns_humidity = ['Relative Humidity (%)']
        color_columns_windspeed = ['Wind Speed (m/s)']
        color_columns_visibility = ['Visibility (km)']
        df_styled = df.style.applymap(apply_color_cloud, subset=color_columns_cloud)
        df_styled = df_styled.applymap(apply_color_humidity, subset=color_columns_humidity)
        df_styled = df_styled.applymap(apply_color_windspeed, subset=color_columns_windspeed)
        df_styled = df_styled.applymap(apply_color_visibility, subset=color_columns_visibility)

        # Highlight rows with 'T00:00' in the Time column
        df_styled = df_styled.applymap(highlight_time_T00, subset=['Time & Date'])
        
        # Display the styled DataFrame
        st.dataframe(df_styled.set_properties(**{'text-align': 'center'}), height=800)

        st.sidebar.markdown("Other sources")
        st.sidebar.markdown(
            """
            <div style="display: flex; flex-direction: column; align-items: flex-start;">
                <a href="https://www.sat24.com/en-gb/country/be#selectedLayer=euMicro" target="_blank">
                    <button style="background-color:Blue;padding:10px;border-radius:10px;color:white;margin-bottom: 10px;">
                        24sat
                    </button>
                </a>
                <a href="https://www.buienradar.nl/" target="_blank">
                    <button style="background-color:Blue;padding:10px;border-radius:10px;color:white;margin-bottom: 10px;">
                        Buienradar
                    </button>
                </a>
                <a href="https://clearoutside.com/forecast/51.37/5.30" target="_blank">
                    <button style="background-color:Blue;padding:10px;border-radius:10px;color:white;margin-bottom: 10px;">
                        Clearoutside
                    </button>
                </a>
                <a href="https://www.buienalarm.nl/duizel-noord-brabant-nederland/51.36833,5.29722" target="_blank">
                    <button style="background-color:Blue;padding:10px;border-radius:10px;color:white;margin-bottom: 10px;">
                        Buienalarm
                    </button>
                </a>
                <a href="https://www.meteoblue.com/en/weather/forecast/multimodel/51.37N5.302E27_Europe%2FAmsterdam/" target="_blank">
                    <button style="background-color:Blue;padding:10px;border-radius:10px;color:white;margin-bottom: 10px;">
                        Meteoblue
                    </button>
                    </a>
                <a href="https://stellarium-web.org/" target="_blank">
                    <button style="background-color:Blue;padding:10px;border-radius:10px;color:white;margin-bottom: 10px;">
                        Stellarium
                    </button>
                    </a>
                <a href="https://gong2.nso.edu/products/tableView/table.php?configFile=configs/hAlpha.cfg" target="_blank">
                    <button style="background-color:Blue;padding:10px;border-radius:10px;color:white;margin-bottom: 30px;">
                        Solar activity
                    </button>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

        selected_location3 = st.sidebar.selectbox("Targets", list(targets.keys()))

    st.write("Add 2 hours for the moonrise & moonset")
    st.write("""
    <iframe src="https://moonphases.co.uk/" width="100%" height="600"></iframe>
""", unsafe_allow_html=True)


if __name__ == "__main__":
    main()

























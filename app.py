import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Railway Station Facility Finder & Navigation", layout="centered")

st.title("🚉 Railway Station Facility Finder & Navigation")

# Get dataset path from user input
csv_path = st.text_input("Enter path to your railway facilities CSV:", "large_railway_facilities_dataset (1).csv")

# Load CSV only if the file exists
try:
    df = pd.read_csv(csv_path)

    # ✅ Rename columns to match the expected names
    df.rename(columns={
        'X': 'Latitude',
        'Y': 'Longitude',
        'Station': 'Station Name',
        'Facility Type': 'Facility Name'
    }, inplace=True)

    # Ensure required columns exist
    required_cols = ['Facility Name', 'Latitude', 'Longitude', 'Station Name']
    if not all(col in df.columns for col in required_cols):
        missing = [col for col in required_cols if col not in df.columns]
        st.error(f"Missing columns in dataset: {', '.join(missing)}")
    else:
        # Sidebar inputs for location
        st.sidebar.header("📍 Enter Your Location")
        user_lat = st.sidebar.number_input("Latitude", value=0.0, format="%.6f")
        user_lon = st.sidebar.number_input("Longitude", value=0.0, format="%.6f")

        # Use session state to retain map visibility
        if "show_result" not in st.session_state:
            st.session_state.show_result = False

        if st.sidebar.button("Find Nearest Facility"):
            if user_lat == 0.0 and user_lon == 0.0:
                st.error("❗ Please enter valid latitude and longitude.")
                st.session_state.show_result = False
            else:
                st.session_state.show_result = True
                df["Distance"] = df.apply(
                    lambda row: np.sqrt((user_lat - row["Latitude"])**2 + (user_lon - row["Longitude"])**2),
                    axis=1
                )
                nearest = df.loc[df["Distance"].idxmin()]
                st.session_state.nearest = nearest

        # Display result if user clicked the button
        if st.session_state.show_result:
            nearest = st.session_state.nearest
            st.success(f"✅ Nearest Facility: {nearest['Facility Name']}")
            st.write(f"📍 Station: {nearest['Station Name']}")
            st.write(f"🧭 Location: ({nearest['Latitude']}, {nearest['Longitude']})")

            m = folium.Map(location=[user_lat, user_lon], zoom_start=14)
            folium.Marker(
                location=[user_lat, user_lon],
                tooltip="Your Location",
                icon=folium.Icon(color='red')
            ).add_to(m)
            folium.Marker(
                location=[nearest["Latitude"], nearest["Longitude"]],
                popup=f"{nearest['Facility Name']} - {nearest['Station Name']}",
                tooltip="Nearest Facility",
                icon=folium.Icon(color='blue')
            ).add_to(m)

            st_folium(m, width=700, height=500)

except FileNotFoundError:
    st.error("❌ The specified file was not found. Please check the path.")
except pd.errors.ParserError:
    st.error("❌ There was a problem parsing the CSV file.")
except Exception as e:
    st.error(f"❌ Error loading or processing dataset: {e}")

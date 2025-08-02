import pandas as pd
import folium
import os
import webbrowser

# ✅ Step 1: Load the CSV dataset
file_path = r"C:\Users\sachi\OneDrive\Desktop\model\large_railway_facilities_dataset (1).csv"

try:
    df = pd.read_csv(file_path, encoding='utf-8')

    # ✅ Step 2: Rename columns (standardize for mapping)
    df.rename(columns={
        'X': 'Latitude',
        'Y': 'Longitude',
        'Station': 'Station Name',
        'Facility Type': 'Facility Name'  # Adjust if already named correctly
    }, inplace=True)

    # ✅ Step 3: Validate necessary columns
    required_columns = {'Station Name', 'Facility Name', 'Latitude', 'Longitude'}
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        raise ValueError(f"Missing columns in dataset: {', '.join(missing)}")

    # ✅ Step 4: Drop rows with missing coordinates
    df.dropna(subset=["Latitude", "Longitude"], inplace=True)

    # ✅ Step 5: Create the base map centered at the first entry
    if df.empty:
        raise ValueError("No valid location data available in dataset.")
    
    map_center = [df.iloc[0]["Latitude"], df.iloc[0]["Longitude"]]
    m = folium.Map(location=map_center, zoom_start=6, tiles='OpenStreetMap')

    # ✅ Step 6: Add a marker for each facility
    for _, row in df.iterrows():
        popup_text = f"""
        <b>Facility:</b> {row['Facility Name']}<br>
        <b>Station:</b> {row['Station Name']}
        """
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=row["Facility Name"],
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

    # ✅ Step 7: Save map to HTML file
    output_file = "railway_facilities_map.html"
    m.save(output_file)

    # ✅ Step 8: Open the map in default web browser
    webbrowser.open('file://' + os.path.realpath(output_file))
    print("✅ Map generated and opened successfully.")

except FileNotFoundError:
    print(f"❌ File not found at: {file_path}")
except Exception as e:
    print(f"❌ An error occurred: {e}")

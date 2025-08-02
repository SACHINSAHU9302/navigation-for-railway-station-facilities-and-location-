import tkinter as tk
from tkinter import messagebox
import pandas as pd
from geopy.distance import geodesic
from sklearn.preprocessing import LabelEncoder

# Load and preprocess data
csv_file = r"D:\CODING\minorproject\Dataset\navigation_railway_facilities.csv"
df = pd.read_csv(csv_file)

# Encode categorical columns
label_encoders = {}
for col in ['Facility Name', 'Facility Type', 'Accessibility']:
    if col in df.columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

# Function to find nearest facility
def find_nearest_facility(user_lat, user_long):
    df['Distance'] = df.apply(lambda row: geodesic((user_lat, user_long), (row['Latitude'], row['Longitude'])).meters, axis=1)
    nearest = df.loc[df['Distance'].idxmin()]
    return nearest

# GUI logic
def get_facility():
    try:
        lat = float(entry_lat.get())
        lon = float(entry_lon.get())
        nearest = find_nearest_facility(lat, lon)
        decoded = nearest.copy()

        for col in ['Facility Name', 'Facility Type', 'Accessibility']:
            if col in label_encoders:
                decoded[col] = label_encoders[col].inverse_transform([int(decoded[col])])[0]

        result_text = (
            f"Nearest Facility:\n\n"
            f"Facility Name: {decoded['Facility Name']}\n"
            f"Facility Type: {decoded['Facility Type']}\n"
            f"Latitude: {decoded['Latitude']}\n"
            f"Longitude: {decoded['Longitude']}\n"
            f"Accessibility: {decoded['Accessibility']}\n"
            f"Distance (m): {decoded['Distance']:.2f}"
        )
        messagebox.showinfo("Result", result_text)
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input or missing data.\n\n{e}")

# Create window
root = tk.Tk()
root.title("Railway Facility Finder")
root.geometry("400x300")
root.configure(bg="lightblue")

# Labels and inputs
tk.Label(root, text="Enter Your Latitude:", bg="lightblue", font=("Arial", 12)).pack(pady=10)
entry_lat = tk.Entry(root, font=("Arial", 12))
entry_lat.pack()

tk.Label(root, text="Enter Your Longitude:", bg="lightblue", font=("Arial", 12)).pack(pady=10)
entry_lon = tk.Entry(root, font=("Arial", 12))
entry_lon.pack()

tk.Button(root, text="Find Nearest Facility", font=("Arial", 12), command=get_facility).pack(pady=20)

# Run the GUI
root.mainloop()

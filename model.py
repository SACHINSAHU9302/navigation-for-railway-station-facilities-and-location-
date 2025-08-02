import os
import pandas as pd
import numpy as np
from geopy.distance import geodesic
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import LabelEncoder

def load_data(csv_file=None):
    """Load railway station facilities data from CSV."""
    if not csv_file:
        csv_file = "large_railway_facilities_dataset (1).csv"
    return pd.read_csv(csv_file)

def preprocess_data(df):
    """Encode categorical columns into numerical values."""
    label_encoders = {}
    categorical_cols = ['Facility Name', 'Facility Type', 'Accessibility']
    
    for col in categorical_cols:
        if col in df.columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            label_encoders[col] = le
        else:
            print(f"Warning: '{col}' column not found in dataset. Skipping.")
    
    return df, label_encoders

def train_ml_model(df):
    """Train a Machine Learning model to recommend facilities."""
    X = df[['Latitude', 'Longitude']]
    y = df['Facility Type']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def train_dl_model(df):
    """Train a Deep Learning model for facility classification."""
    X = df[['Latitude', 'Longitude']].values
    y = df['Facility Type'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = keras.Sequential([
        layers.Dense(32, activation='relu', input_shape=(2,)),
        layers.Dense(16, activation='relu'),
        layers.Dense(len(set(y)), activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=50, batch_size=10, verbose=1)
    return model

def find_nearest_facility(df, user_lat, user_long):
    """Find the nearest facility based on user coordinates."""
    df['Distance'] = df.apply(lambda row: geodesic((user_lat, user_long), (row['Latitude'], row['Longitude'])).meters, axis=1)
    nearest = df.loc[df['Distance'].idxmin()]
    return nearest

if __name__ == "__main__":
    csv_file = r"D:\CODING\minorproject\Dataset\navigation_railway_facilities.csv"
    
    # Load and preprocess data
    df = load_data(csv_file)
    df, label_encoders = preprocess_data(df)

    print("Training Machine Learning Model...")
    ml_model = train_ml_model(df)

    print("Training Deep Learning Model...")
    dl_model = train_dl_model(df)

    #  ✅Save the trained DL model as .h5
    model_path = r"C:\Users\sachi\OneDrive\Desktop\model\minor_project_model.h5"
    dl_model.save(model_path)
    print(f"✅ Model saved to: {model_path}")

    # Get user location
    user_lat = float(input("Enter your latitude: "))
    user_long = float(input("Enter your longitude: "))

    # Find and decode nearest facility
    nearest_facility = find_nearest_facility(df, user_lat, user_long)
    decoded = nearest_facility.copy()

    for col in ['Facility Name', 'Facility Type', 'Accessibility']:
        if col in label_encoders:
            decoded[col] = label_encoders[col].inverse_transform([int(decoded[col])])[0]

    print("\n🔎 Nearest Facility Details (Decoded):")
    print(f"Facility Name: {decoded['Facility Name']}")
    print(f"Facility Type: {decoded['Facility Type']}")
    print(f"Latitude: {decoded['Latitude']}")
    print(f"Longitude: {decoded['Longitude']}")
    print(f"Accessibility: {decoded['Accessibility']}")
    print(f"Distance (m): {decoded['Distance']:.2f}")


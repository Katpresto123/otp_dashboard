import zipfile
import os
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


# Load data function with caching
@st.cache_data
def load_gtfs_data():
    # Define the zip file path
    zip_file = 'stop_times.zip'  # Your ZIP file containing stop_times.txt

    # Extract stop_times.txt if the ZIP file exists and is valid
    if zipfile.is_zipfile(zip_file):
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extract('stop_times.txt', path='.')  # Extract only stop_times.txt
    else:
        st.error(f"{zip_file} is not a valid ZIP file or doesn't exist!")
        st.stop()

    # Check if the necessary files exist
    if not os.path.isfile('stop_times.txt'):
        st.error("stop_times.txt not found!")
        st.stop()

    if not os.path.isfile('stops.txt'):
        st.error("stops.txt not found in the repository!")
        st.stop()

    if not os.path.isfile('trips.txt'):
        st.error("trips.txt not found in the repository!")
        st.stop()

    # Load the data from the extracted and existing CSV files
    stop_times = pd.read_csv('stop_times.txt')
    stops = pd.read_csv('stops.txt')
    trips = pd.read_csv('trips.txt')

    # Merge datasets and perform data transformations
    stops['stop_id'] = stops['stop_id'].astype(str)
    stop_times['stop_id'] = stop_times['stop_id'].astype(str)

    stop_times_trips = stop_times.merge(trips, on="trip_id")
    otp_data = stop_times_trips.merge(stops, on="stop_id")

    otp_data['arrival_time'] = pd.to_datetime(otp_data['arrival_time'], format='%H:%M:%S', errors='coerce')
    random_delays = np.random.randint(-60, 300, size=len(otp_data))
    otp_data['actual_arrival']

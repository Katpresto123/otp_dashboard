import zipfile
import os
import pandas as pd
import streamlit as st
import numpy as np

# Load data function with caching
@st.cache_data
def load_gtfs_data():
    # Define the zip file path
    zip_file = 'stop_times.txt.zip'
    
    # Check if the zip file exists and is valid
    if not zipfile.is_zipfile(zip_file):
        st.error(f"Error: {zip_file} is not a valid zip file!")
        st.stop()

    # Extract the files from the zip
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_contents = zip_ref.namelist()  # Get the list of files in the zip archive

        # Check for necessary files and extract them
        files_to_extract = ['stop_times.txt', 'stops.txt', 'trips.txt']
        for file in files_to_extract:
            if file in zip_contents:
                zip_ref.extract(file)
            else:
                st.error(f"{file} not found in the zip file!")
                st.stop()

    # After extraction, check if the files exist
    if not os.path.isfile('stop_times.txt'):
        st.error("stop_times.txt not found!")
        st.stop()

    if not os.path.isfile('stops.txt'):
        st.error("stops.txt not found!")
        st.stop()

    if not os.path.isfile('trips.txt'):
        st.error("trips.txt not found!")
        st.stop()

    # Load the data from the extracted CSV files
    try:
        stops = pd.read_csv('stops.txt')
        stop_times = pd.read_csv('stop_times.txt')
        trips = pd.read_csv('trips.txt')

        # Convert stop_id and arrival_time to string for consistent merging
        stops['stop_id'] = stops['stop_id'].astype(str)
        stop_times['stop_id'] = stop_times['stop_id'].astype(str)

        # Merge datasets
        stop_times_trips = stop_times.merge(trips, on="trip_id")
        otp_data = stop_times_trips.merge(stops, on="stop_id")

        # Convert arrival_time to datetime
        otp_data['arrival_time'] = pd.to_datetime(otp_data['arrival_time'], format='%H:%M:%S', errors='coerce')

        # Check the length of otp_data and generate random delays
        num_rows = len(otp_data)
        if num_rows > 0:
            # Simulate actual arrival times with delay (in seconds)
            random_delays = np.random.randint(-60, 300, size=num_rows)  # Ensure this matches the length of otp_data
            otp_data['actual_arrival_time'] = otp_data['arrival_time'] + pd.to_timedelta(random_delays, unit='s')
        else:
            st.error("No data available to process.")
            return None  # Return None if there is no data to process

        # Calculate delay and categorize on-time or late
        otp_data['delay_seconds'] = (otp_data['actual_arrival_time'] - otp_data['arrival_time']).dt.total_seconds()
        otp_data['on_time'] = otp_data['delay_seconds'].between(-60, 300)

        return otp_data

    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()


# Streamlit app starts here
st.title("TriMet On-Time Performance Dashboard")

# Load the data
try:
    otp_data = load_gtfs_data()
    st.success("Data loaded successfully!")
except FileNotFoundError as e:
    st.error(f"File not found: {e}")
    st.stop()

# Show the data
st.subheader("Preview of Merged Data")
st.dataframe(otp_data.head())

# Enhanced Interactivity with More Filters
stop_ids = otp_data['stop_id'].unique()
selected_stop_id = st.selectbox("Select a Stop ID", stop_ids)

route_ids = otp_data['route_id'].unique()
selected_route_id = st.selectbox("Select a Route ID", route_ids)

# Apply both filters
filtered_data = otp_data[(otp_data['stop_id'] == selected_stop_id) & 
                         (otp_data['route_id'] == selected_route_id)]

st.write(f"Filtered Data for Stop ID: {selected_stop_id} and Route ID: {selected_route_id}")
st.dataframe(filtered_data)

# Calculate OTP percentage
otp_percentage = otp_data['on_time'].mean() * 100

# OTP Visualization
st.subheader("On-Time Performance")
fig, ax = plt.subplots(figsize=(6, 4))
otp_data['on_time'].value_counts().plot(kind='bar', color=['green', 'red'], ax=ax)
ax.set_title("On-Time vs. Late")
ax.set_ylabel("Count")
ax.set_xticklabels(["On-Time", "Late"], rotation=0)
st.pyplot(fig)

# Group by route and stop to calculate average delays
patterns = otp_data.groupby(['route_id', 'stop_id']).agg(
    avg_delay=('delay_seconds', 'mean'),
    on_time_percentage=('on_time', 'mean')
).reset_index()

# Slider for threshold
threshold = st.slider("On-Time Threshold (%)", min_value=50, max_value=100, value=80)
poor_performance = patterns[patterns['on_time_percentage'] < (threshold / 100)]

# Display poor-performing stops or routes
st.subheader("Stops with Poor Performance")
st.dataframe(poor_performance)

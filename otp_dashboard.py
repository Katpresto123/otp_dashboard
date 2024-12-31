import zipfile
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import os

# Load data function with caching
@st.cache_data
def load_gtfs_data(zip_file='stop_times.zip'):
    # Check if ZIP file exists
    if not os.path.isfile(zip_file):
        st.error(f"{zip_file} not found!")
        st.stop()

    # Extract the stop_times.txt file from the ZIP archive
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        if 'stop_times.txt' not in zip_ref.namelist():
            st.error("stop_times.txt not found in the ZIP archive!")
            st.stop()
        zip_ref.extract('stop_times.txt', path='.')

    # Load the stop_times.txt file
    stop_times = pd.read_csv('stop_times.txt')

    # Simulate arrival times (if applicable)
    stop_times['arrival_time'] = pd.to_datetime(stop_times['arrival_time'], format='%H:%M:%S', errors='coerce')

    # Simulate actual arrival times with delays (in seconds)
    stop_times['actual_arrival_time'] = stop_times['arrival_time'] + pd.to_timedelta(
        np.random.randint(-60, 300, size=len(stop_times)), unit='s'
    )

    # Calculate delay and categorize on-time or late
    stop_times['delay_seconds'] = (
        stop_times['actual_arrival_time'] - stop_times['arrival_time']
    ).dt.total_seconds()
    stop_times['on_time'] = stop_times['delay_seconds'].between(-60, 300)

    return stop_times

# Streamlit app starts here
st.title("TriMet On-Time Performance Dashboard")

# File uploader for the ZIP file
uploaded_zip = st.file_uploader("Upload your stop_times.zip", type="zip")

if uploaded_zip is not None:
    # Save uploaded ZIP to a temporary file
    with open("uploaded_stop_times.zip", "wb") as temp_zip:
        temp_zip.write(uploaded_zip.read())

    # Load the data using the load_gtfs_data function
    stop_times = load_gtfs_data("uploaded_stop_times.zip")

    if stop_times is not None:
        st.success("Data loaded successfully!")

        # Show the data
        st.subheader("Preview of stop_times Data")
        st.dataframe(stop_times.head())

        # Calculate OTP percentage
        otp_percentage = stop_times['on_time'].mean() * 100
        st.metric(label="Overall On-Time Percentage", value=f"{otp_percentage:.2f}%")
	

	 # Histogram of Arrival Times
        if 'arrival_time' in stop_times.columns:
            st.write("### Histogram of Arrival Times")
            stop_times['hour'] = stop_times['arrival_time'].dt.hour

            plt.hist(stop_times['hour'].dropna(), bins=np.arange(0, 25) - 0.5, edgecolor='black')
            plt.title('Distribution of Arrival Times by Hour')
            plt.xlabel('Hour of the Day')
            plt.ylabel('Frequency')
            st.pyplot(plt.gcf())


        # OTP Visualization
        st.subheader("On-Time Performance")
        fig, ax = plt.subplots(figsize=(6, 4))
        stop_times['on_time'].value_counts().plot(kind='bar', color=['green', 'red'], ax=ax)
        ax.set_title("On-Time vs. Late")
        ax.set_ylabel("Count")
        ax.set_xticklabels(["On-Time", "Late"], rotation=0)
        st.pyplot(fig)

        # Group by stop_id to calculate average delays
        patterns = stop_times.groupby('stop_id').agg(
            avg_delay=('delay_seconds', 'mean'),
            on_time_percentage=('on_time', 'mean')
        ).reset_index()

        # Slider for threshold
        threshold = st.slider("On-Time Threshold (%)", min_value=50, max_value=100, value=80)
        poor_performance = patterns[patterns['on_time_percentage'] < (threshold / 100)]

        # Display poor-performing stops
        st.subheader("Stops with Poor Performance")
        st.dataframe(poor_performance)
else:
    st.info("Upload a ZIP file to proceed.")

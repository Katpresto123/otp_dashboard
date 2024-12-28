
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import folium
import streamlit as st
import plotly.express as px



gtfs_path = "/Users/kathypresto/Desktop/gtfs"
files = ["agency.txt", "stops.txt", "routes.txt", "trips.txt", "stop_times.txt", "calendar.txt"]
gtfs_data = {file: pd.read_csv(os.path.join(gtfs_path, file)) for file in files}
for file, df in gtfs_data.items():
    print(f"--- {file} ---")
    print(df.head())
    print("\n")
stop_times = gtfs_data["stop_times.txt"]
print (stop_times.head())

stop_times['arrival_time'] = pd.to_datetime(stop_times['arrival_time'], format='%H:%M:%S', errors='coerce')
stop_times['departure_time'] = pd.to_datetime(stop_times['departure_time'], format='%H:%M:%S', errors='coerce')

routes = gtfs_data["routes.txt"]
trips = gtfs_data["trips.txt"]

print(routes.head())
print(trips.head())

# Load stops.txt
stops = gtfs_data["stops.txt"]

# Display the first few rows
print(stops.head())


print(stop_times.columns)
print(stops.columns)


# Convert stop_id in both DataFrames to string
stop_times['stop_id'] = stop_times['stop_id'].astype(str)
stops['stop_id'] = stops['stop_id'].astype(str)

# Merge stop_times with trips on trip_id
stop_times_trips = stop_times.merge(trips, on="trip_id", how="inner")

# Merge with stops on stop_id
otp_data = stop_times_trips.merge(stops, on="stop_id", how="inner")

# Display the merged DataFrame
print(otp_data.head())



# simulate actual arrial times with delay (in seconds)
otp_data['actual_arrival_time'] = otp_data['arrival_time'] + pd.to_timedelta(np.random.randint(-60, 300, size=len(otp_data)), unit='s')

# calculate delay
otp_data['delay_seconds'] = (otp_data['actual_arrival_time'] - otp_data['arrival_time']).dt.total_seconds()

# categorize as 'on-time' or 'late'
otp_data['on_time'] = otp_data['delay_seconds'].between(-60, 300)
print(otp_data.head())


# calculate OTP percentage
otp_percentage = otp_data['on_time'].mean() * 100

# plot
plt.figure(figsize=(6,4))
plt.bar(['On-Time', 'Late'], [otp_percentage, 100 - otp_percentage], color=['green', 'red'])
plt.title("On-Time Performance")
plt.ylabel("Percentage")
plt.show()

# Group by route and stop to calculate average delays
patterns = otp_data.groupby(['route_id', 'stop_id']).agg(
    avg_delay=('delay_seconds', 'mean'),
    on_time_percentage=('on_time', 'mean')
).reset_index()

# Identify poorly performing routes or stops
poor_performance = patterns[patterns['on_time_percentage'] < 0.8]
print(poor_performance)



# Load data
otp_data = pd.read_csv('otp_data.csv')  # Replace with your actual file

# Streamlit layout
st.title("TriMet On-Time Performance Dashboard")
st.write("Explore on-time performance data.")

# OTP Visualization
fig, ax = plt.subplots(figsize=(6, 4))
otp_data['on_time'].value_counts().plot(kind='bar', color=['green', 'red'], ax=ax)
ax.set_title("On-Time vs. Late")
st.pyplot(fig)

# Filter and display poor performance
threshold = st.slider("On-Time Threshold (%)", min_value=50, max_value=100, value=80)
poor_performance = otp_data[otp_data['on_time_percentage'] < (threshold / 100)]
st.write("Stops with Poor Performance")
st.dataframe(poor_performance)





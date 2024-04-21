import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set the title for the dashboard
st.title("COM Events Dashboard")

# File uploader for input data
uploaded_file = st.file_uploader("Choose an Excel (.xlsx) file", type="xlsx")


# Preprocess data, setting 'Date' as a datetime index
def preprocess_data(df: pd.DataFrame):
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    return df


# Plot the attendance for speaker events filtered by date and event type.
def create_event_attendance_chart(df: pd.DataFrame, start_date: pd.Timestamp, end_date: pd.Timestamp):
    st.subheader("Event Attendance Chart")

    # Filter data for events between the selected date range and specific months
    filtered_data = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    filtered_data = filtered_data[filtered_data['Date'].dt.month.isin([11, 12])]

    # Further filter for events of type "Speaker"
    speaker_events = filtered_data[filtered_data['Event Category'].str.contains('Speaking Events')]

    # Aggregate attendance
    speaker_attendance = speaker_events.groupby(['Date', 'Primary Midnight Mission Employee Involved',
                                                 'Location', 'Event Category'])['Total Attendees'].sum().reset_index()

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 8))
    for speaker in speaker_attendance['Primary Midnight Mission Employee Involved'].unique():
        speaker_data = speaker_attendance[speaker_attendance['Primary Midnight Mission Employee Involved'] == speaker]

        for category in speaker_data['Event Category'].unique():
            category_data = speaker_data[speaker_data['Event Category'] == category]
            bars = ax.bar(category_data['Date'], category_data['Total Attendees'], label=f"{speaker} - {category}",
                          alpha=0.7, width=0.8)

            # Annotate location and count above each bar
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{int(height)}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=8, clip_on=True)

    ax.set_xlabel('Date')
    ax.set_ylabel('Attendance')
    ax.set_title('Speaker Event Attendance by Primary Speaker and Event Category')
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.xticks(rotation=45)

    st.pyplot(fig)


# Plot a bar chart showing the historical summary of event counts by monthly periods.
def create_historical_summary_chart(df: pd.DataFrame):
    st.subheader("Historical Summary Chart")

    # Group and count events by month
    monthly_counts = df.groupby(pd.Grouper(key='Date', freq='M')).size()

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.bar(monthly_counts.index, monthly_counts, width=20)
    plt.xlabel('Month')
    plt.ylabel('Event Count')
    plt.title('Monthly Event Counts')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)


# Main logic to handle file upload and display charts
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    df = preprocess_data(df)

    # Display the historical summary chart
    create_historical_summary_chart(df)

    # Date selection for event attendance chart
    start_date = st.date_input("Start Date", value=pd.Timestamp.today() - pd.DateOffset(months=2))
    end_date = st.date_input("End Date", value=pd.Timestamp.today())

    # Ensure the start date is not after the end date
    if start_date > end_date:
        st.error("Start date must be before end date.")
    else:
        create_event_attendance_chart(df, pd.Timestamp(start_date), pd.Timestamp(end_date))

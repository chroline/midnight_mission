import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.write("# COM Events Dashboard")

uploaded_file = st.file_uploader("Choose an Excel (.xlsx) file", type="xlsx")


def create_event_attendance_chart(df: pd.DataFrame, start_date, end_date):
    st.write("## Event Attendance Chart")

    data = df.copy()

    # Convert 'Date' column to datetime
    data['Date'] = pd.to_datetime(data['Date'])

    # Filter the data based on user input
    data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]

    # Filter for events in November and December
    nov_dec_events = data[(data['Date'].dt.month == 11) | (data['Date'].dt.month == 12)]

    # Filter for events of type "Speaker" (AA and TMM)
    speaker_events = nov_dec_events[(nov_dec_events['Event Category'] == 'Speaking Events (AA)') |
                                    (nov_dec_events['Event Category'] == 'Speaking Events (TMM)')]

    # Aggregate attendance by speaker, date, location, and event category
    speaker_attendance = \
    speaker_events.groupby(['Date', 'Primary Midnight Mission Employee Involved', 'Location', 'Event Category'])[
        'Total Attendees'].sum().reset_index()

    # Plot
    fig, ax = plt.subplots(figsize=(12, 8))
    for speaker in speaker_attendance['Primary Midnight Mission Employee Involved'].unique():
        speaker_data = speaker_attendance[speaker_attendance['Primary Midnight Mission Employee Involved'] == speaker]

        for category in speaker_data['Event Category'].unique():
            category_data = speaker_data[speaker_data['Event Category'] == category]
            bars = ax.bar(category_data['Date'], category_data['Total Attendees'], label=f"{speaker} - {category}",
                          alpha=0.7, width=0.8)

            # Add location labels
            for bar, location in zip(bars, category_data['Location']):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, height + 10, location, ha='center', va='bottom', fontsize=8,
                        rotation=0)

            # Add count labels
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, height + 5, str(int(height)), ha='center', va='bottom',
                        fontsize=8)

    plt.xlabel('Date')
    plt.ylabel('Attendance')
    plt.title('Speaker Event Attendance by Primary Speaker and Event Category')
    plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1))
    plt.xticks(rotation=45)
    plt.subplots_adjust(right=0.7)
    plt.tight_layout()

    st.pyplot(plt)


def create_historical_summary_chart(df: pd.DataFrame):
    st.write("## Historical Summary Chart")

    data = df.copy()

    # Group the data by monthly periods and count the events
    data['Date'] = pd.to_datetime(data['Date'])
    monthly_counts = data.groupby(pd.Grouper(key='Date', freq='M')).size()

    # Create the bar chart
    plt.figure(figsize=(12, 6))
    bar_width = 20
    plt.bar(monthly_counts.index, monthly_counts.values, width=bar_width)
    plt.xlabel('Monthly Periods')
    plt.ylabel('Event Count')
    plt.title('Historical Summary of Event Counts by Monthly Periods')
    plt.xticks(rotation=45)
    # plt.grid(True)
    plt.tight_layout()

    st.pyplot(plt)


if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    create_historical_summary_chart(df)

    # Let the user choose the date range
    start_date = pd.to_datetime(st.date_input("Start Date", value=pd.Timestamp.today() - pd.DateOffset(months=2)))
    end_date = pd.to_datetime(st.date_input("End Date", value=pd.Timestamp.today()))

    # Check if the start date is not after the end date
    if start_date > end_date:
        st.error("Start date must be before end date.")
    else:
        create_event_attendance_chart(df, start_date, end_date)


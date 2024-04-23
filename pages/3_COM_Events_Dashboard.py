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


# Plot a bar chart showing the historical summary of event counts by monthly periods.
def plot_historical_summary_chart(df: pd.DataFrame):
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


# Plot the attendance for speaker events filtered by date and event type.
def plot_event_attendance_chart(df: pd.DataFrame):
    st.subheader("Event Attendance Chart")

    # Further filter for events of type "Speaker"
    speaker_events = df[df['Event Category'].str.contains('Speaking Events')]

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


# Plot count of events, excluding specific speaker events
def plot_event_category_chart(df: pd.DataFrame):
    st.subheader("Event Counts by Category")

    # Define the categories of interest
    categories = ['Laughter with a Mission', 'Art with a Mission', 'Music with a Mission', 'Community Event',
                  'Special Event']

    # Filter for events in the specified categories
    filtered_events = df[df['Event Category'].isin(categories)]

    # Count the number of events for each category
    category_counts = filtered_events['Event Category'].value_counts()

    if category_counts.empty:
        return st.write("No non-speaker events found.")

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    category_counts.plot(kind='bar', color='skyblue')

    # Add labels for counts above the bars
    for i, v in enumerate(category_counts):
        plt.text(i, v + 0.5, str(v), ha='center', va='bottom')

    plt.xlabel('Event Category')
    plt.ylabel('Count')
    plt.title('Event Counts by Category')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)


# Main logic to handle file upload and display charts
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    df = preprocess_data(df)

    plot_historical_summary_chart(df)

    # Date selection for event attendance chart
    start_date = st.date_input("Start Date", value=pd.Timestamp.today() - pd.DateOffset(months=2))
    end_date = st.date_input("End Date", value=pd.Timestamp.today())

    if start_date > end_date:
        st.error("Start date must be before end date.")
    else:
        filtered_data = df[(df['Date'] >= pd.Timestamp(start_date)) & (df['Date'] <= pd.Timestamp(end_date))].fillna(0)
        st.write(f"Data from {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}")

        if not filtered_data.empty:
            plot_event_attendance_chart(filtered_data)
            plot_event_category_chart(filtered_data)
        else:
            st.write("No data available for the selected date range.")

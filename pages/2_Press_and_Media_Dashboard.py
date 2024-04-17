import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

st.write("# Press & Media Dashboard")

uploaded_file = st.file_uploader("Choose an Excel (.xlsx) file", type="xlsx")


def create_distribution_chart(df: pd.DataFrame, start_date, end_date):
    data = df.copy()

    # Convert 'Date to post/air' column to datetime
    data['Date to post/air'] = pd.to_datetime(data['Date to post/air'])

    # Filter the data based on user input
    filtered_data = data[(data['Date to post/air'] >= start_date) & (data['Date to post/air'] <= end_date)]

    date_range_str = f"Date Range: {start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}"
    st.write(date_range_str)

    if filtered_data.empty:
        st.write("No data available")
        return

    # Explode the 'Form of Media' column
    media_types = filtered_data['Form of Media'].str.split(', ').explode()

    # Calculate media type distribution
    media_type_distribution = media_types.value_counts()

    # Plotting
    plt.figure(figsize=(10, 6))
    media_type_distribution.plot(kind='bar', color='skyblue')
    plt.title('Distribution of Media Coverage by Type')
    plt.xlabel('Media Type')
    plt.ylabel('Occurrences')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--')

    # Print the selected date range
    st.write("## Distribution")
    st.write(date_range_str)
    st.pyplot(plt)


def create_events_table(df: pd.DataFrame, start_date, end_date):
    st.write("## Events and Press Outlets Table")

    data = df.copy()

    # Filter the data based on user input
    filtered_data = data[(data['Date to post/air'] >= start_date) & (data['Date to post/air'] <= end_date)]

    # Selecting the appropriate date column
    filtered_data['Event Date'] = filtered_data['Date of Interview'].fillna(filtered_data['Date to post/air'])

    # Combining "Current Event(s)" and "Name of Press Outlet" for the description
    filtered_data['Description'] = filtered_data['Current Event(s)'] + " (" + filtered_data['Name of Press Outlet'] + ")"
    filtered_data = filtered_data.dropna(subset=['Description'])

    # Selecting relevant columns for the table
    table_data = filtered_data[['Event Date', 'Description']]
    table_data.dropna(subset=['Event Date'], inplace=True)  # Dropping rows where the event date is missing
    table_data.sort_values('Event Date', inplace=True)  # Sorting by date

    table_data['Event Date'] = pd.to_datetime(table_data['Event Date']).dt.strftime('%B %d, %Y')

    fig, ax = plt.subplots(figsize=(10, 9))  # Slightly larger figure to accommodate the table text
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=table_data.values, colLabels=table_data.columns, loc='center', cellLoc='center', colWidths=[0.2, 0.8])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)  # Scale the table size to make it more readable

    st.pyplot(plt)


if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # Let the user choose the date range
    start_date = pd.to_datetime(st.date_input("Start Date", value=pd.Timestamp.today() - pd.DateOffset(months=2)))
    end_date = pd.to_datetime(st.date_input("End Date", value=pd.Timestamp.today()))

    # Check if the start date is not after the end date
    if start_date > end_date:
        st.error("Start date must be before end date.")
    else:
        create_distribution_chart(df, start_date, end_date)
        create_events_table(df, start_date, end_date)


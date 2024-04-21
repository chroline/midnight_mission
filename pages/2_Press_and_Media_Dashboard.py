import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.write("# Press & Media Dashboard")

uploaded_file = st.file_uploader("Choose an Excel (.xlsx) file", type="xlsx")


def create_distribution_chart(df: pd.DataFrame):
    data = df.copy()

    if data.empty:
        st.write("No data available")
        return

    # Explode the 'Form of Media' column
    media_types = data['Form of Media'].str.split(', ').explode()

    # Calculate media type distribution
    media_type_distribution = media_types.value_counts()

    # Plotting
    plt.figure(figsize=(10, 6))
    ax = media_type_distribution.plot(kind='bar', color='skyblue')
    plt.title('Distribution of Media Coverage by Type')
    plt.xlabel('Media Type')
    plt.ylabel('Occurrences')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--')

    # Adding annotations
    for i, count in enumerate(media_type_distribution):
        ax.text(i, count + 1, str(count), ha='center')

    st.write("## Distribution")
    st.pyplot(plt)


def create_events_table(df: pd.DataFrame):
    st.write("## Events and Press Outlets Table")

    data = df.copy()

    # Selecting the appropriate date column
    data['Event Date'] = data['Date of Interview'].fillna(data['Date to post/air'])

    # Combining "Current Event(s)" and "Name of Press Outlet" for the description
    data['Description'] = data['Current Event(s)'] + " (" + data['Name of Press Outlet'] + ")"
    data = data.dropna(subset=['Description'])

    # Selecting relevant columns for the table
    table_data = data[['Event Date', 'Description']]
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

    df['Date to post/air'] = pd.to_datetime(df['Date to post/air'])
    df.set_index('Date to post/air', inplace=True, drop=False)

    min_date, max_date = df.index.min(), df.index.max()

    # Let the user choose the date range
    start_date = st.date_input("Start date", min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input("End date", min_value=min_date, max_value=max_date, value=max_date)

    # Convert user-selected dates to pandas timestamps
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Check if the start date is not after the end date
    if start_date >= end_date:
        st.error("Start date must be before end date.")
    else:
        # Filter the data based on user input
        filtered_data = df[(df['Date to post/air'] >= start_date) & (df['Date to post/air'] <= end_date)]

        date_range_str = f"Date Range: {start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}"
        st.write(date_range_str)

        create_distribution_chart(filtered_data)
        create_events_table(filtered_data)


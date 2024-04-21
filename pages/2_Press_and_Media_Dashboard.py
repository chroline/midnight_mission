import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Press & Media Dashboard")

# File uploader for input data
uploaded_file = st.file_uploader("Choose an Excel (.xlsx) file", type="xlsx")


# Preprocess data, setting 'Date to post/air' as a datetime index
def preprocess_data(df: pd.DataFrame):
    df['Date to post/air'] = pd.to_datetime(df['Date to post/air'])
    df.set_index('Date to post/air', inplace=True, drop=False)
    return df


# Plot the distribution of different media types via a bar chart.
def plot_media_distribution(df: pd.DataFrame):
    st.subheader("Distribution of Media Coverage by Type")

    media_types = df['Form of Media'].str.split(', ').explode()
    media_type_distribution = media_types.value_counts()

    plt.figure(figsize=(10, 6))
    ax = media_type_distribution.plot(kind='bar', color='skyblue')
    plt.title('Distribution by Media Type')
    plt.xlabel('Media Type')
    plt.ylabel('Occurrences')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    for i, count in enumerate(media_type_distribution):
        ax.text(i, count, str(count), ha='center')

    st.pyplot(plt)


# Plot a table displaying events and corresponding press outlets.
def display_events_table(df: pd.DataFrame):
    st.subheader("Events and Press Outlets")

    df['Event Date'] = df['Date of Interview'].fillna(df['Date to post/air'])
    df['Description'] = df['Current Event(s)'] + " (" + df['Name of Press Outlet'] + ")"
    df = df.dropna(subset=['Event Date', 'Description'])

    df['Event Date'] = df['Event Date'].dt.strftime('%B %d, %Y')
    df.sort_values('Event Date', inplace=True)

    table_data = df[['Event Date', 'Description']]
    table_data.dropna(subset=['Event Date'], inplace=True)  # Dropping rows where the event date is missing
    table_data.sort_values('Event Date', inplace=True)  # Sorting by date

    table_data['Event Date'] = pd.to_datetime(table_data['Event Date']).dt.strftime('%B %d, %Y')

    fig, ax = plt.subplots(figsize=(10, 9))  # Slightly larger figure to accommodate the table text
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=table_data.values, colLabels=table_data.columns, loc='center', cellLoc='center',
                     colWidths=[0.2, 0.8])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)  # Scale the table size to make it more readable

    st.pyplot(plt)


# Main logic to handle file upload and display charts
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    df = preprocess_data(df)

    # Date selection for filtering
    min_date, max_date = df.index.min(), df.index.max()
    st.write("Select the date range for analysis:")
    start_date = st.date_input("Start date", min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input("End date", min_value=min_date, max_value=max_date, value=max_date)

    if start_date >= end_date:
        st.error("Start date must be before the end date.")
    else:
        # Filter the data based on selected dates
        filtered_data = df[start_date:end_date]
        st.write(f"Data from {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}")

        if not filtered_data.empty:
            plot_media_distribution(filtered_data)
            display_events_table(filtered_data)
        else:
            st.write("No data available for the selected date range.")

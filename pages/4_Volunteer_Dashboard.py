import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set the title for the dashboard
st.title("Volunteer Dashboard")

# File uploader for input data
uploaded_file = st.file_uploader("Choose an Excel (.xlsx) file", type="xlsx")


# Preprocess data, setting 'Date' as a datetime index
def preprocess_data(df: pd.DataFrame):
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    return df


# Plot volunteer breakdown by category for a selected date range
def plot_volunteer_breakdown_chart(df: pd.DataFrame):
    st.subheader("Volunteer Breakdown by Category")

    # Assuming `Category` and `Count` are columns in your data after preprocessing
    category_counts = df.groupby('Category')['Count'].sum()
    labels = category_counts.index.tolist()
    sizes = category_counts.tolist()

    # Calculate percentages for filtering labels
    total_size = sum(sizes)
    percentages = [size / total_size * 100 for size in sizes]
    explode = tuple(0.05 for _ in sizes)
    filtered_labels = [label if pct > 2 else '' for label, pct in zip(labels, percentages)]

    # Create Pie Chart
    plt.figure(figsize=(10, 8))
    plt.pie(sizes, labels=filtered_labels, autopct=lambda pct: f'{pct:.1f}%' if pct > 2 else '', pctdistance=0.85,
            explode=explode)
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.title('Volunteer Breakdown by Category')
    plt.legend(labels, title="Categories", loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()

    st.pyplot(plt)


# Main logic to handle file upload and display charts
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    df = preprocess_data(df)

    # Display charts...
    start_date = st.date_input("Start Date", value=pd.Timestamp.today() - pd.DateOffset(months=2))
    end_date = st.date_input("End Date", value=pd.Timestamp.today())

    if start_date > end_date:
        st.error("Start date must be before end date.")
    else:
        filtered_data = df[(df['Date'] >= pd.Timestamp(start_date)) & (df['Date'] <= pd.Timestamp(end_date))].fillna(0)
        st.write(f"Data from {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}")

        if not filtered_data.empty:
            plot_volunteer_breakdown_chart(filtered_data)
        else:
            st.write("No data available for the selected date range.")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the dashboard
st.title('Volunteer Statistics Dashboard')

# File uploader for input data
uploaded_file = st.file_uploader("Choose a CSV file", type="xlsx")

if uploaded_file is not None:
    # Read the uploaded file
    df = pd.read_excel(uploaded_file)

    # Drop unnamed columns and rows with NaN values in the 'November' column as a placeholder for general cleaning
    unnamed_columns = [col for col in df.columns if 'Unnamed' in col]
    df.drop(columns=unnamed_columns, inplace=True)
    df.dropna(subset=['November'], inplace=True)  # Assuming initial cleanup based on an example column

    # Extract categories
    categories = df['Category']

    # Setting labels for items in Chart
    labels = categories.tolist()

    # Dropdown to select the month
    month_list = [col for col in df.columns if col not in ['Category'] + unnamed_columns]
    selected_month = st.selectbox('Select Month for Analysis', options=month_list)

    # Data for the selected month
    month_data = df[selected_month].tolist()

    # Calculate totals and percentages
    total_size = sum(month_data)
    percentages = [size / total_size * 100 for size in month_data]

    # Define the explosion for slices
    explode = tuple(0.05 if pct > 2 else 0 for pct in percentages)  # Explode only significant slices

    # Filter labels for significant percentages
    filtered_labels = [label if pct > 2 else '' for label, pct in zip(categories, percentages)]

    # Pie Chart
    plt.pie(month_data, labels=filtered_labels,
            autopct=lambda pct: f'{pct:.1f}%' if pct > 2 else '',
            pctdistance=0.85, explode=explode)

    # Draw center circle for a donut shape
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # Chart title
    plt.title(f'{selected_month} Volunteering by Category')

    # Adding legend outside the plot
    plt.legend(labels, title="Categories", loc='center left', bbox_to_anchor=(1.5, 0.5))

    # Show plot
    st.pyplot(fig)
else:
    st.write("Please upload a CSV file.")

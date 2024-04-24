import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the dashboard
st.title('Volunteer Statistics Dashboard')

# File uploader for input data
uploaded_file = st.file_uploader("Choose a CSV file", type="xlsx")


def plot_graph(df: pd.DataFrame, title, selected_month):
    plt.figure()

    # Drop unnamed columns and rows with NaN values in the 'November' column as a placeholder for general cleaning
    unnamed_columns = [col for col in df.columns if 'Unnamed' in col]
    df.drop(columns=unnamed_columns, inplace=True)
    df.dropna(subset=[selected_month], inplace=True)  # Cleanup based on the selected month

    # Extract categories
    categories = df['Category'].tolist()

    # Data for the selected month
    month_data = df[selected_month].tolist()

    # Calculate total size
    total_size = sum(month_data)

    # Calculate percentages
    percentages = [size / total_size * 100 for size in month_data]

    # Explosion
    explode = tuple(0.05 if pct > 2 else 0 for pct in percentages)  # Explode only significant slices

    # Filter labels for significant percentages
    filtered_labels = [label if pct > 2 else '' for label, pct in zip(categories, percentages)]

    # Pie Chart
    plt.pie(month_data, labels=filtered_labels,
            autopct=lambda pct: f'{pct:.1f}%' if pct > 2 else '',
            pctdistance=0.85, explode=explode)

    # Draw circle
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()

    # Adding Circle in Pie chart
    fig.gca().add_artist(centre_circle)

    # Chart title
    plt.title(f'{selected_month} {title}')

    # Adding legend outside the plot
    plt.legend(categories, title="Categories", loc='center left', bbox_to_anchor=(1.5, 0.5))

    # Show plot
    st.pyplot(fig)


if uploaded_file is not None:
    # Read the uploaded file
    volunteer_numbers_df = pd.read_excel(uploaded_file, 'Counts')
    volunteer_hours_df = pd.read_excel(uploaded_file, 'Hours')

    # Dropdown to select the month (outside the plotting function)
    month_list = [col for col in volunteer_numbers_df.columns if col not in ['Category']]
    selected_month = st.selectbox('Select Month for Analysis', options=month_list)

    # Plotting
    plot_graph(volunteer_numbers_df, 'Volunteering by Category', selected_month)
    plot_graph(volunteer_hours_df, 'Volunteering Hours by Category', selected_month)

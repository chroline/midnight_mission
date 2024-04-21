import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.write("# Social Media Dashboard")

# File uploader for input data
uploaded_file = st.file_uploader("Choose an Excel (.xlsx) file", type="xlsx")


# Preprocess data, setting 'Date' as a datetime index
def preprocess_data(df: pd.DataFrame):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df


# Plot total followers per platform
def plot_total_followers(df: pd.DataFrame):
    st.write("## Total Followers")

    # Sidebar component to select a month
    selected_month = st.date_input("Select a month to view followers",
                                   value=df.index.max(),
                                   min_value=df.index.min(),
                                   max_value=df.index.max())

    # Filter data to the selected month
    month_data = df[df.index.month == selected_month.month]
    monthly_totals = month_data.sum()

    # Plotting
    plt.figure(figsize=(10, 6))
    ax = monthly_totals.plot(kind='bar', color='skyblue')
    plt.title('Total Followers per Platform')
    plt.xlabel('Platforms')
    plt.ylabel('Total Followers')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    # Adding annotations for data points
    for i, count in enumerate(monthly_totals):
        ax.text(i, count, str(count), ha='center')

    st.pyplot(plt)


# Plot growth over time for each platform
def plot_growth_over_time(df: pd.DataFrame):
    st.write("## Growth Over Time")

    # Calculate the growth from the initial value for all columns
    growth_from_initial = ((df - df.iloc[0]) / df.iloc[0]) * 100

    # For TikTok, filter the data from November 2022 onwards before calculating the growth
    if 'TikTok' in df.columns:  # Check if TikTok column exists
        df_tiktok_filtered = df[df.index >= '2023-01']['TikTok']
        growth_from_initial['TikTok'] = ((df_tiktok_filtered - df_tiktok_filtered.iloc[0]) / df_tiktok_filtered.iloc[
            0]) * 100

    # Plotting
    plt.figure(figsize=(14, 8))
    for column in growth_from_initial.columns:
        plt.plot(growth_from_initial.index, growth_from_initial[column], label=column, marker='o')

    plt.title('Social Media Platform Growth')
    plt.xlabel('Date')
    plt.ylabel('% Growth')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(plt)


# Function to plot median monthly percentage change for each platform
def plot_median_growth(df: pd.DataFrame):
    st.write("## Median Growth")

    # Calculate month-to-month percentage change for the entire dataset
    monthly_percent_changes = df.pct_change() * 100
    median_monthly_percent_changes = monthly_percent_changes.median()

    # Creating a bar graph of the median percentage changes
    fig, ax = plt.subplots()
    median_monthly_percent_changes.plot(kind='bar', color='teal', ax=ax)
    ax.set_title('Median Monthly Percentage Change in Social Media Platform Usage')
    ax.set_ylabel('Median % Change')
    ax.set_xlabel('Platforms')
    ax.axhline(0, color='black', linewidth=0.8)

    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    st.pyplot(plt)


# Main logic to handle file upload and display charts
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    df_preprocessed = preprocess_data(df)

    plot_total_followers(df_preprocessed)
    plot_growth_over_time(df_preprocessed)
    plot_median_growth(df_preprocessed)

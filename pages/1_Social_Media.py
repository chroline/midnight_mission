import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame
from statsmodels.tsa.statespace.sarimax import SARIMAX

st.write("# Social Media Dashboard")

uploaded_file = st.file_uploader("Choose an Excel (.xlsx) file", type="xlsx")


def create_followers_chart(df: DataFrame):
    st.write("## Total Followers")

    data = df.copy()

    # Ensure the 'Date' column is in datetime format
    data['Date'] = pd.to_datetime(data['Date'])

    # Streamlit sidebar component to select a month
    selected_month = st.date_input("Select a month", min_value=data['Date'].min(), max_value=data['Date'].max(), value=data['Date'].max())

    # Filter data to the selected month
    # Extracting year and month from the date for comparison
    data['YearMonth'] = data['Date'].dt.strftime('%Y-%m')
    selected_month_str = selected_month.strftime('%Y-%m')
    month_data = data[data['YearMonth'] == selected_month_str]

    # Aggregate the data for the selected month
    numeric_columns = data.select_dtypes(include='number').columns.drop('Date', errors='ignore')
    monthly_totals = month_data[numeric_columns].sum()

    # Plotting
    plt.figure(figsize=(10, 6))
    ax = monthly_totals.plot(kind='bar', color='skyblue')
    plt.title('Total Followers per Platform')
    plt.xlabel('Platforms')
    plt.ylabel('Total Followers')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    # Adding annotations
    for i, count in enumerate(monthly_totals):
        ax.text(i, count, str(count), ha='center')


    st.pyplot(plt)


def create_growth_chart(df: DataFrame):
    data = df.copy()

    data.set_index('Date', inplace=True)

    # Calculate the growth from the initial value for all columns
    df_growth_from_initial = ((data - df.iloc[0]) / data.iloc[0]) * 100

    # For TikTok, filter the data from November 2022 onwards before calculating the growth
    if 'TikTok' in df.columns:  # Check if TikTok column exists
        df_tiktok_filtered = data[data.index >= '2023-01']['TikTok']
        df_growth_from_initial['TikTok'] = ((df_tiktok_filtered - df_tiktok_filtered.iloc[0]) / df_tiktok_filtered.iloc[
            0]) * 100

    # Plotting
    plt.figure(figsize=(14, 8))
    for column in df_growth_from_initial.columns:
        if column == 'Vero':
            continue
        if column == 'TikTok':
            # Plot only the filtered TikTok data
            plt.plot(df_growth_from_initial.loc[df_growth_from_initial.index >= '2022-11', column].index,
                     df_growth_from_initial.loc[df_growth_from_initial.index >= '2022-11', column], label=column,
                     marker='o')
        else:
            # Plot the entire data for other columns
            plt.plot(df_growth_from_initial.index, df_growth_from_initial[column], label=column, marker='o')

    plt.title('Social Media Platform Growth')
    plt.xlabel('Date')
    plt.ylabel('% Growth')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.write("## Growth Over Time")
    st.pyplot(plt)


def create_median_growth_chart(df: DataFrame):
    data = df.copy()

    # Ensure the date column is set as the index correctly and that it's excluded from calculations
    data_indexed = data.set_index(data.columns[0])

    # Calculate month-to-month percentage change for the entire dataset, excluding the date index
    monthly_percent_changes = data_indexed.pct_change() * 100

    # Calculate the median percentage change for each social media platform
    median_monthly_percent_changes = monthly_percent_changes.median()

    # Creating a bar graph of the median percentage changes
    fig, ax = plt.subplots()
    median_monthly_percent_changes.plot(kind='bar', color='teal', ax=ax)
    ax.set_title('Median Monthly Percentage Change in Social Media Platform Usage')
    ax.set_ylabel('Median % Change')
    ax.set_xlabel('Platforms')
    ax.axhline(0, color='black', linewidth=0.8)  # Adding a line at 0 for reference

    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    st.write("## Median Growth")
    st.pyplot(plt)


def create_mtm_growth_chart(df: pd.DataFrame):
    st.write("## Month-to-Month Growth")

    # Copy DataFrame and preprocess data
    data = df.copy()
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    data.columns = data.columns.str.strip()

    # Streamlit components for date range selection
    st.write("### Select Date Range for Analysis")
    st.write("**Example:** To compare growth from September–October 2023, choose 2023-09-01 and 2023-11-01")
    min_date, max_date = data.index.min(), data.index.max()

    start_date = st.date_input("Start date", min_value=min_date, max_value=max_date, value=min_date)
    st.write("Please choose the first of the beginning month to compare.")
    end_date = st.date_input("End date", min_value=min_date, max_value=max_date, value=max_date)
    st.write("Please choose the first of the month after the ending month to compare.")

    if start_date > end_date:
        st.sidebar.error("End date must be after start date.")
        return

    # Filtering data based on selected date range
    selected_data = data.loc[start_date:end_date]
    percent_change = (selected_data.diff().iloc[-1] / selected_data.iloc[0]) * 100

    # Plotting
    fig, ax = plt.subplots()
    percent_change.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title('Percentage Change in Social Media Platform Usage')
    ax.set_ylabel('% Change')
    ax.set_xlabel('Platforms')
    ax.axhline(0, color='black', linewidth=0.8)

    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    st.pyplot(fig)


if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    create_followers_chart(df)
    create_growth_chart(df)
    create_median_growth_chart(df)
    create_mtm_growth_chart(df)

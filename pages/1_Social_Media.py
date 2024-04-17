import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame
from statsmodels.tsa.statespace.sarimax import SARIMAX

st.write("# Social Media Dashboard")

uploaded_file = st.file_uploader("Choose an Excel (.xlsx) file", type="xlsx")


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


def create_growth_projection(df: pd.DataFrame):
    st.write("## Instagram Growth Forecast")

    data = df.copy()
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    instagram_data = data['Instagram']

    sarima_order = (1, 1, 1)
    seasonal_order = (1, 1, 1, 12)  # yearly seasonality

    sarima_model = SARIMAX(instagram_data, order=sarima_order, seasonal_order=seasonal_order,
                           enforce_stationarity=False, enforce_invertibility=False)
    sarima_result = sarima_model.fit()

    forecast = sarima_result.get_forecast(steps=12)
    forecast_values = forecast.predicted_mean
    confidence_intervals = forecast.conf_int()

    forecast_index_corrected = pd.date_range(instagram_data.index[-1] + pd.offsets.MonthEnd(1), periods=12, freq='M')

    plt.figure(figsize=(14, 7))
    plt.plot(instagram_data.index, instagram_data, label='Actual', marker='o')
    plt.plot(forecast_index_corrected, forecast_values, color='red', label='Forecast', marker='x')
    plt.fill_between(forecast_index_corrected, confidence_intervals.iloc[:, 0], confidence_intervals.iloc[:, 1],
                     color='pink', alpha=0.3)
    plt.title('Instagram Growth Forecast')
    plt.xlabel('Date')
    plt.ylabel('Instagram Metrics')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(plt)


if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    create_growth_chart(df)
    create_median_growth_chart(df)

    create_mtm_growth_chart(df)
    create_growth_projection(df)

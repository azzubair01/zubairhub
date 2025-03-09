import os
import logging
import requests
import datetime
import pandas as pd
import streamlit as st
import plotly.express as px


def fuel_price():

    # Streamlit App Title
    st.title("⛽ Fuel Price (Malaysia)")

    # API Call Function
    @st.cache_data
    def fetch_fuel_data():
        BASE_URL = 'https://api.data.gov.my/'
        ENDPOINT = 'data-catalogue?meta=True&filter=level@series_type&id=fuelprice'
        FULL_URL = os.path.join(BASE_URL, ENDPOINT)

        try:
            response = requests.get(FULL_URL)
            response.raise_for_status()
            return response.json().get('data', [])
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {e}")
            return []

    # Fetch Data
    with st.spinner("Fetching fuel price data..."):
        fuel_data = fetch_fuel_data()

    if fuel_data:
        # Convert data to DataFrame
        df = pd.DataFrame(fuel_data)
        df['date'] = pd.to_datetime(df['date'])

        # Get default date range (last 7 days)
        max_date = df['date'].max()
        min_date = df['date'].min()
        default_start_date = max(min_date, max_date - pd.Timedelta(days=365))  # Ensure at least 7 days if available

        col1, col2 = st.columns(2)
        with col1:
            start_date, end_date = st.date_input(
                "Select Date Range",
                [default_start_date, max_date],
                min_value=min_date,
                max_value=max_date
            )

        with col2:
            fuel_types = ['ron95', 'ron97', 'diesel']
            selected_fuels = st.multiselect("Select Fuel Type", fuel_types, default=fuel_types)

        # Apply Filters
        filtered_df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]
        df_melted = filtered_df.melt(id_vars=['date'], value_vars=selected_fuels, var_name='Fuel Type', value_name='Price')

        # Plotly Line Chart
        if not df_melted.empty:
            fig = px.line(df_melted, x='date', y='Price', color='Fuel Type',
                          title='Weekly Fuel Price Trends',
                          labels={'date': 'Date', 'Price': 'Price/Litre (MYR)', 'Fuel Type': 'Fuel Type'},
                          markers=True)
            st.plotly_chart(fig)
        else:
            st.warning("No data available for the selected filters.")

        # Display Data Table
        st.subheader("📊 Fuel Price Data")
        st.dataframe(
            data=filtered_df.drop(['diesel_eastmsia', 'series_type'], axis=1).sort_values(by='date', ascending=False),
            use_container_width=True,
            column_config={
                'date': st.column_config.DateColumn()
            },
            hide_index=True
        )
    else:
        st.error("No fuel price data available.")

    # Footer
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="text-align: left;">
            🔄 <strong>Data last updated:</strong> {df['date'].max().strftime('%Y-%m-%d')}
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="text-align: right;">
            📡 <strong>Source:</strong> <a href="https://api.data.gov.my/data-catalogue?meta=True&filter=level@series_type&id=fuelprice" target="_blank">DOSM Open API</a>
        </div>
        """, unsafe_allow_html=True)
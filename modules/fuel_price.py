import os
import json
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
        BASE_URL = 'https://api.data.gov.my'
        ENDPOINT = 'data-catalogue?meta=True&filter=level@series_type&id=fuelprice'
        FULL_URL = f"{BASE_URL}/{ENDPOINT}"

        try:
            response = requests.get(FULL_URL)
            response.raise_for_status()
            return response.json().get('data', [])
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {e}")
            return []

    @st.cache_data
    def load_fuel_events():
        events_file = 'modules/fuel_price_data/events.json'
        if os.path.exists(events_file):
            try:
                with open(events_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"Failed to load fuel events: {e}")
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
            date_range = st.date_input(
                "Select Date Range",
                [default_start_date, max_date],
                min_value=min_date,
                max_value=max_date
            )
            if not isinstance(date_range, (list, tuple)) or len(date_range) < 2:
                st.info("Please select both start and end dates.")
                return
            start_date, end_date = date_range[0], date_range[1]

        with col2:
            fuel_types = ['ron95', 'ron97', 'diesel']
            selected_fuels = st.multiselect("Select Fuel Type", fuel_types, default=fuel_types)

        # Event Overlay Controls
        events = load_fuel_events()
        col_ev1, col_ev2 = st.columns([1, 2])
        with col_ev1:
            show_events = st.checkbox("📌 Show Key Historical Events", value=True)
        with col_ev2:
            if show_events:
                category_options = ["All Categories", "🇲🇾 Domestic Policy", "🌍 Global Oil Shock"]
                selected_category = st.radio("Filter Category", category_options, horizontal=True)
            else:
                selected_category = "All Categories"

        # Filter events in selected date range and category
        active_events = []
        if show_events and events:
            for ev in events:
                ev_date = pd.to_datetime(ev["date"])
                if pd.to_datetime(start_date) <= ev_date <= pd.to_datetime(end_date):
                    if selected_category == "All Categories":
                        active_events.append(ev)
                    elif selected_category == "🇲🇾 Domestic Policy" and ev.get("category") == "Domestic Policy":
                        active_events.append(ev)
                    elif selected_category == "🌍 Global Oil Shock" and ev.get("category") == "Global Oil Shock":
                        active_events.append(ev)

        # Apply Filters
        filtered_df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]
        df_melted = filtered_df.melt(id_vars=['date'], value_vars=selected_fuels, var_name='Fuel Type', value_name='Price')

        # Plotly Line Chart
        if not df_melted.empty:
            chart_title = 'Weekly Fuel Price Trends with Key Historical Events' if active_events else 'Weekly Fuel Price Trends'
            fig = px.line(df_melted, x='date', y='Price', color='Fuel Type',
                          title=chart_title,
                          labels={'date': 'Date', 'Price': 'Price/Litre (MYR)', 'Fuel Type': 'Fuel Type'},
                          markers=True)

            # Add vertical dashed lines with badges for active events
            for ev in active_events:
                fig.add_vline(
                    x=pd.to_datetime(ev["date"]).timestamp() * 1000,
                    line_width=1.5,
                    line_dash="dash",
                    line_color=ev.get("color", "#7f7f7f"),
                    annotation_text=ev.get("badge", ev.get("title", "")),
                    annotation_position="top left",
                    annotation_font_size=10,
                    annotation_font_color="#ffffff",
                    annotation_bgcolor=ev.get("color", "#7f7f7f")
                )

            st.plotly_chart(fig, use_container_width=True)

            # Event Timeline Expander
            if active_events:
                with st.expander(f"📰 Key Historical Events in Selected Period ({len(active_events)})", expanded=True):
                    for ev in active_events:
                        badge = ev.get("badge", "")
                        title = ev.get("title", "")
                        date_str = ev.get("date", "")
                        desc = ev.get("description", "")
                        color = ev.get("color", "#1f77b4")
                        st.markdown(
                            f"""
                            <div style="border-left: 4px solid {color}; padding-left: 10px; margin-bottom: 12px;">
                                <strong>{date_str}</strong> | <span style="background-color: {color}; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.85em;">{badge}</span> <strong>{title}</strong>
                                <p style="margin: 4px 0 0 0;">{desc}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
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
    last_updated = df['date'].max().strftime('%Y-%m-%d') if (fuel_data and 'df' in locals() and not df.empty) else "N/A"
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="text-align: left;">
            🔄 <strong>Data last updated:</strong> {last_updated}
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="text-align: right;">
            📡 <strong>Source:</strong> <a href="https://api.data.gov.my/data-catalogue?meta=True&filter=level@series_type&id=fuelprice" target="_blank">DOSM Open API</a>
        </div>
        """, unsafe_allow_html=True)
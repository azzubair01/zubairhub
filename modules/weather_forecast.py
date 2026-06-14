import os
import logging
import requests
import datetime
import pandas as pd
import streamlit as st
import plotly.express as px

# Weather condition to image mapping
WEATHER_IMAGES = {
    "default": None
}

API_BASE_URL = 'https://api.data.gov.my/weather/forecast'

def fetch_weather_data(location):
    """Fetch weather forecast data for the selected location."""
    params = {
        "filter": f"{location}@location__location_name",
        "contains": "Ds@location__location_id"
    }
    try:
        response = requests.get(API_BASE_URL, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return data if isinstance(data, list) else []
    except requests.RequestException as e:
        logging.error(f"Failed to fetch weather data: {e}")
        return []

def get_weather_image(weather_status):
    """Return the appropriate weather image based on the forecast."""
    # Since images are missing, returning None to avoid MediaFileStorageError
    return None

def weather_forecast():
    st.title("📊 Weather Forecast")

    # Select location
    location_list = ['Kuala Lumpur', 'Kota Bharu', 'Jasin', 'Alor Gajah', 'Asajaya',
                     'Bachok', 'Bagan Datuk', 'Baling',
                     'Bandar Baharu', 'Barat Daya', 'Batang Padang', 'Batu Pahat',
                     'Bau', 'Beaufort', 'Belaga', 'Beluran', 'Beluru', 'Bentong',
                     'Bera', 'Besut', 'Betong', 'Bintulu', 'Bukit Mabong', 'Dalat',
                     'Daro', 'Dungun', 'FP Labuan', 'Gombak', 'Gua Musang', 'Hilir Perak',
                     'Hulu Langat', 'Hulu Perak', 'Hulu Selangor', 'Hulu Terengganu',
                     'Jelebu', 'Jeli', 'Jempol', 'Jerantut', 'Johor Bahru',
                     'Julau', 'Kabong', 'Kampar', 'Kanowit', 'Kapit', 'Kemaman', 'Keningau',
                     'Kerian', 'Kinabatangan', 'Kinta', 'Klang', 'Kluang', 'Kota Belud',
                     'Kota Kinabalu', 'Kota Marudu', 'Kota Setar', 'Kota Tinggi',
                     'Kuala Kangsar', 'Kuala Krai', 'Kuala Langat', 'Kuala Muda',
                     'Kuala Nerus', 'Kuala Penyu', 'Kuala Pilah', 'Kuala Selangor', 'Kuala Terengganu',
                     'Kuantan', 'Kubang Pasu', 'Kuching', 'Kudat', 'Kulai', 'Kulim', 'Kunak', 'Lahad Datu',
                     'Langkawi', 'Larut, Matang Dan Selama', 'Lawas', 'Limbang', 'Lipis', 'Lubok Antu',
                     'Lundu', 'Machang', 'Manjung', 'Maran', 'Marang', 'Marudi', 'Matu', 'Melaka Tengah',
                     'Meradong', 'Mersing', 'Miri', 'Muallim', 'Muar', 'Mukah', 'Nabawan', 'Padang Terap',
                     'Pakan', 'Papar', 'Pasir Mas', 'Pasir Puteh', 'Pekan', 'Penampang', 'Pendang', 'Perak Tengah',
                     'Perlis', 'Petaling', 'Pitas', 'Pokok Sena', 'Pontian', 'Port Dickson', 'Pusa', 'Putatan',
                     'Putrajaya', 'Ranau', 'Raub', 'Rembau', 'Rompin', 'Sabak Bernam', 'Samarahan', 'Sandakan',
                     'Saratok', 'Sarikei', 'Sebauh', 'Seberang Perai Selatan', 'Seberang Perai Tengah',
                     'Seberang Perai Utara', 'Segamat', 'Selangau', 'Semporna', 'Sepang', 'Seremban',
                     'Serian', 'Setiu', 'Sibu', 'Sik', 'Simunjan', 'Sipitang', 'Song', 'Sri Aman', 'Subis',
                     'Tambunan', 'Tampin', 'Tanah Merah', 'Tanah Tinggi Cameron', 'Tangkak', 'Tanjung Manis',
                     'Tatau', 'Tawau', 'Tebedu', 'Telang Usan', 'Telupid', 'Temerloh', 'Tenom', 'Timur Laut',
                     'Tongod', 'Tuaran', 'Tumpat', 'Yan']
    location = st.selectbox('Select location', location_list)

    # Fetch weather data
    weather_data = fetch_weather_data(location)

    # Get current weather status & display image
    current_weather = weather_data[0].get("summary_forecast", "default") if weather_data else "default"
    weather_image = get_weather_image(current_weather)
    if weather_image:
        st.image(weather_image, use_column_width=True)

    # Process data for display
    if weather_data:
        df = pd.DataFrame(weather_data).sort_values(by='date')
        df["date"] = pd.to_datetime(df["date"])

        # Plot Temperature Trends
        today_date = datetime.date.today().strftime('%Y-%m-%d')
        fig_temp = px.line(df, x="date", y=["min_temp", "max_temp"],
                           title="📈 Temperature Trends",
                           markers=True, labels={"value": "Temperature (°C)", "date": "Date"},
                           color_discrete_map={"min_temp": "blue", "max_temp": "red"})
        fig_temp.add_vline(x=pd.to_datetime(today_date), line_dash="dash", line_color="green")
        st.plotly_chart(fig_temp)

        # Display Forecast Details in a Table
        st.subheader("📅 Daily Forecast Details")
        st.dataframe(
            data=df[["date", "morning_forecast", "afternoon_forecast", "night_forecast", "summary_forecast"]],
            column_config={
                "date": st.column_config.DateColumn()
            },
            hide_index=True,
            width='stretch'
        )

        # Footer
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style="text-align: left;">
                🔄 <strong>Data last updated:</strong> {today_date}
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style="text-align: right;">
                📡 <strong>Source:</strong> <a href="https://api.data.gov.my/weather/forecast" target="_blank">DOSM Open API</a>
            </div>
            """, unsafe_allow_html=True)
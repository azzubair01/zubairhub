import os
import logging
import requests
import datetime
import pandas as pd
import streamlit as st
import plotly.express as px


def weather_forecast():
    # Streamlit App Title
    st.title(f"📊 Weather Forecast")

    location_list = ['Alor Gajah', 'Asajaya', 'Bachok', 'Bagan Datuk', 'Baling',
                     'Bandar Baharu', 'Barat Daya', 'Batang Padang', 'Batu Pahat',
                     'Bau', 'Beaufort', 'Belaga', 'Beluran', 'Beluru', 'Bentong',
                     'Bera', 'Besut', 'Betong', 'Bintulu', 'Bukit Mabong', 'Dalat',
                     'Daro', 'Dungun', 'FP Labuan', 'Gombak', 'Gua Musang', 'Hilir Perak',
                     'Hulu Langat', 'Hulu Perak', 'Hulu Selangor', 'Hulu Terengganu',
                     'Jasin', 'Jelebu', 'Jeli', 'Jempol', 'Jerantut', 'Johor Bahru',
                     'Julau', 'Kabong', 'Kampar', 'Kanowit', 'Kapit', 'Kemaman', 'Keningau',
                     'Kerian', 'Kinabatangan', 'Kinta', 'Klang', 'Kluang', 'Kota Belud',
                     'Kota Bharu', 'Kota Kinabalu', 'Kota Marudu', 'Kota Setar', 'Kota Tinggi',
                     'Kuala Kangsar', 'Kuala Krai', 'Kuala Langat', 'Kuala Lumpur', 'Kuala Muda',
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
    location = st.selectbox(label='Select location', options=location_list, key='Select bos for location in weather forecast')
    BASE_URL = 'https://api.data.gov.my/'
    ENDPOINT = f'weather/forecast?filter={location}@location__location_name&contains=Ds@location__location_id'
    FULL_URL = os.path.join(BASE_URL,ENDPOINT)
    response = requests.get(FULL_URL)

    weather_forecast = pd.DataFrame()
    if response.status_code == 200:
        weather_forecast = response.json()
        logging.info(f'API Call Status: {response.status_code}')
    else:
        logging.error(f'API Call Status: {response.status_code}')

    weather_forecast_df = pd.DataFrame(weather_forecast).sort_values(by='date')
    weather_forecast_df["date"] = pd.to_datetime(weather_forecast_df["date"])  # Convert date column to datetime

    # Plot Temperature Trends
    fig_temp = px.line(weather_forecast_df, x="date", y=["min_temp", "max_temp"],
                       title="📈 Temperature Trends",
                       markers=True, labels={"value": "Temperature (°C)", "date": "Date"},
                       color_discrete_map={"min_temp": "blue", "max_temp": "red"})
    # Add vertical line
    today_date = datetime.date.today().strftime('%Y-%m-%d')
    vertical_line_date = pd.to_datetime(today_date)  # Change this to your desired date
    fig_temp.add_vline(x=vertical_line_date, line_dash="dash", line_color="green")

    st.plotly_chart(fig_temp)

    # Display Forecast Details in a Table
    st.subheader("📅 Daily Forecast Details")
    st.dataframe(
        data=weather_forecast_df[["date", "morning_forecast", "afternoon_forecast", "night_forecast", "summary_when", "summary_forecast"]],
        column_config={
            'date': st.column_config.DateColumn()
        },
        hide_index=True,
        use_container_width=True
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
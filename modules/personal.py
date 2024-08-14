import io
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime


def generate_download_button(dataframe, filename):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        # Write each dataframe to a different worksheet.
        dataframe.to_excel(writer, sheet_name='Sheet1', index=False)

    download2 = st.download_button(
        label=f"Download {filename}.xlsx",
        data=buffer,
        file_name=f'{filename}.xlsx',
        mime="application/vnd.ms-excel",
        key=filename
    )

@st.fragment
def transform_sap_data():
    uploaded_file = st.file_uploader(label='Upload SAP data', key='Upload button for sap data')

    if uploaded_file:
        df_raw = pd.read_excel(uploaded_file, sheet_name='Sheet1')
        df_raw['Notification Date'] = pd.to_datetime(df_raw['Notification Date'])
        df_raw['Notification Time'] = pd.to_datetime(df_raw['Notification Time'], format='%H:%M:%S')
        df_raw['Call Log'] = df_raw.apply(lambda x: datetime.strptime(
            f'{x["Notification Date"].strftime("%Y-%m-%d")} {x["Notification Time"].strftime("%H:%M:%S")}',
            "%Y-%m-%d %H:%M:%S"), axis=1)

        df_raw['First OSR Start Time'] = df_raw['First OSR Start Time'].astype(str)
        df_raw['Last OSR Finish Date'] = df_raw['Last OSR Finish Date'].astype(str)

        df_raw['First OSR Start Date'] = df_raw['First OSR Start Date'].apply(
            lambda x: '-' if x == 'Not Applicable' else datetime.strptime(x, '%d.%m.%Y'))
        df_raw['First OSR Start Time'] = df_raw['First OSR Start Time'].str.replace('24:00:00', '00:00:00', regex=False)
        df_raw['First OSR Start Time'] = df_raw['First OSR Start Time'].apply(
            lambda x: '-' if x == 'Not Applicable' else datetime.strptime(x, '%H:%M:%S'))

        df_raw['Last OSR Finish Date'] = df_raw['Last OSR Finish Date'].apply(
            lambda x: '-' if x == 'Not Applicable' else datetime.strptime(x, '%d.%m.%Y'))
        df_raw['Last OSR Finish Time'] = df_raw['Last OSR Finish Time'].str.replace('24:00:00', '00:00:00', regex=False)
        df_raw['Last OSR Finish Time'] = df_raw['Last OSR Finish Time'].apply(
            lambda x: '-' if x == 'Not Applicable' else datetime.strptime(x, '%H:%M:%S'))

        df_raw['CSE OSR'] = df_raw.apply(lambda x: '-' if x["First OSR Start Date"] == '-' else datetime.strptime(
            f'{x["First OSR Start Date"].strftime("%Y-%m-%d")} {x["First OSR Start Time"].strftime("%H:%M:%S")}',
            "%Y-%m-%d %H:%M:%S"), axis=1)
        df_raw['Job Done'] = df_raw.apply(lambda x: '-' if x["Last OSR Finish Date"] == '-' else datetime.strptime(
            f'{x["Last OSR Finish Date"].strftime("%Y-%m-%d")} {x["Last OSR Finish Time"].strftime("%H:%M:%S")}',
            "%Y-%m-%d %H:%M:%S"), axis=1)
        df_raw['Customer Name1'] = df_raw['Customer Name1'].fillna('')
        df_raw['Customer Name1'] = df_raw.apply(
            lambda x: x['Functional Location Description'] if x['Customer Name1'] == '' else x['Customer Name1'],
            axis=1)
        df_raw['Customer Name1'] = df_raw['Customer Name1'].str.replace('Hosp Kemaman', 'Hospital Kemaman')
        df_raw['Customer Name1'] = df_raw['Customer Name1'].str.replace('Universiti Putra Malaysia-Serdang',
                                                                        'Hospital Pengajar UPM Serdang')
        df_raw['Scanning Affected, (x)'] = ''
        df_raw['Downtime, hr (D-A)'] = 0
        df_raw['Comments / Remarks'] = 'Refer FSR'

        df_agg = df_raw.groupby('Customer Name1').agg({'Notification': 'count'}).sort_values('Notification', ascending=False).reset_index()

        fig = px.bar(
            df_agg,
            x="Notification",
            y="Customer Name1",
            color="Customer Name1",
            text="Notification",
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)

        hospital_name_list = df_agg['Customer Name1'].tolist()

        cols = ['Notification Type', 'Call Log', 'Effect Code Text', 'Notification', 'Equipment Description',
                'Serial Number', 'Notification Text', 'Resolution Type',
                'Scanning Affected, (x)', 'CSE OSR', 'Job Done', 'Downtime, hr (D-A)',
                'Comments / Remarks']

        renamed_cols = {
            'Effect Code Text': 'Effect',
            'Equipment Description': 'System Name',
            'Notification Text': 'Description',
            'Resolution Type': 'Support Type'
        }

        for hospital in hospital_name_list:
            df_temp = df_raw[df_raw['Customer Name1'] == hospital]
            df_temp = df_temp.sort_values(by='Notification', ascending=True).reset_index(drop=True)
            df_temp = df_temp[cols]
            df_temp = df_temp.rename(renamed_cols, axis=1)
            # df_temp.to_excel(f"{hospital}.xlsx", index=False)
            generate_download_button(df_temp, hospital)

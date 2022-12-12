import streamlit as st
from PIL import Image
from io import BytesIO
import requests


def intro():
    image = Image.open(BytesIO(requests.get("https://cdn.nimbu.io/s/znvdo1j/channelentries/vbzcjzz/files/leverage%20data.jpeg?6hdixzz=&filter=w_1200%2Ch_400%2Cc_fill").content))
    st.image(image)

    text = "<h1 style='text-align: center; color: black;'>\
              🕵️ Welcome Readers!</h1>"

    st.markdown(text, unsafe_allow_html=True)
    st.write("---")

    st.write('## About Me')
    text = '<p style="font-family:sans-serif; color:Black; font-size: 18px;">' \
           '◉ A <span style="font-weight:bold; color:MediumBlue;"> Data Scientist </span>' \
           'with 3 years of experience in Business, and Artificial Intelligence </br>' \
           '◉ A constant learner and a firm believer of experimentation over expertise </br> ' \
           '◉ Passionate on Data driven solutions which are easy, economical and scalable'
    st.markdown(text, unsafe_allow_html=True)
    st.write("---")

    st.write('## My Experiences')
    #  '<figure><embed align="right" type="image/svg+xml" src="https://ade.aero/static/media/ADE-logo.80e854a7.svg" height="30"></figure>' \
    # '<figure><embed align="right" type="image/svg+xml" src="https://www.datamicron.com/img/logo.svg" height="35" ></figure>' \
    text = '<p style="font-family:sans-serif; color:Black; font-size: 18px;">' \
           '◉ <span style="font-weight:bold; color:MediumBlue;">Data Scientist II</span> (Sept 2021 - Present) - <b><i>Asia Digital Engineering Sdn Bhd</i></b></br>' \
           '&nbsp&nbsp&nbsp - <i>Provide Digital Innovation Services (Big Data) for AirAsia departments</i></br>' \
           '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp a) Query and transform data using Google BigQuery</br>' \
           '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp b) Build backend engines for data processing using Python on PyCharm</br>' \
           '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp c) Visualise data on Streamlit web application</br>' \
           '<p style="font-family:sans-serif; color:Black; font-size: 18px;">' \
           '◉ <span style="font-weight:bold; color:MediumBlue;">Junior Data Scientist</span> (July 2020 - Sept 2021) - <b><i>DataMicron Systems Sdn Bhd</i></b></br> ' \
           '&nbsp&nbsp&nbsp - <i>Deliver Big Data consultation services through POCs</i></br>' \
           '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp a) Transform and process data using EzData and Python</br>' \
           '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp b) Perform prediction and forecasting using DataMicron Foresight</br>' \
           '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp c) Provide Artificial Intelligence modules for DataMicron EagleEye</br>' \
           '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp d) Visualise Business Intelligence dashboards using DataMicron InstaBI</br>'
    st.markdown(text, unsafe_allow_html=True)
    st.write("---")

    st.write('## My Education')
    # '<figure><embed align="right" type="image/svg+xml" src="https://www.freelogovectors.net/svg09/universiti-sains-malaysia-logo-freelogovectors.net_.svg" width="150" ></figure>' \
    # '<figure><embed align="right" type="image/svg+xml" src="https://upload.wikimedia.org/wikipedia/commons/f/f7/IIUM_Logo_.svg" width="170" ></figure>' \
    text = '<p style="font-family:sans-serif; color:Black; font-size: 18px;">' \
           '◉ <span style="font-weight:bold; color:Purple;">Master of Science (Data Science & Analytics)</span> - <b><i>Universiti Sains Malaysia</i></b></br>' \
           '&nbsp&nbsp&nbsp - <i>Obtain foundations on Data Science and Analytics</i></br>' \
           '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 1) Principles and Practices of Data Science and Analytics</br>' \
           '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 2) Machine Learning</br>' \
           '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 3) Big Data Storage and Management</br>' \
           '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 4) Data Visualisation and Visual Analytics</br>' \
           '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 5) Social Media Analytics</br>' \
           '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 6) Multimodal Information Retrieval</br>' \
           '<p style="font-family:sans-serif; color:Black; font-size: 18px;">' \
           '◉ <span style="font-weight:bold; color:Purple;">Bachelor of Science (Applied Chemistry)</span> - <b><i>Universiti Islam Antarabangsa Malaysia</i></b> </br> ' \
           '&nbsp&nbsp&nbsp - <i>Obtain foundations and best practices of Applied Chemistry</i></br>' \
           '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 1) Organic Chemistry</br>' \
           '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 2) Inorganic Chemistry</br>' \
           '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 3) Analytical Chemistry</br>' \
           '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 4) Food Chemistry</br>' \
           '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 5) Analytical Spectroscopy</br>' \
           '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 6) Natural Product</br>'
    st.markdown(text, unsafe_allow_html=True)
    st.write("---")

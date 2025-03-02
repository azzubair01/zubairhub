import streamlit as st


@st.fragment
def intro():


    text = "<h1 style='text-align: center; color: black;'>\
              🕵️ Welcome Readers!</h1>"

    st.markdown(text, unsafe_allow_html=True)
    st.write("---")

    st.write('## About Me')
    text = '<p style="font-family:sans-serif; color:Black; font-size: 18px;">' \
           '◉ A <span style="font-weight:bold; color:MediumBlue;"> Data Scientist </span>' \
           'with 4 years of experience in Data Science and Analysis </br>' \
           '◉ A constant learner and a firm believer of experimentation over expertise </br> ' \
           '◉ Passionate on Data driven solutions which are easy, economical and scalable'
    st.markdown(text, unsafe_allow_html=True)
    st.write("---")

    st.write('## My Experiences')
    #  \
    # '<figure><embed align="right" type="image/svg+xml" src="https://www.datamicron.com/img/logo.svg" height="35" ></figure>' \
    # '<figure><embed align="right" type="image/svg+xml" src="	https://ade.aero/static/media/ADE-logo.80e854a71ef3aba1ae99a21ff47eecfe.svg" height="30"></figure>' \

    text = '<p style="font-family:sans-serif; color:Black; font-size: 18px;">' \
        '◉ <span style="font-weight:bold; color:MediumBlue;">Data Scientist II</span> (Sept 2021 - Present) - <b><i>Asia Digital Engineering Sdn Bhd</i></b></br>' \
        '&nbsp&nbsp&nbsp - <i>Provide Digital Innovation Services for AirAsia departments</i></br>' \
        '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp a) Provide od_data services for inter and intra-departments</br>' \
        '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp b) Build od_data pipeline for od_data extraction, transformation and load</br>' \
        '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp c) Deliver od_data analysis and insights on aviation engineering operations</br>' \
        '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp d) Implement Artificial Intelligence solutions for Aviation Digitalisation</br>' \
        '<p style="font-family:sans-serif; color:Black; font-size: 18px;">' \
        '◉ <span style="font-weight:bold; color:MediumBlue;">Junior Data Scientist</span> (July 2020 - Sept 2021) - <b><i>DataMicron Systems Sdn Bhd</i></b></br> ' \
        '&nbsp&nbsp&nbsp - <i>Deliver Big Data consultation services through POCs</i></br>' \
        '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp a) Transform and process od_data using EzData and Python</br>' \
        '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp b) Perform prediction and forecasting using DataMicron Foresight</br>' \
        '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp c) Provide Artificial Intelligence modules for DataMicron EagleEye</br>' \
        '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp d) Visualise Business Intelligence dashboards using DataMicron InstaBI</br>'
    st.markdown(text, unsafe_allow_html=True)

    st.divider()

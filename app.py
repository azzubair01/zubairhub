import streamlit as st
from PIL import Image
from io import BytesIO
import requests

st.set_page_config(page_title="Azzubair's Webapp", page_icon="📊", layout='centered')

image = Image.open(BytesIO(requests.get("https://cdn.wallpapersafari.com/49/5/x3u5bU.jpg").content))
st.image(image)

text = "<h1 style='text-align: center; color: black;'>\
          🕵️ Welcome Readers!</h1>"

st.markdown(text, unsafe_allow_html=True)
st.write("---")

image = Image.open(BytesIO(requests.get("https://scontent.fkul16-2.fna.fbcdn.net/v/t39.30808-6/210187710_4135796173126331_5137455833497972237_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=174925&_nc_ohc=rzob6XFgv9MAX9ACEiT&_nc_oc=AQmvd70bDWS1l4Lq786gQb8EDjVG8VKP9Eh8PUuJNt8Mfsv6XTFfxhlPIIMtKjJDHscODwJOdWThcNxoViQIEevI&tn=ry9UFMse0NLNkbzR&_nc_ht=scontent.fkul16-2.fna&oh=00_AfBDkatuGsacwzRbI1UCCR3doEauJfaW2Ysu-BxpFVwKoA&oe=63629B22").content))
newsize = (300, 300)
image = image.resize(newsize)

st.sidebar.image(image)
text = '<p style="font-family:sans-serif; color:Black; font-size: 16px;">' \
       '◉ Muhammad Azzubair bin Azeman </br>' \
       '◉ Gombak, Selangor</br>' \
       '◉ azzubairazeman@gmail.com'
st.sidebar.markdown(text,  unsafe_allow_html=True)

st.sidebar.write('---')
st.sidebar.title('Navigation')
st.sidebar.radio('Select project to display:', ('Introduction', ))


st.write('## About Me')
text = '<p style="font-family:sans-serif; color:Black; font-size: 18px;">' \
       '◉ A <span style="font-weight:bold; color:MediumBlue;"> Data Scientist </span>' \
       'with 3 years of experience in Business, and Artificial Intelligence </br>'\
       '◉ A constant learner and a firm believer of experimentation over expertise </br> '\
       '◉ Passionate on Data driven solutions which are easy, economical and scalable'
st.markdown(text, unsafe_allow_html=True)
st.write("---")

st.write('## My Experiences')
text = '<figure><embed align="right" type="image/svg+xml" src="https://ade.aero/static/media/ADE-logo.80e854a7.svg" height="30"></figure>'\
       '<p style="font-family:sans-serif; color:Black; font-size: 18px;">' \
       '◉ <span style="font-weight:bold; color:MediumBlue;">Data Scientist II</span> (Sept 2021 - Present) </br>' \
       '&nbsp&nbsp&nbsp - <i>Provide Digital Innovation Services (Big Data) for AirAsia departments</i></br>' \
       '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp a) Query and transform data using Google BigQuery</br>' \
       '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp b) Build backend engines for data processing using Python on PyCharm</br>' \
       '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp c) Visualise data on Streamlit web application</br>' \
       '<figure><embed align="right" type="image/svg+xml" src="https://www.datamicron.com/img/logo.svg" height="35" ></figure>' \
       '<p style="font-family:sans-serif; color:Black; font-size: 18px;">'\
       '◉ <span style="font-weight:bold; color:MediumBlue;">Junior Data Scientist</span> (July 2020 - Sept 2021)</br> '\
       '&nbsp&nbsp&nbsp - <i>Deliver Big Data consultation services through POCs</i></br>'\
       '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp a) Transform and process data using EzData and Python</br>'\
       '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp b) Perform prediction and forecasting using DataMicron Foresight</br>'\
       '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp c) Provide Artificial Intelligence modules for DataMicron EagleEye</br>'\
       '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp d) Visualise Business Intelligence dashboards using DataMicron InstaBI</br>'\

st.markdown(text, unsafe_allow_html=True)
st.write("---")


st.write('## My Education')
text = '<figure><embed align="right" type="image/svg+xml" src="https://www.freelogovectors.net/svg09/universiti-sains-malaysia-logo-freelogovectors.net_.svg" width="150" ></figure>' \
       '<p style="font-family:sans-serif; color:Black; font-size: 18px;">' \
       '◉ <span style="font-weight:bold; color:Purple;">Master of Science (Data Science & Analytics)</span></br>' \
       '&nbsp&nbsp&nbsp - <i>Obtain foundations on Data Science and Analytics</i></br>' \
       '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 1) Principles and Practices of Data Science and Analytics</br>' \
       '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 2) Machine Learning</br>' \
       '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 3) Big Data Storage and Management</br>' \
       '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 4) Data Visualisation and Visual Analytics</br>' \
       '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 5) Social Media Analytics</br>' \
       '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 6) Multimodal Information Retrieval</br>' \
       '<figure><embed align="right" type="image/svg+xml" src="https://upload.wikimedia.org/wikipedia/commons/f/f7/IIUM_Logo_.svg" width="150" ></figure>' \
       '<p style="font-family:sans-serif; color:Black; font-size: 18px;">' \
       '◉ <span style="font-weight:bold; color:Purple;">Bachelor of Science (Applied Chemistry)</span>  </br> ' \
       '&nbsp&nbsp&nbsp - <i>Obtain foundations and best practices of Applied Chemistry</i></br>' \
       '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 1) Organic Chemistry</br>' \
       '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 2) Inorganic Chemistry</br>' \
       '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 3) Analytical Chemistry</br>' \
       '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 4) Food Chemistry</br>' \
       '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 5) Analytical Spectroscopy</br>' \
       '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 6) Natural Product</br>' \

st.markdown(text, unsafe_allow_html=True)
st.write("---")
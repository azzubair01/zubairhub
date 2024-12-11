import streamlit as st
from PIL import Image
from io import BytesIO
import requests
from modules.social_graph import (family_graph)
from modules.introduction import (intro)
from modules.personal import transform_sap_data
from modules.computer_vision import detect_object


st.set_page_config(page_title="Azzubair's Webapp", page_icon="📊", layout='centered')

st.sidebar.title('My Profile')

style_image1 = """
width: auto;
max-width: 150px;
height: auto;
max-height: 500px;
display: block;
margin-left: auto;
margin-right: auto;
justify-content: center;
border-radius: 25%;
"""

st.sidebar.markdown(
    f'<img src="{"https://avatars.githubusercontent.com/u/52235533?s=400&u=933b82feeb4ec3f9278f6b66cf02d9d5ad351a72&v=4"}" style="{style_image1}">',
    unsafe_allow_html=True,
)

text = '<p style="font-family:sans-serif; color:Black; font-size: 16px;">' \
       '◉ Muhammad Azzubair bin Azeman </br>' \
       '◉ Gombak, Selangor</br>' \
       '◉ azzubairazeman@gmail.com'
st.sidebar.markdown(text, unsafe_allow_html=True)

st.sidebar.write('---')
st.sidebar.title('Navigation')
page_names_to_func = {
    'Introduction': intro,
    'Family Graph': family_graph,
    'Object Detection': detect_object,
    'Personal': transform_sap_data,

}

project_select = st.sidebar.radio('Select project to display:', (list(page_names_to_func.keys())))
page_names_to_func[project_select]()




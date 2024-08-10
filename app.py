import streamlit as st
from PIL import Image
from io import BytesIO
import requests
from modules.social_graph import (family_graph)
from modules.introduction import (intro)
from modules.computer_vision import detect_labels


st.set_page_config(page_title="Azzubair's Webapp", page_icon="📊", layout='centered')

st.sidebar.title('My Profile')
image = Image.open(BytesIO(requests.get(
    "https://avatars.githubusercontent.com/u/52235533?s=400&u=933b82feeb4ec3f9278f6b66cf02d9d5ad351a72&v=4").content))
newsize = (300, 300)
image = image.resize(newsize)

st.sidebar.image(image)
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
    'Computer Vision': detect_labels
}

project_select = st.sidebar.radio('Select project to display:', (list(page_names_to_func.keys())))
page_names_to_func[project_select]()




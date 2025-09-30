from modules.setup import initialise_page

page_title = "Azzubair's Webapp"
initialise_page(
    page_title=page_title,
    page_icon="😎",
    layout='centered'
)

import streamlit as st
from modules.social_graph import family_graph
from modules.introduction import intro
from modules.personal import transform_sap_data
# from modules.computer_vision import detect_object, extract_text
# from modules.natural_language import parse_document
from modules.artificial_intelligence import generative_ai
from modules.weather_forecast import weather_forecast
from modules.fuel_price import fuel_price


st.sidebar.title('Navigation')
page_names_to_func = {
    '📌 Introduction': intro,
    '👨‍👩‍👧‍👦 Family Graph': family_graph,
    # '📷 Object Detection': detect_object,
    # '📄 Document Parsing': parse_document,
    # '🔍 Text Extraction': extract_text,
    '🔮 Generative AI': generative_ai,
    '🌥️ Weather Forecast': weather_forecast,
    '⛽ Fuel Price': fuel_price,
    '💼 Personal': transform_sap_data,
}

project_select = st.sidebar.radio('Select project to display:', (list(page_names_to_func.keys())))
page_names_to_func[project_select]()




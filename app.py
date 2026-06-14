import streamlit as st
from modules.setup import initialise_page
from modules.utils.generative_ai import initialise_quotas

page_title = "Azzubair's Webapp"
initialise_page(
    page_title=page_title,
    page_icon="😎",
    layout='wide'
)

# Initialize quotas in session state
initialise_quotas()

st.sidebar.title('Navigation')

# Model Configuration with Quota Info
st.sidebar.subheader("Model Configuration")
MODELS = {
    "Gemini 3.5 Flash": "gemini-3.5-flash",
    "Gemini 2.0 Flash": "gemini-2.0-flash",
    "Gemini 1.5 Flash": "gemini-1.5-flash",
}
selected_model_display = st.sidebar.selectbox(
    "Select Model:",
    options=list(MODELS.keys()),
    index=0  # Default to 3.5 Flash
)
selected_model_id = MODELS[selected_model_display]
st.session_state.selected_model = selected_model_id

# Display Quota Left
if 'quota_usage' in st.session_state and selected_model_id in st.session_state.quota_usage:
    quota = st.session_state.quota_usage[selected_model_id]
    total_rpd = 1500 # Default total RPD for Free Tier
    percentage = (quota['RPD_left'] / total_rpd) * 100
    st.sidebar.metric(
        "Quota Left (RPD)", 
        f"{quota['RPD_left']} / {total_rpd}", 
        f"{percentage:.1f}%"
    )
    st.sidebar.caption("RPD = Requests Per Day (Free Tier estimate)")

st.sidebar.markdown("---")

def load_intro():
    from modules.introduction import intro
    return intro

def load_family_graph():
    from modules.social_graph import family_graph
    return family_graph

def load_detect_object():
    from modules.computer_vision import detect_object
    return detect_object

def load_parse_document():
    from modules.natural_language import parse_document
    return parse_document

def load_extract_text():
    from modules.computer_vision import extract_text
    return extract_text

def load_generative_ai():
    from modules.artificial_intelligence import generative_ai
    return generative_ai

def load_bank_statement_parser():
    from modules.bank_parser import bank_statement_parser
    return bank_statement_parser

def load_weather_forecast():
    from modules.weather_forecast import weather_forecast
    return weather_forecast

def load_fuel_price():
    from modules.fuel_price import fuel_price
    return fuel_price

def load_transform_sap_data():
    from modules.personal import transform_sap_data
    return transform_sap_data

page_names_to_func = {
    '📌 Introduction': load_intro(),
    '👨‍👩‍👧‍👦 Family Graph': load_family_graph(),
    '📷 Object Detection': load_detect_object(),
    '📄 Document Parsing': load_parse_document(),
    '🔍 Text Extraction': load_extract_text(),
    '🔮 Generative AI': load_generative_ai(),
    '🏦 Bank Statement Parser': load_bank_statement_parser(),
    '🌥️ Weather Forecast': load_weather_forecast(),
    '⛽ Fuel Price': load_fuel_price(),
    '💼 Personal': load_transform_sap_data(),
}

project_select = st.sidebar.radio('Select project to display:', (list(page_names_to_func.keys())))
page_names_to_func[project_select]()




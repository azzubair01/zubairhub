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

def render_intro():
    from modules.introduction import intro
    intro()

def render_family_graph():
    from modules.social_graph import family_graph
    family_graph()

def render_detect_object():
    from modules.computer_vision import detect_object
    detect_object()

def render_parse_document():
    from modules.natural_language import parse_document
    parse_document()

def render_extract_text():
    from modules.computer_vision import extract_text
    extract_text()

def render_generative_ai():
    from modules.artificial_intelligence import generative_ai
    generative_ai()

def render_bank_statement_parser():
    from modules.bank_parser import bank_statement_parser
    bank_statement_parser()

def render_weather_forecast():
    from modules.weather_forecast import weather_forecast
    weather_forecast()

def render_fuel_price():
    from modules.fuel_price import fuel_price
    fuel_price()

def render_transform_sap_data():
    from modules.personal import transform_sap_data
    transform_sap_data()

page_names_to_func = {
    '📌 Introduction': render_intro,
    '👨‍👩‍👧‍👦 Family Graph': render_family_graph,
    '📷 Object Detection': render_detect_object,
    '📄 Document Parsing': render_parse_document,
    '🔍 Text Extraction': render_extract_text,
    '🔮 Generative AI': render_generative_ai,
    '🏦 Bank Statement Parser': render_bank_statement_parser,
    '🌥️ Weather Forecast': render_weather_forecast,
    '⛽ Fuel Price': render_fuel_price,
    '💼 Personal': render_transform_sap_data,
}

project_select = st.sidebar.radio('Select project to display:', (list(page_names_to_func.keys())))

st.sidebar.markdown("---")

# Model Configuration with Quota Info - ONLY for Bank Statement Parser
if project_select == '🏦 Bank Statement Parser':
    st.sidebar.subheader("Model Configuration")
    MODELS = {
        "Gemini 2.0 Flash": "gemini-2.0-flash",
        "Gemini 1.5 Flash": "gemini-1.5-flash",
    }
    selected_model_display = st.sidebar.selectbox(
        "Select Model:",
        options=list(MODELS.keys()),
        index=0  # Default to 2.0 Flash
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
else:
    # Ensure a default model is set for other modules that might use it
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = "gemini-2.0-flash"

page_names_to_func[project_select]()




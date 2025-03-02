import streamlit as st

def initialise_page(
        page_title: str = "Template DB | ADE",
        page_icon: str = "🤖",
        layout: str = "wide",
        initial_sidebar_state: str = "expanded",

):
    ## on top because streamlit doesn't like it :(
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout=layout,
        initial_sidebar_state=initial_sidebar_state,
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': "This app is created to extract tasklisting that are absent in the current shared folder"
        }
    )

    style_image = """
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
        f'<img src="{"https://avatars.githubusercontent.com/u/52235533?s=400&u=933b82feeb4ec3f9278f6b66cf02d9d5ad351a72&v=4"}" style="{style_image}">',
        unsafe_allow_html=True,
    )

    text = '<p style="font-family:sans-serif; color:Black; font-size: 16px;">' \
           '◉ Muhammad Azzubair Azeman </br>' \
           '◉ Cheras, Selangor</br>' \
           '◉ azzubairazeman@gmail.com'
    st.sidebar.markdown(text, unsafe_allow_html=True)

    st.sidebar.write('---')


def reset_session(soft=False):
    if not soft:
        for key in st.session_state.keys():
            del st.session_state[key]
    st.cache_data.clear()
    st.rerun()


def setup_session_state():
    if "tasklisting_sheet" not in st.session_state.keys():
        st.session_state['tasklisting_sheet'] = None
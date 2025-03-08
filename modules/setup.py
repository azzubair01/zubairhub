import streamlit as st

def initialise_page(
        page_title: str = "Template DB | ADE",
        page_icon: str = "🤖",
        layout: str = "wide",
        initial_sidebar_state: str = "expanded",
):
    # Set Streamlit page config
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout=layout,
        initial_sidebar_state=initial_sidebar_state,
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': "This app is created to extract task listings that are absent in the current shared folder."
        }
    )

    # Style for profile image
    style_image = """
        width: auto;
        max-width: 130px;
        height: auto;
        max-height: 500px;
        display: block;
        margin-left: auto;
        margin-right: auto;
        border-radius: 50%;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
    """

    # Sidebar profile image
    st.sidebar.markdown(
        f'<img src="{"https://avatars.githubusercontent.com/u/52235533?s=400&u=933b82feeb4ec3f9278f6b66cf02d9d5ad351a72&v=4"}" style="{style_image}">',
        unsafe_allow_html=True,
    )

    # Sidebar profile info
    st.sidebar.markdown(
        """
        <div style="text-align: left; font-family: Arial, sans-serif;">
            <h3>👤 Muhammad Azzubair Azeman</h3>
            <p>📍 Cheras, Selangor</p>
            <p>📧 <a href="mailto:azzubairazeman@gmail.com" style="color: #0072B1; text-decoration: none;">azzubairazeman@gmail.com</a></p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.write("---")


def reset_session(soft=False):
    if not soft:
        for key in st.session_state.keys():
            del st.session_state[key]
    st.cache_data.clear()
    st.rerun()


def setup_session_state():
    if "tasklisting_sheet" not in st.session_state.keys():
        st.session_state['tasklisting_sheet'] = None

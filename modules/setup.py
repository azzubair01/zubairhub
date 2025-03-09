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
            'About': "This app is designed to extract task listings missing from the shared folder."
        }
    )

    # Sidebar Profile Card
    st.sidebar.markdown(
        """
        <style>
            .profile-card {
                text-align: center;
                padding: 20px;
                border-radius: 12px;
                background: #f8f9fa;
                box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.1);
                font-family: 'Arial', sans-serif;
            }
            .profile-img {
                width: 110px;
                height: 110px;
                border-radius: 50%;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.15);
                margin-bottom: 10px;
            }
            .profile-name {
                font-size: 18px;
                font-weight: bold;
                color: #222;
                margin-bottom: 5px;
            }
            .profile-info {
                font-size: 15px;
                color: #555;
                margin: 4px 0;
            }
            .profile-links a {
                color: #0072B1;
                text-decoration: none;
                font-weight: bold;
            }
            .profile-links a:hover {
                text-decoration: underline;
            }
        </style>

        <div class="profile-card">
            <img src="https://avatars.githubusercontent.com/u/52235533?s=400&u=933b82feeb4ec3f9278f6b66cf02d9d5ad351a72&v=4" class="profile-img">
            <div class="profile-name">👤 Azzubair Azeman</div>
            <div class="profile-info">📍 Cheras, Selangor</div>
            <div class="profile-info">📧 <a href="mailto:azzubairazeman@gmail.com" class="profile-links">azzubairazeman@gmail.com</a></div>
            <div class="profile-info profile-links">
                🔗 <a href="https://github.com/azzubair01" target="_blank">GitHub</a> | 
                🔗 <a href="https://www.linkedin.com/in/azzubair-azeman-b96222142/" target="_blank">LinkedIn</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.divider()


def reset_session(soft=False):
    if not soft:
        for key in st.session_state.keys():
            del st.session_state[key]
    st.cache_data.clear()
    st.rerun()


def setup_session_state():
    if "tasklisting_sheet" not in st.session_state.keys():
        st.session_state['tasklisting_sheet'] = None

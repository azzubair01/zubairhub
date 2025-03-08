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
                text-align: left;
                padding: 15px;
                border-radius: 12px;
                background: #f8f9fa;
                box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.15);
                font-family: Arial, sans-serif;
            }
            .profile-img-container {
                text-align: center;
                margin-bottom: 10px;
            }
            .profile-img {
                width: 120px;
                height: 120px;
                border-radius: 50%;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
            }
            .profile-name {
                font-size: 16px;
                font-weight: bold;
                color: #333;
            }
            .profile-info {
                font-size: 16px;
                color: #555;
                margin: 5px 0;
            }
            .email-link {
                color: #0072B1;
                text-decoration: none;
                font-weight: bold;
            }
        </style>

        <div class="profile-card">
            <div class="profile-img-container">
                <img src="https://avatars.githubusercontent.com/u/52235533?s=400&u=933b82feeb4ec3f9278f6b66cf02d9d5ad351a72&v=4" class="profile-img">
            </div>
            <div class="profile-name">👤 Muhammad Azzubair Azeman</div>
            <div class="profile-info">📍 Cheras, Selangor</div>
            <div class="profile-info">📧 <a href="mailto:azzubairazeman@gmail.com" class="email-link">azzubairazeman@gmail.com</a></div>
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

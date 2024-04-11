import streamlit as st 
from streamlit_option_menu import option_menu
import dashboard, sentiment


def uif():
    st.markdown("""
        <style>
            .block-container {
                padding-top: 2rem;
                padding-bottom: 0rem;
                padding-left: 5rem;
                padding-right: 5rem;
            }
            .sidebar .sidebar-content {
                padding-top: 0px !important;
                padding-bottom: 0px !important;
            }
            .sidebar .stImage {
                margin-top: -10px !important;
                margin-bottom: -10px !important;
            }
            section[data-testid="stSidebar"] {
                width: 270px !important; # Set the width to your desired value
            }
        </style>
        """, unsafe_allow_html=True)

    with st.sidebar:
        st.image("AmazonLogo2.svg", use_column_width=True)
        st.markdown('<hr>', unsafe_allow_html=True)
        st.subheader(':level_slider: Slicers:')
        color_theme_list = ['blues', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
        selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
        if st.button('logout'):
            st.session_state['authentication_status'] = False
            st.session_state['logged_out'] = True
            st.session_state['session_ends'] = False
            st.experimental_rerun()
            
        
    selected = option_menu(
        menu_title=None,
        options=["Dashboard page", "Sentiment page"], 
        icons=["graph-up", "emoji-smile"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal")
    
    if selected=="Dashboard page":
        dashboard.app()
    else:
        sentiment.app()


        
""" 
    modal = Modal("Warning", key="demo-modal",padding=60,max_width=500)
    
    
    with modal.container():
        
        
        st.write('You have been 5 mins without activity, login again please...')
        col1, col2, col3 = st.columns([1, 4, 1.2])
        with col3:
            if st.button("Logout",key="logout-modal"):
                # Add logout logic here
                pass
        
"""






import streamlit as st
from dashboard import slicers

def app():
    filter={}
    with st.sidebar:
        container3 = st.container(border=True,height=70)
        with container3:
            col = st.columns([3.5, 3], gap="medium")
            with col[0]:
                st.image("AmazonLogo2.svg", width=90)
            with col[1]:
                if st.button('logout',key="logout-original"):
                    st.session_state['authentication_status'] = False
                    st.session_state['logged_out'] = True
                    st.session_state['session_ends'] = False
                    st.rerun()
    
        st.markdown('<hr style="margin-top: 5px; margin-bottom: 7px">', unsafe_allow_html=True)
        st.subheader(':level_slider: Slicers:')
        filter=slicers()

    st.title('Sentiment')
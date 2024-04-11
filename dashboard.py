import streamlit as st
import extra_streamlit_components as stx
import session5


def app():
    
    chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id="tab1", title="Overview",description=''),
    stx.TabBarItemData(id="tab2", title="Performance",description=''),
    stx.TabBarItemData(id="tab3", title="Sales Prediction",description='') ], default="tab1")
    st.markdown('<hr style="margin-top: -10px;">', unsafe_allow_html=True)

    if chosen_id == "tab1":
        st.write("dihgf")
    elif chosen_id == "tab2":
        st.write("lkjhgfx")
    else:
        st.write("hgfx")
        


    with st.sidebar:
        st.image("AmazonLogo2.svg", use_column_width=True)
        col1, col2, col3 = st.columns([2.2, 4, 2])
        with col2:
            if st.button('logout',key="logout-original"):
                st.session_state['authentication_status'] = False
                st.session_state['logged_out'] = True
                st.session_state['session_ends'] = False
                st.rerun()
        st.markdown('<hr style="margin-top: -10px;">', unsafe_allow_html=True)
        st.subheader(':level_slider: Slicers:')
        color_theme_list = ['blues', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
        selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
        
        

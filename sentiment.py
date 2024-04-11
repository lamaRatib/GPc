import streamlit as st

def app():
    with st.sidebar:
        st.image("AmazonLogo2.svg", use_column_width=True)
        st.markdown('<hr>', unsafe_allow_html=True)
        st.subheader(':level_slider: Slicers:')
    st.title('Home')

    st.write('This is the `home page` of this multi-page app.')

    st.write('In this app, we will be building a simple classification model using the Iris dataset.')
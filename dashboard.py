import streamlit as st
import extra_streamlit_components as stx
import overviewSubpage, performanceSubpage, predictionSubpage, sidbar


def app():

    # Tabs for Subpages:
    chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id="tab1", title="🌐 Overview",description=''),
    stx.TabBarItemData(id="tab2", title="💸 Performance",description=''),
    stx.TabBarItemData(id="tab3", title="📆 Sales Prediction",description='') ], default="tab1")
    st.markdown('<hr style="margin-top: -25px; margin-bottom: 0px;">', unsafe_allow_html=True)
    
    filter={}

    # Each tab has its own code:
    # Tab1: Overview:
    if chosen_id == "tab1":
        # Sidebar code which contains (sidebar func, slicers func):
        with st.sidebar:
            sidebar_top=sidbar.visuals().sidebar_top()
            filter=sidbar.visuals().slicers()
        # Visuals calling func:
        overviewSubpage.overview(filter)
    
    # Tab2: Performance:
    elif chosen_id == "tab2":
        # Sidebar code which contains (sidebar func, slicers func):
        with st.sidebar:
            sidebar_top=sidbar.visuals().sidebar_top()
            filter=sidbar.visuals().slicers()

        # Visuals calling func:
        performanceSubpage.performance(filter)


    # Tab3: Sales Prediction:
    else:
        predictionSubpage.predict()
        
        


    
        
    
 
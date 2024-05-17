import streamlit as st
import extra_streamlit_components as stx
import plotly.express as px
import plotly.graph_objects as go
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
    # Tab1: Overview: ///////////////////////////////////////////////////////////////////////////////////////////////////
    if chosen_id == "tab1":
        # Sidebar code which contains (sidebar func, slicers func):
        with st.sidebar:
            sidebar_top=sidbar.visuals().sidebar_top()
            filter=sidbar.visuals().slicers()
        # Visuals calling func:
        re = overviewSubpage.overview(filter)

        col1, col2, col3, col4 = st.columns([2.8,3.1,2.6,2.1])
        st.markdown(""" <style> div[data-testid="stMetric"] { margin-top: -25px; } </style> """, unsafe_allow_html=True)

        # Card1: Total Sales
        if re['card1'] != None:
            formatted_sales = f"${re['card1'] / 1000:.1f}K" if re['card1'] >= 1000 else re['card1']
            formatted_sales = f"${re['card1'] / 1000000:.1f}M" if re['card1'] >= 1000000 else formatted_sales
        elif re['card1'] > 0:
            formatted_pro=f"${re['card1']}"
        else:
            formatted_sales="$0"
        col1.metric(value=str(formatted_sales), label="Total Sales")

        # Card2: Number of Products Sold
        if re['card2'] != None:
            formatted_pro = f"{re['card2'] / 1000:.1f}K" if re['card2'] >= 1000 else re['card2']
            formatted_pro = f"{re['card2'] / 1000000:.1f}M" if re['card2'] >= 1000000 else formatted_pro
        else:
            formatted_pro="0"
        col2.metric(value=str(formatted_pro), label="Number of Products Sold")

        # Card3: Average Rating
        if re['card3'] is None:
            re['card3']=0
        else:
            re['card3']=round(re['card3'], 2)
        col3.metric(value= str(re['card3']), label="Average Rating")

        # Card4: Number of Customers with applying related filter if exist:
        col4.metric(value=int(re['card4']), label="Number of Customers")

        col=st.columns(2)

        # Visual1:
        with col[0]:
            fig= px.pie(re['visual_2'], names='Category', values='Count of Sales', title='# of Sales per Category',height=400,color_discrete_sequence=["LightGray", "Silver", "DimGray", "LightSlateGray","DarkSlateGray","Black"])
            fig.layout.xaxis.fixedrange = True
            fig.layout.yaxis.fixedrange = True
            config = {'displayModeBar': False,'dragMode':False}
            st.plotly_chart(fig,config=config,use_container_width=True)

        # Visual2:
        with col[1]:
            fig= px.bar(re['result_df_top10'],x='City',y='Avg Rating',title='Top 10 AVG Rating by City',height=350,color_discrete_sequence=[ "LightSlateGray"])
            fig.layout.xaxis.fixedrange = True
            fig.layout.yaxis.fixedrange = True 
            config = {'displayModeBar': False,'dragMode':False}
            st.plotly_chart(fig,config=config,use_container_width=True)

        # Filter notification:
        par = {}
        par['date'] = re['date']
        par['category'] = re['category']
        par['subcategory'] = re['subcategory']
        par['productid'] = re['productid']
        par['city'] = re['city']
        par['rating'] = re['rating']

        sidbar.visuals().toastNotificate(par,filter)


    # Tab2: Performance: /////////////////////////////////////////////////////////////////////////////////////////////////
    elif chosen_id == "tab2":
        # Sidebar code which contains (sidebar func, slicers func):
        with st.sidebar:
            sidebar_top=sidbar.visuals().sidebar_top()
            filter=sidbar.visuals().slicers()

        # calling func:
        re = performanceSubpage.performance(filter)

        # Visual 1:
        fig= px.line(re['visual_1'],x='Date',y='Total Sales',title='Total Sales Over Time',height=260,color_discrete_sequence=[ "LightSlateGray"])
        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True 
        fig.update_layout(margin=dict(t=20))
        config = {'displayModeBar': False,'dragMode':False}
        st.plotly_chart(fig,config=config,use_container_width=True)

        col=st.columns([4,1.5], gap="large")

        # Visual 2:
        with col[0]:
            fig_boxplot = px.box(re['visual_2'], y='Price', height=250,title='Box Plot of Prices',color_discrete_sequence=[ "LightSlateGray"])
            fig_boxplot.layout.xaxis.fixedrange = True
            fig_boxplot.layout.yaxis.fixedrange = True 
            fig_boxplot.update_layout(margin=dict(t=20))
            config = {'displayModeBar': False,'dragMode':False}
            st.plotly_chart(fig_boxplot,config=config,use_container_width=True)

        # Visual 3:
        with col[1]:
            g = go.Figure(go.Indicator(domain = {'x': [0, 1], 'y': [0, 1]}, value = re['Total_sales'], mode = "gauge+number+delta",
                title = {'text': "Target VS Total Sales"}, delta = {'reference': re['Target']}, gauge = {'axis': {'range': [None, re['Target']]}}))
            g.layout.xaxis.fixedrange = True
            g.layout.yaxis.fixedrange = True 
            g.update_layout( height=260, width=400, margin=dict(t=40))
            config = {'displayModeBar': False,'dragMode':False}
            st.plotly_chart(g,config=config,use_container_width=True)



    # Tab3: Sales Prediction: /////////////////////////////////////////////////////////////////////////////////////////////
    else:
        predictionSubpage.predict()
    

        


    
        
    
 
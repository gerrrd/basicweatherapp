# basicweatherapp streamlit file

from basicweatherapp.utils import get_data, search_city
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title='Quick Weather Check',
    page_icon=':sun:',
    layout ='wide',
    initial_sidebar_state='auto')

# AI-rtsie API URL
st.sidebar.markdown('''# Quick Weather Check''')

st.sidebar.markdown(
    '''using the Metaweather API'''
)
hist_days = st.sidebar.slider(label="History of meteorological data for ... days.",
                               min_value=1,
                               max_value=50,
                               step=1,
                               value=14)

pred_days = st.sidebar.slider(label="Prediction for ... days.",
                               min_value=1,
                               max_value=5,
                               step=1,
                               value=3)


text = st.sidebar.text_input('Please, enter a city or place:')

if st.sidebar.button('Submit'):
    # make a request to OUR api
    city_data, df = get_data(text, past = hist_days, pred = pred_days)
    
    if city_data == -1:
        st.markdown('''I could not find it...''')
    else:
        st.markdown(f"## Meteorlogical data of {city_data['title']} ({city_data['location_type']})")
        st.markdown(city_data['latt_long'])
        
        
        # show the graphs

        #split the data into observations and predictions
        today = date.today()
        df1 = df[pd.to_datetime(df['applicable_date']) <= pd.to_datetime(today)]
        df2 = df[pd.to_datetime(df['applicable_date']) >= pd.to_datetime(today)]
        
        # the title will be
        title = f"{city_data['title']} ({city_data['location_type']}), temperature"
        
        # the observations are represented with darker colours
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df1.applicable_date, y=df1.min_temp, 
                                 name = 'Min', line = {'color':'blue'},legendgroup=0))
        fig.add_trace(go.Scatter(x=df1.applicable_date, y=df1.max_temp, 
                                 fill='tonexty', name = 'Max', line = {'color':'red'}, 
                                 fillcolor='khaki',legendgroup=0))
        fig.add_trace(go.Scatter(x=df1.applicable_date, y=df1.the_temp, 
                                 name = 'Temp', line = {'color':'black'},legendgroup=0))

        # the predictions are represented with lighter colours
        fig.add_trace(go.Scatter(x=df2.applicable_date, y=df2.min_temp, 
                                 name = 'Min (pred)', line = {'color':'lightblue'},legendgroup=1))
        fig.add_trace(go.Scatter(x=df2.applicable_date, y=df2.max_temp, name = 'Max (pred)', 
                                 fill='tonexty', line = {'color':'lightsalmon'}, 
                                 fillcolor='whitesmoke',legendgroup=1))
        fig.add_trace(go.Scatter(x=df2.applicable_date, y=df2.the_temp, 
                                 name = 'Temp (pred)', line = {'color':'gray'},legendgroup=1))

        # show the title, centered
        fig.update_layout(title_text=title, title_x=0.5)
        st.plotly_chart(fig)
        
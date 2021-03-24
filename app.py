# basicweatherapp streamlit file

from basicweatherapp.utils import get_data, search_city
import plotly.graph_objects as go
import plotly.express as px
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
                               max_value=31,
                               step=1,
                               value=14)

pred_days = st.sidebar.slider(label="Prediction for ... days. (Predictions are available for maximum 5-10 days from now on.)",
                               min_value=1,
                               max_value=10,
                               step=1,
                               value=3)

st.sidebar.markdown("Include...")
include_wind = st.sidebar.checkbox('wind information')
include_air = st.sidebar.checkbox('air pressure')
include_humidity = st.sidebar.checkbox('humidity')
include_temp_vs_humidity = st.sidebar.checkbox('temperature vs humidity')
include_temp_humidity_air = st.sidebar.checkbox('temperature vs humidity vs air pressure')

text = st.sidebar.text_input('Please, enter a city and press Submit.')

if st.sidebar.button('Submit'):
    # make a request to OUR api
    city_data, df = get_data(text, past = hist_days, pred = pred_days)
    
    if city_data == -1:
        st.markdown('''I could not find it...''')
    else:
        today = date.today()
        act_weather = df[pd.to_datetime(df['applicable_date']) == pd.to_datetime(today)]['weather_state_abbr'].iloc[0]
        st.markdown(f"## ![Alt Text](https://www.metaweather.com/static/img/weather/png/64/{act_weather}.png) Meteorlogical data of {city_data['title']} ({city_data['location_type']}) ")
        st.markdown(f"Latitude and Longitude coordinates: {city_data['latt_long']}")
        
        if include_wind:
            wind_dict={'N':   5,  'S':  6,  'E':   8, 'W':7,
                       'WNW': 12, 'NW': 12, 'NNW': 12,
                       'WSW': 11, 'SW': 11, 'SSW': 11,
                       'SSE': 10, 'SE': 10, 'ESE': 10,
                       'NNE': 9,  'NE': 9,  'ENE': 9}
            df['winddir']=200+df['wind_direction_compass'].map(wind_dict)

        # show the graphs

        #split the data into observations and predictions
        df1 = df[pd.to_datetime(df['applicable_date']) <= pd.to_datetime(today)]
        df2 = df[pd.to_datetime(df['applicable_date']) >= pd.to_datetime(today)]
        
        # the title will be
        title = f"{city_data['title']} ({city_data['location_type']}), temperature"
        if include_wind:
            title = title + " and wind (direction and speed)"
        
        # the observations are represented with darker colours
        fig = go.Figure()
        
        # min line observation part
        fig.add_trace(go.Scatter(x=df1.applicable_date, y=df1.min_temp, 
                                 name = 'Min', line = {'color':'blue'},legendgroup=0))
        
        # max line observation part
        fig.add_trace(go.Scatter(x=df1.applicable_date, y=df1.max_temp, 
                                 fill='tonexty', name = 'Max', line = {'color':'red'}, 
                                 fillcolor='khaki',legendgroup=0))

        # actual temperature. if include_wind, then we include the 
        # markers showing the direction and speed of the wind.
        if include_wind:
            fig.add_trace(go.Scatter(x=df1.applicable_date, y=df1.the_temp, 
                                     marker_symbol=df1.winddir,
                                     marker_size=df1.wind_speed*3.5,
                                     name = 'Temp', 
                                     line = {'color':'black'},legendgroup=0))
        else:
            fig.add_trace(go.Scatter(x=df1.applicable_date, y=df1.the_temp, 
                                     name = 'Temp', line = {'color':'black'},legendgroup=0))

        # the predictions are represented with lighter colours
        
        # minimum prediction line
        fig.add_trace(go.Scatter(x=df2.applicable_date, y=df2.min_temp, 
                                 name = 'Min (pred)', line = {'color':'lightblue'},legendgroup=1))
        
        # maximums prediction line
        fig.add_trace(go.Scatter(x=df2.applicable_date, y=df2.max_temp, name = 'Max (pred)', 
                                 fill='tonexty', line = {'color':'lightsalmon'}, 
                                 fillcolor='whitesmoke',legendgroup=1))
        
        # exact temperature prediction
        # if include_wind, then we include the
        # markers showing the direction and speed of the wind.
        if include_wind:
            fig.add_trace(go.Scatter(x=df2.applicable_date, y=df2.the_temp,
                                     marker_symbol=df2.winddir,
                                     marker_size=df2.wind_speed*3.5,
                                     name = 'Temp (pred)', line = {'color':'gray'},legendgroup=1))        
        else:
            fig.add_trace(go.Scatter(x=df2.applicable_date, y=df2.the_temp, 
                                     name = 'Temp (pred)', line = {'color':'gray'},legendgroup=1))

        # show the title, centered
        fig.update_layout(title_text=title, title_x=0.5)
        fig.update_yaxes(title_text='Temperature (C)')
        fig.update_xaxes(title_text='Date')
        

        st.plotly_chart(fig)
 
        # air pressure
        if include_air:
            title = f"{city_data['title']} ({city_data['location_type']}), air pressure"

            df3 = df[pd.to_datetime(df['applicable_date']) > pd.to_datetime(today)]
            fig2 = go.Figure()

            fig2.add_trace(go.Bar(y=df1.air_pressure,x=df1.applicable_date,
                                  name="Air pressure", marker={'color': 'blueviolet'}))
            fig2.add_trace(go.Bar(y=df3.air_pressure,x=df3.applicable_date,
                                  name="Air pressure (pred)", marker={'color': 'lightsteelblue'}))
            fig2.update_layout(title_text=title,
                               title_x=0.5,
                               yaxis_range=[int(min(df.air_pressure)-3),int(max(df.air_pressure)+3)])

            fig2.update_yaxes(title_text="Bar")
            fig2.update_xaxes(title_text='Date')
            st.plotly_chart(fig2)
 
        # air humidity
        if include_humidity:
            title = f"{city_data['title']} ({city_data['location_type']}), humidity"

            fig3 = go.Figure()

            fig3.add_trace(go.Scatter(y=df1.humidity,x=df1.applicable_date,
                                  name="Humidity", marker={'color': 'blueviolet'}, line_shape='spline'))
            fig3.add_trace(go.Scatter(y=df2.humidity,x=df2.applicable_date,
                                  name="Humidity (pred)", marker={'color': 'lightsteelblue'}, line_shape='spline'))
            fig3.update_layout(title_text=title,
                               title_x=0.5,
                               yaxis_range=[int(min(df.humidity)-5),int(max(df.humidity)+5)])

            fig3.update_yaxes(title_text="%")
            fig3.update_xaxes(title_text='Date')
            st.plotly_chart(fig3)

        
        # temperature vs humidity 
        if include_temp_vs_humidity:
            title = f"{city_data['title']} ({city_data['location_type']}), temperature vs humidity"

            fig4 = go.Figure()

            fig4.add_trace(go.Scatter(y=df1.humidity,x=df1.the_temp,
                                  name="Observation", marker={'color': 'blueviolet'},
                                   mode='markers'))
            fig4.add_trace(go.Scatter(y=df3.humidity,x=df3.the_temp,
                                  name="Prediction", marker={'color': 'lightsteelblue'},
                                     mode='markers'))
            fig4.update_layout(title_text=title,
                               title_x=0.5,
                               yaxis_range=[int(min(df.humidity)-5),int(max(df.humidity)+5)],
                               xaxis_range=[int(min(df.the_temp)-3),int(max(df.the_temp)+3)]
                              )

            fig4.update_yaxes(title_text="Humidity")
            fig4.update_xaxes(title_text='Temperature')
            st.plotly_chart(fig4)

        # Temperature - Air pressure - Humidity
        if include_temp_humidity_air:
            title = f"{city_data['title']} ({city_data['location_type']}), temperature vs air pressure vs humidity"
            df['color'] = [1 if x <= today else 0 for x in pd.to_datetime(df.applicable_date)]
            fig5 = px.scatter_3d(df, x='the_temp', y='air_pressure', z='humidity', color = 'color', opacity=0.7)
            # tight layout
            fig5.update_layout(title_text=title, margin=dict(l=0, r=0, b=0, t=0), showlegend = False)
            st.plotly_chart(fig5)

    



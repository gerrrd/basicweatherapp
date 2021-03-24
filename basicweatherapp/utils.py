import requests
import pandas as pd
from datetime import date, timedelta

def search_city(query):
    '''
    a method to look for the "where on earth ID" (woeid) of the given city
    using metaweather API
    '''
    url = "https://www.metaweather.com/api/location/search/?query="+query
    response = requests.get(url).json()
    
    # if there is no data, return None
    if not response:
        return None
    return response[0]

def daily_forecast(woeid, year, month, day):
    '''
    it returns the last measurement/prediction of the given woeid and date
    '''
    # query format" woerd/year/month/day:
    query = f'{woeid}/{year}/{month}/{day}'
    # request to the weather API  
    response = requests.get("https://www.metaweather.com/api/location/"+query).json()
    # we use only the latest measurements and the lates forecast for the upcoming days
    
    if not response:
        return None
    
    return response[0]

def forecasts(woeid, dates):
    '''
    it fetches and returns the measurements/forecast for the given woeid and dates
    '''
    fc = []
    for d in dates:
        fc.append(daily_forecast(woeid, d.year, d.month, d.day))
    return fc

def get_data(city = 'Berlin', past = 14, pred = 4):
    '''
    it returns a pandas DataFrame object with the necessary measurements/forecasts
    of the given city in a time range of 14 before and 3 days after "today"
    '''
    city_data = search_city(city)
    if city_data == None:
        return -1, -1

    woeid = city_data['woeid']
    
    today = date.today()
    dates = [today+timedelta(t) for t in range(-past,pred+1)]
    data = forecasts(woeid, dates)
    
    return city_data, pd.DataFrame(data).drop(columns=['id','created', 'visibility', 'predictability'])
    
    
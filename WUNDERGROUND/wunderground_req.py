#!/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import requests
import bs4
import os
import schedule
import uuid


def job():
    meteo_list = []
    
    webpage = "https://www.wunderground.com/weather/us/ny/new-york-city"
    response = requests.get(webpage)
    doc = bs4.BeautifulSoup(response.text)
    
    seed = uuid.uuid4()
    temperatura=doc.select("div.current-temp > display-unit > span > span.wu-value")[0].text
    temp_max=doc.select("span.hi")[0].text.encode('utf-8')
    temp_max_ok=temp_max.replace('°','')

    temp_min=doc.select("span.lo")[0].text.encode('utf-8')
    temp_min_ok=temp_min.replace('°','')
    
    tempo=doc.select("div.condition-icon > p")[0].text

    time=doc.select("p> span > strong")[0].text

    meteo_list.append({'_id': seed, 'date': time, 'temperature': temperatura, 'temp_max': temp_max_ok, 'temp_min': temp_min_ok, 
                         'weather': tempo})

    ds_meteo = pd.DataFrame(meteo_list)
    ds_meteo.head()
    
    
    if os.path.isfile('/wunderground/wunderground_scrap.csv'):
            ds_meteo.to_csv("/wunderground/wunderground_scrap.csv", sep=";", mode='a', header=False)
    else:
            ds_meteo.to_csv("/wunderground/wunderground_scrap.csv", sep=";", mode='a')

job()
#schedule.every(5).minutes.do(job)

#if __name__ == '__main__':
#    while True:
#        schedule.run_pending()


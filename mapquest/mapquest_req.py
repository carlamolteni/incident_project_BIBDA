import requests
import json
import pandas as pd
import os
import schedule

URL = "https://www.mapquestapi.com/traffic/v2/incidents?&outFormat=json&boundingBox=40.81069108268215%2C-73.77662658691406%2C40.61551614707256%2C-74.23805236816406&filters=incidents&key=T4eqDjtnpzWsfeMBZgKAqKobvcICurpU"

def job():
    dettagli = []
    response = requests.get(URL)
    geo = json.loads(response.text)
    incidents = geo['incidents']
    # print(len(incidents))
    if len(incidents) > 0:
        for incident in incidents:
            new_incident = {
              "id": incident['id'],
              "type": incident['type'],
              "severity": incident['severity'],
              "eventCode": incident['eventCode'],
              "lat": incident['lat'],
              "lng": incident['lng'],
              "startTime": incident['startTime'],
              "endTime": incident['endTime'],
              "impacting": incident['impacting'],
              "shortDesc": incident['shortDesc'],
              "fullDesc": incident['fullDesc'],
              "delayFromFreeFlow": incident['delayFromFreeFlow'],
              "delayFromTypical": incident['delayFromTypical'],
              "distance": incident['distance'],
              "iconURL": incident['iconURL'],
              "parameterizedDescription": incident['parameterizedDescription']
            }
            dettagli.append(new_incident)
            #print(dettagli)
        ds_dettagli = pd.DataFrame(dettagli)
        ds_dettagli.set_index("id")

        if os.path.isfile('./mapquest_traffic.csv'):
            ds_dettagli.to_csv("./mapquest_traffic.csv", sep=";", mode='a', header=False)
        else:
            ds_dettagli.to_csv("./mapquest_traffic.csv", sep=";", mode='a')

schedule.every(5).minutes.do(job)

if __name__ == '__main__':
    while True:
        schedule.run_pending()


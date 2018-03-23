# -*- coding: utf-8 -*-

"""Main module."""
import requests
import json
import csv
import pandas
import mysql.connector
from pprint import pprint
from datetime import datetime



#Use json.load to read in the Dublin.json file
#Dublin.json contains static information about all the bike stations

staticData = json.load(open('Dublin.json'))
apiKey = "066552409dad0809af4e338d67817a8d931d697d"
dubUrl = "https://api.jcdecaux.com/vls/v1/stations/30?contract=Dublin&apiKey=066552409dad0809af4e338d67817a8d931d697d"

        
def query_API(stationNumber):
    r = requests.get('https://api.jcdecaux.com/vls/v1/stations/' + str(stationNumber) + '?contract=Dublin&apiKey=' + apiKey)
    r = r.json() 
    return r

def stations_list(fileName):
    data = json.load(open(fileName))
    stations = []
    for i in data:
        stations.append(i["number"])
        stations.sort()
    return stations

def timestamp_to_ISO(timestamp):
    moment = datetime.fromtimestamp(timestamp / 1000)
    return moment.time().isoformat()

def information():
    stations = stations_list('Dublin.json')
    
    #Save information for all stations in a csv
    #-------------------------------------------
    with open('info.csv', 'w') as csvfile:
        fieldnames = ['number', 'name', 'latitude', 'longitude', 'bikes', 'stands']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader() 

        for i in stations:
            g = query_API(i) 
            station_info = {'number': g["number"], 
                    'name': g["name"], 
                    'latitude': g["position"]["lat"], 
                    'longitude': g["position"]["lng"], 
                    'bikes': g["available_bikes"], 
                    'stands': g["available_bike_stands"]}
            writer.writerow(station_info)
    #-------------------------------------------
    
    
    #Send the information to the database
    g = query_API(30) 
    station_info = {'number': g["number"], 
                    'name': g["name"], 
                    'latitude': g["position"]["lat"], 
                    'longitude': g["position"]["lng"], 
                    'bikes': g["available_bikes"], 
                    'stands': g["available_bike_stands"]}
        
    
    
class Database:
    host="something.com"
    port=3306
    dbname="DublinBikesStationInfo"
    user="your_username"
    password="your_password"

    def __init__(self):
        cnx = mysql.connector.connect(user=user, password = password, 
                                      host = host, database=dbname)
        self.connection = cnx
        self.cursor = cnx.cursor()
        
    def add_station_info(self, statInfo):
        add_info = ("INSERT INTO stations"
               "(number, name, latitude, longitude, bikes_available, stands_available) "
               "VALUES (%(number)s, %(name)s, %(latitude)s, %(longitude), %(bikes)s, %(stands)s")
        self.cursor.execute(add_info, statInfo)
    
    def close_db(self):
        cnx.commit()
        cursor.close()
        cnx.close()
      
      
print(stations_list('Dublin.json'))
print(query_API(55))
information()
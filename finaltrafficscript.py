import numpy as np
import matplotlib
import pandas as pd
import random
from bs4 import BeautifulSoup
import urllib
import datetime as datetime

#Open page and parse UTML
page = urllib.request.urlopen('http://www.massdot.state.ma.us/highway/TrafficTravelResources/TrafficInformationMap/RealTimeTraffic.aspx').read()
soup = BeautifulSoup(page, "lxml")
#Find desired table
table = soup.find('table', attrs ={'class':'xmlView'})
#grab all table bodies (3 in total)
tbodies = table.find_all('tbody')

#get routes separately, since we only need to get the routes once
#Initilize list of routes
routes = []

for tbody in tbodies:
    #for each tbody, find all rows in the body
    rows = tbody.find_all('tr')
    for row in rows:
        entries = row.find_all('td')                
        if len(entries) == 3:
        #Excludes rows that just consist of "Rt. #"
            if entries[0].string is not None:
                #The first tag gives description of road location
                road = entries[0].string
                routes.append(road)

#Initilize list of traffic speed and travel time
speed = []
travel = []

def grab_data(speed_ls, travel_ls):
    for tbody in tbodies:
        #for each tbody, find all rows in the body
        rows = tbody.find_all('tr')

        for row in rows:
            entries = row.find_all('td')
            if len(entries) == 3:
            #Excludes rows that just consist of "Rt. #"
                if entries[1].string is not None:
                     #The second tag gives description of travel time
                    time = entries[1].string
                    travel_ls.append(time)  
                else:
                    #adds NA for blank travel times
                    travel_ls.append("NA")
                if entries[2].string is not None:
                    #The third tag gives description of traffic speed
                    s = entries[2].string
                    speed_ls.append(s)
grab_data(speed, travel)

d = {"Routes":routes,
     "Travel Time at "+ datetime.datetime.now().strftime("%d-%m-%y %H:%M"): travel,
     "Speed at " + datetime.datetime.now().strftime("%d-%m-%y %H:%M"): speed}
df = pd.DataFrame(data=d)

def scrape():
    #Open page and parse UTML
    page = urllib.request.urlopen('http://www.massdot.state.ma.us/highway/TrafficTravelResources/TrafficInformationMap/RealTimeTraffic.aspx').read()
    soup = BeautifulSoup(page, "lxml")
    #Find desired table
    table = soup.find('table', attrs ={'class':'xmlView'})
    #grab all table bodies (3 in total)
    tbodies = table.find_all('tbody')
    
    speed = []
    travel = []
    grab_data(speed, travel)
    
    d = {"Travel Time at "+datetime.datetime.now().strftime("%d-%m-%y %H:%M"): travel,
     "Speed at " + datetime.datetime.now().strftime("%d-%m-%y %H:%M"): speed}
    scraped_df = pd.DataFrame(data=d)
    return scraped_df


initial_hr = int(datetime.datetime.now().strftime("%H"))
#picks out hour part of the datetime element
initial_day = int(datetime.datetime.now().strftime("%d"))
#saves start date

end_day = 7
#run for 7 days
days_passed = 0
#tracks days passed
time_not_expired = True

hr = initial_hr

while time_not_expired:
    current_hr = int(datetime.datetime.now().strftime("%H"))
    current_day = int(datetime.datetime.now().strftime("%d"))
    #picks out minute part of the datetime element
    if hr != current_hr:
        #scrape when an hour has passed
        new_df = scrape()
        print (datetime.datetime.now().strftime("%d-%m-%y %H:%M"))
        df = df.join(new_df)
    hr = current_hr
    if current_day == (initial_day + 1):
        df.to_csv("traffic for June"+ str(initial_day) +".csv", encoding='utf-8')
        #write df as a csv for each day
        days_passed += 1
        initial_day = current_day
        #update days passed
    time_not_expired =  (days_passed != end_day)

    
print('done')
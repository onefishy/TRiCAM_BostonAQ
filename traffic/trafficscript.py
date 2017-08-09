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

'''grab_data

grab_data will process the html table given by this URL:
It will convert the HTML table for travel times and speed at the current moment into two separate lists for speed and travel time.

input parameters: 

speed_ls: empty list that will store strings describing current speed

travel_ls: empty list that will store strings describing travel times

output parameters: No return value, will append to existing lists
'''

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
                    
now = datetime.datetime.now().strftime("%d-%m-%y %H")
grab_data(speed, travel)

d = {"Routes":routes,
     "Travel Time at "+ now: travel,
     "Speed at " + now: speed}
df = pd.DataFrame(data=d)

'''Function Name: 

Description of what function does:

input parameters:

output parameters:
'''

def scrape(date):
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
    
    d = {"Travel Time at "+ date: travel,
     "Speed at " + date: speed}
    scraped_df = pd.DataFrame(data=d)
    return scraped_df

days_passed = 0
end_day = 3
time_not_expired = True
i = 0

initial = int(datetime.datetime.now().strftime("%M"))
initial_day = int(datetime.datetime.now().strftime("%M"))
prev_min = initial

#picks out minute part of the datetime element
while time_not_expired:
    current = int(datetime.datetime.now().strftime("%M"))
    current_day = int(datetime.datetime.now().strftime("%M"))
    #picks out minute part of the datetime element
    if prev_min != current:
        #scrape when a minute has passed
        print (datetime.datetime.now().strftime("%d-%m-%y %H:") + str(current))
        new_df = scrape(datetime.datetime.now().strftime("%d-%m-%y %H:") + str(current))
        df = df.join(new_df)
        prev_min = current
    if current_day == (initial_day + 2):
        df.to_csv("traffic on "+ str(initial_day) + ".csv", encoding='utf-8')
        days_passed += 1
        initial_day = current_day
    time_not_expired = (days_passed != end_day)
print('done')
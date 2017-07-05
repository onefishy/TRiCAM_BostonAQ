import requests
import xmltodict
import datetime
import time
import json


'''This block of code is an intermediary block that accesses the "Routes" page from the MBTA API, using the specific API key
that is hard-coded in. The resulting XML file is read, processed, and parsed so that the focus is on the Bus routes and
the bus routes only. By the time this cell is finished executing, routeidnums will contain a list of all bus routes as strings,
which will be used later to access each individual bus on the MBTA API.


Variables:
api_key: (string) contains the API key provided by MBTA, held as  a string
routespage: XML file that contains the content read using requests.get
routesdoc: (Ordered Dictionary) contains the routespage XML file as a parsed, Ordered Dictionary
allroutes: (list) a list of ordered dictionary that contains all routes, regardless of transportation type
busroutes: (Ordered Dictionary) an odered dict that contains information about all the bus routes
busrouteslist: (list) a list of ordered dicts, in which each entry is an individual route
routeidnums: (list) a list of all the bus route ID numbers, as strings. Each entry is a bus route ID number, that we will use
                later and iterate through to access all buses with our API
'''


api_key = "LiKpmuCun0uvMJUXBNAp2Q"

#Read the page that contains the list of all bus route ID numbers
routespage = requests.get("http://realtime.mbta.com/developer/api/v2/routes?api_key=" + api_key + "&format=xml")

#Looking for our lines to be read. Parses XML document and turns into a dictionary
routesdoc = xmltodict.parse(routespage.content)

#A list of ordered dictionaries that contains all the routes, regardless of type (Subway, Bus, ferry etc)
allroutes = routesdoc['route_list']['mode']

busroutes = allroutes[3]
#This is a list of ordered dictionaries. Each entry is an ordered dictionary that is an individual route
busrouteslist = list(busroutes['route'])

#This list will hold id numbers as strings for each bus route
routeidnums = []
for x in range(0, len(busrouteslist)):
    routeidnums.append(busrouteslist[x]['@route_id'])
#end of loop
# routeidnums now is a list of all the bus route id numbers, each one as a string


'''
Method
get_route_data(str route_id): 
    - takes a string parameter route_id which is a Bus Route ID number
    - calls the "Vehicles By Route" real-time data accessor of the MBTA API, using route_id to properly complete the call
    - this XML file is stored in var page
    - parses page.content and converts to an ordered dictionary
    - ordered dictionary is stored in routedata var
    - returns routedata (Ordered Dict)
'''

def get_route_data(route_id):
    page = requests.get('http://realtime.mbta.com/developer/api/v2/vehiclesbyroute?api_key=LiKpmuCun0uvMJUXBNAp2Q&route='+ route_id + '&format=xml')
    routedata = xmltodict.parse(page.content)
    return routedata

'''This cell contains the script that will scrape real-time bus location data for all MBTA buses, once every 15 minutes,
for an entire day. This cell contains a series of nested "for" loops that are delayed in time by the time.sleep() method,
which explicitly tells the loop to execute once every 60*15 seconds, or 15 minutes. It then opens a file and writes the data
from the entire day (the daydata dictionary) to its own unique file.

Variables:
data: (dict) dictionary which contains information about all MBTA buses at a single instance in time. Is reset every quarter.
qtrdata: (dict) dictionary which contains information about quarter-hours of a given hour. Is reset evey hour. Key: quarter-hour
hourdata: (dict) dictionary which contains information about hours of a given day. Key: hour
daydata: (dict) dictionary which contains information about a single day. Key: day number

'''

#Small Scale Test

data = {}
qtrdata = {}
hourdata = {}
daydata = {}

for day in range(2):
    
    for hour in range(2):
        
        for qtr in range(4):
            
            for y in range(5):    
                data[routeidnums[y]] = get_route_data(routeidnums[y])
            
            qtrdata["Qtr " + str(qtr)] = data
            print("quarter " + time.strftime("%H:%M:%S"))
            data = {}
            time.sleep(15)
        
        hourdata["Hour " + str(hour)] = qtrdata
        print("hour " + time.strftime("%H"))
        qtrdata = {}
        
    daydata["Day " + str(day)] = hourdata
    print("day " + time.strftime("%m-%d-%y"))
    hourdata = {}

    
    f = open("/home/ubuntu/" + time.strftime("%m-%d-%H-%M_") + 'TEST_output_file.json', 'w')
    json.dump(daydata, f,sort_keys = True, indent = 4, separators = (',', ': ') )
    f.close()
    print("Day added")
    
    daydata = {}

print("done")
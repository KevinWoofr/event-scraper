import sys
import json
import requests
import codecs
import os.path

from datetime import datetime
from dateutil import parser

APP_ID = "1759548447703049"
APP_SECRET = "38762800fe27a48cf3464838ea9b60ba"
GRAPH_URL = "https://graph.facebook.com/"
VERSION = "v2.8/"
EVENT_LIMIT = 25

TEMP_ACCESS_TOKEN = "EAAZAATMwwwAkBAP3vbvWNfUCVcnxaF1ZBFbBwlZB0hGSKmrPV7aKQxAt3nKk9lBJR2qk7ZBCWa6dtmfZADwmEU165A8ns0tMZC9VO7K0lX6cMz7KjfDn34eT0KYhzLaqaSX0kbo9KztLwCysxZAbvIcIUcKYyDZBhqEZD" #2 months

PAGE_ID = "19268387803" #Attica

query = GRAPH_URL + VERSION + PAGE_ID + "/?fields=fan_count,name,events.limit(" + str(EVENT_LIMIT) + "){id,name,start_time,end_time,is_canceled,attending},albums{name,id,photos.limit(2000){source}}&access_token=" + TEMP_ACCESS_TOKEN

#Go to https://developers.facebook.com/docs/graph-api/reference/page/ for list of fields
request = requests.get(query)
data = json.loads(request.text)

#save_path = "C:/Users/Kevin-Notebook/Desktop"
#complete_name = os.path.join(save_path, "nameoffilehere.txt")

events = data['events']
events = events['data']
albums = data['albums']
albums = albums['data']
#print(events)

for event in events:
    if event['is_canceled']:
        continue
    
    print("Event: " + event['name'])
    print("Event ID: " + event['id'])
    startTime = datetime.strptime(event['start_time'], "%Y-%m-%dT%H:%M:%S+0800") #%z for timezone doesnt work
    endTime = datetime.strptime(event['end_time'], "%Y-%m-%dT%H:%M:%S+0800")
    print("From " + str(startTime) + " to " + str(endTime))

    if 'attending' in event:
        attendees = event['attending']
        attendees = attendees['data']

        for attendee in attendees:
            print("Name: " + attendee['name'])
            print("FB ID: " + attendee['id'])
print("Number of events: {}".format(len(events)))

for album in albums:
    if album['name'] == "Untitled Album":
        continue
    
    print("Album name: " + album['name'])
    print("Album ID: " + album['id'])

    photos = album['photos']
    photos = photos['data']
    
    for photo in photos:
        print("Photo source: " + photo['source'])
        print("Photo ID: " + photo['id'])
    print("Number of photos: {}".format(len(photos)))
    
print("Number of albums: {}".format(len(albums)))

#file.close()

def getAttendeeLists(eventLimit):
    query = GRAPH_URL + VERSION + PAGE_ID + "/?fields=fan_count,name,events.limit(" + str(eventLimit) + "){id,name,is_canceled,attending}&access_token=" + TEMP_ACCESS_TOKEN

    request = requests.get(query)
    data = json.loads(request.text)

    events = data['events']
    events = events['data']
    eventDict = dict()

    for event in events:
        if event['is_canceled']:
            continue

        ev = (event['name'], event['id'])

        attendeeList = []
        if 'attending' in event:
            attendees = event['attending']
            attendees = attendees['data']

            for attendee in attendees:
                user = {'attendee_name': attendee['name'], 'attendee_id': attendee['id']}
                attendeeList.append(user)

        eventDict[ev] = attendeeList

    return eventDict
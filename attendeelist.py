import sys
import json
import requests
import codecs
import os.path

APP_ID = "1759548447703049"
APP_SECRET = "38762800fe27a48cf3464838ea9b60ba"
GRAPH_URL = "https://graph.facebook.com/"
VERSION = "v2.8/"
EVENT_LIMIT = 25

TEMP_ACCESS_TOKEN = "EAAZAATMwwwAkBAP3vbvWNfUCVcnxaF1ZBFbBwlZB0hGSKmrPV7aKQxAt3nKk9lBJR2qk7ZBCWa6dtmfZADwmEU165A8ns0tMZC9VO7K0lX6cMz7KjfDn34eT0KYhzLaqaSX0kbo9KztLwCysxZAbvIcIUcKYyDZBhqEZD" #2 months

PAGE_ID = "19268387803" #Attica

def getUrlFromId( id ):
    return "http://facebook.com/profile.php?id=" + id

def getAttendeeLists( eventLimit ):
    query = GRAPH_URL + VERSION + PAGE_ID + "/?fields=fan_count,name,events.limit(" + str(EVENT_LIMIT) + "){id,name,is_canceled,attending}&access_token=" + TEMP_ACCESS_TOKEN

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
                user = {'attendee_name': attendee['name'], 'attendee_url': getUrlFromId(attendee['id'])}
                attendeeList.append(user)

        eventDict[ev] = attendeeList

    return eventDict

print(getAttendeeLists(EVENT_LIMIT))
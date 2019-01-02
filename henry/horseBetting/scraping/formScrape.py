from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import re



def raceScrape(link):

    # link suffix will be /trackname-date(yyyymmdd)/name-of-race(eg. canadian-club-qtis-two-years-old-maiden-race-1 <--- from initial scrape)
    apiPrefixRace = 'https://api.racenet.com.au/api/v2/horse/formguide/field/'

    page = urlopen(apiPrefixRace + link)
    soup = BeautifulSoup(page, 'html.parser')
    jsonSoup = json.loads(soup.text.strip())['data'][0]

    #todo Find out what other data is useful other than what is below

    returnData = {}

    returnData['distance'] = jsonSoup['distance']
    returnData['entryConditions'] = jsonSoup['entryConditions']
    returnData['hasResult'] = jsonSoup['hasResult']
    returnData['stageId1'] = jsonSoup['stageId']
    returnData['stageId2'] = jsonSoup['meeting']['stageId']
    returnData['meetingDate'] = jsonSoup['meeting']['meetingDate']
    returnData['trackCondition'] = jsonSoup['meeting']['trackCondition']
    returnData['prizeMoney'] = jsonSoup['prizes']
    returnData['runners'] = jsonSoup['runners']
    returnData['startTimeLocal'] = jsonSoup['startTimeLocal']
    returnData['startTimeUtc'] = jsonSoup['startTimeUtc']
    returnData['antiClockwise'] = jsonSoup['track']['antiClockwise']

    return returnData


def horseHistory(horseId, meetingDate, stageId, long = False):

    # link suffix will be /horseID?meetingDate=yyyy-mm-dd&stage=stageID  <--- horseID, yyyy-mm-dd & stageId will be pulled from above api
    apiPrefixHorse = 'https://api.racenet.com.au/api/v1/horse/formguide/form/horse/'

    if long:
        page = urlopen(apiPrefixHorse + '/' + str(horseId) + '?meetingDate=' + meetingDate + '&stage=' + str(stageId))
    else:
        page = urlopen(apiPrefixHorse + '/' + str(horseId) + '?meetingDate=' + meetingDate + '&numberOfRun=all&stage=' + str(stageId))
    soup = BeautifulSoup(page, 'html.parser')
    jsonSoup = json.loads(soup.text.strip())['data']

    #todo Find out what other data is useful other than what is below

    returnData = jsonSoup

    # returns an array, 0 being the most recent race the horse has run
    # ['raceUniqueIdentifier'] provides a link to the race in question (from which we can get class/location/ratings/comments etc)
    # ['venue'], ['venueCategory'] -> provincial/country/metro,
    # ['videoComment'] full comment, ['railPosition'] comment on the horses start
    # ['or1-']prefix = other racer details
    # ['positionId'] horses place, ['starters'] no of horses that ran
    # ['apprentice'] jockey - bool, ['barrierNumber'], ['day'], ['distance'], ]['daysBetweenRuns']
    # ['jockeyId'], ['jockeyName'], ['jockeyUniqueIdentifier']

    ##Also much more, can be broken down as needed

    return returnData

def formatDateWithDashes(longDate):
    return longDate[0:10]

def formatDateNoDashes(longDate):
    shortDate = longDate[0:10]
    return re.sub('-', '', shortDate)
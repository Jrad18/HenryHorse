from urllib.request import urlopen
from bs4 import BeautifulSoup

#Scrapes data from all available future meetings and their races.

#define meeting and race class
class Race:
    def __init__(self, num, detail, length, time, link):
        self.num = num
        self.detail = detail
        self.length = length
        self.time = time
        self.link = link

    def printRace(self):
        print(self.num + ': ' + self.detail + '\n' + self.length + '\ntime: ' + self.time + '\n' + self.link + '\n')

class Meeting:
    def __init__(self, track, races):
        self.track = track
        self.races = races

    def printMeeting(self):
        print(self.track + ': \n')
        for x in range(0, len(self.races)):
            self.races[x].printRace()

#extract HTML from form guide page listing all meetings and races
quote_page = 'https://www.racenet.com.au/racing-form-guide'
page = urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')

#Todays meeting
today = soup.find('div', attrs={'class':'rn-js-race-meetings-day', 'id':'meetinglist_tab_1'})

#Pull details for each race
#trackTitles = today.find_all('h3', attrs={'class':'table-race-meetings-track-title'})

meetingsList = today.find('tbody').find_all('tr')


meetings = []
meetingRaces = []


for x in range(0, len(meetingsList)):
    title = meetingsList[x].find('h3', attrs={'class':'table-race-meetings-track-title'})
    raceNumberList = meetingsList[x].find_all('span', attrs={'class':'table-race-meeting-detail-order'})
    raceDetailList = meetingsList[x].find_all('span', attrs={'class':'table-race-meeting-detail-label-race-name-mobile'})
    raceLengthList = meetingsList[x].find_all('span', attrs={'class':'table-race-meeting-detail-label-race-distance'})
    raceTimeList = meetingsList[x].find_all('span', attrs={'class':'table-race-meeting-detail-info-wrapper'})

    raceLinks = meetingsList[x].find_all('td', attrs={'class': 'table-race-meeting-detail'})
    raceLink = []

    for i in range(0, len(raceLinks)):
        raceLink.append('https://www.racenet.com.au' + raceLinks[i].find('a')['href'])


    races = []
    for y in range(0, len(raceNumberList)):
        race = Race(raceNumberList[y].text.strip(), raceDetailList[y].text.strip(), raceLengthList[y].text.strip(), raceTimeList[y].text.strip(), raceLink[y])
        races.append(race)
    meetings.append(Meeting(title.text.strip(), races))

meetings[0].printMeeting()

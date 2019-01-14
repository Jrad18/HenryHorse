from raceClass import horseEval
from meetingScrape import scrapeMeeting
from formScrape import raceScrape

day = input('What days race meets would you like to view \nToday [1], Tomorrow [2] etc. max [5]\n >>')

meetings = scrapeMeeting(day)

for x in range(0, len(meetings)):
    print('[' + str(x) + ']')
    meetings[x].printMeetingTitle()

meeting = int(input('Which meeting would you like to view\n >>'))

meetings[meeting].printMeeting()

race = input('Which race number would you like to analyse\n >>')
analysedRace = meetings[meeting].races[int(race)-1]

raceData = raceScrape(analysedRace)

horses = []

for x in range(0, len(raceData['runners'])):
    horseId = raceData['runners'][x]['horse']['id']
    horses.append(horseEval(horseId, analysedRace, x))

#print race data
for x in range(0, len(horses)):
    horses[x].printHorse()

#Generate market based only on ratings
sumRatings = 0
for x in range(0, len(horses)):
    sumRatings+= horses[x].currentRating

market = {}
#print('Calculated Market: ')
for x in range(0, len(horses)):
    market[horses[x].horse['name']] = sumRatings/horses[x].currentRating
    print(horses[x].horse['name'] + '\t: ' + str(100/market[horses[x].horse['name']]))
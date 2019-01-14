from formScrape import raceScrape
from formScrape import horseHistory
from formScrape import formatDateWithDashes
from meetingScrape import scrapeMeeting
import datetime


class ClassData:
    def __init__(self, cl, weight, region, dow, track, prize, starters, distance, pHol = False, mpc = None, age = None, sex = None, place = None, rtg = None, daysBetweenRuns = None, comment = None, pastRace = False, isTrial = False):
        self.cl = cl                    #cl = class; As in, Maiden, BM84, class 1 etc.
        self.weight = weight            #HCP or SW
        self.age = age                  #age restriction (3YO +)
        self.sex = sex                  #eg. fillies and mares
        self.distance = distance
        self.region = region            #short code state (eg. VIC/SA)
        self.mpc = mpc                  #metro/prov/country
        self.dow = dow                  #Monday = 0, Sunday = 6
        self.pHol = pHol                #bool
        self.track = track              #track name
        self.prize = prize              #total prize pool, no bonuses
        self.place = place              #where horse placed in race (None if pastRace = False)
        self.starters = starters        #number of starters in race
        self.rtg = rtg                  #rating of horse for the evaluated race (None if pastRace = False)
        self.daysBetweenRuns = daysBetweenRuns
        self.comment = comment          #comment of horses performance in evaluated race
        self.pastRace = pastRace        #bool, true: evaluating horses performance, false: race for which a horses performance is being estimated
        self.isTrial = isTrial          #barrier trial has different data points

    def printRating(self):
        place = 0
        starters = 0
        age = 'age **'
        sex = 'sex **'
        cl = 'class **'
        weight = 'weight **'
        if self.place:
           place = self.place
        if self.starters:
            starters = self.starters
        if self.age:
            age = self.age
        if self.sex:
            sex = self.sex
        if self.cl:
            cl = self.cl
        if self.weight:
            weight = self.weight
        if self.isTrial:
            print(' -- TRIAL -- ')
        print(str(place) + ' of ' + str(starters) + ' in ' + str(self.distance) + 'm ' + str(age) + ' ' + sex + ' ' + cl + ' ' + str(weight))
        print('Track: ' + self.track + ' Region: ' + self.mpc + ' State: ' + self.region)

class HorseData:
    def __init__(self, currentRating, weight, currentRace, pastRaces, jockey, trainer, horse, scratched = False):
        self.currentRating = currentRating
        self.weight = weight
        self.currentRace = currentRace
        self.pastRaces = pastRaces
        self.jockey = jockey
        self.trainer = trainer
        self.horse = horse
        self.scratched = scratched

    def printHorse(self):
        print(self.horse['name'] + '    RTG: ' + str(self.currentRating) + '\n')
        if self.scratched:
            print(' -- SCRATCHED -- ')
        else:
            for x in range(0, len(self.pastRaces)):
                self.pastRaces[x].printRating()
                print('\n')


def evalRace(race):
    #take data from a race and pull class-relevant data into a class object (class the racing term, not the programming term)

    raceData = raceScrape(race)

    cl = raceData['classRestrict']
    weight = raceData['weightRestrict']
    if raceData['ageRestrict'] == '':
        age = None
    else:
        age = raceData['ageRestrict']
    if raceData['sexRestrict'] == '':
        sex = None
    else:
        sex = raceData['sexRestrict']
    region = raceData['trackRegion']
    track = raceData['trackName']
    date = datetime.datetime(int(raceData['meetingDate'][0:4]), int(raceData['meetingDate'][6:7]), int(raceData['meetingDate'][9:10]))
    dow = date.weekday()
    prize = raceData['prizeMoney']['prizeMoneyTotalNoBonus']
    starters = len(raceData['runners'])
    scratches = 0
    for x in range(0, starters):
        if raceData['runners'][x]['scratched']:
            scratches += 1

    distance = raceData['distance']

    classData = ClassData(cl, weight, region, dow, track, prize, starters, distance, age, sex)
    return classData

def horseEval(horseId, race, runnerNo):
    raceData = raceScrape(race)
    currentRaceClassData = evalRace(race)
    runnerData = raceData['runners'][runnerNo]

    noRaces = 4
    hHistory = horseHistory(horseId, formatDateWithDashes(raceData['meetingDate']), raceData['stageId1'])

    if len(hHistory) < noRaces:
        hHistory = horseHistory(horseId, formatDateWithDashes(raceData['meetingDate']), raceData['stageId1'], True)
    if len(hHistory) < noRaces:
        noPastRacesChecked = len(hHistory)
    else:
        noPastRacesChecked = noRaces

    if runnerData['scratched']:
        scratched = True
    else:
        scratched = False

    if 'jockey' in runnerData:
        jockeyData = runnerData['jockey']
    else:
        jockeyData = None
    if 'trainer' in runnerData:
        trainerData = runnerData['trainer']
    else:
        trainerData = None
    horseData = runnerData['horse']

    initialRating = runnerData['handicapRating']
    initialWeight = runnerData['handicapWeight']
    trainingLocation = runnerData['trainingLocation']

    pastRaceData = []

    for x in range(0, noPastRacesChecked):
        pastRaceData.append(evalPastRace(hHistory[x], raceData['trackRegion']))

    evaluatedHorse = HorseData(initialRating, initialWeight, currentRaceClassData, pastRaceData, jockeyData, trainerData, horseData, scratched)
    return evaluatedHorse

def evalPastRace(pastRace, region):

    pRace = True
    distance = pastRace['distance']
    mpc = pastRace['venueCategory']
    track = pastRace['venue']
    date = datetime.datetime(int(pastRace['meetingDate'][0:4]), int(pastRace['meetingDate'][5:7]), int(pastRace['meetingDate'][8:10]))
    dow = date.weekday()
    starters = pastRace['starters']
    place = pastRace['positionId']
    isTrial = pastRace['isBarrierTrial']
    region = region

    if not isTrial:
        age = pastRace['restrictionAgeShortCondition']
        cl = pastRace['restrictionClassMediumCondition']
        weight = pastRace['restrictionWeightLongCondition']
        sex = pastRace['restrictionSexLongCondition']
        daysBetweenRuns = pastRace['daysBetweenRuns']
        prize = pastRace['prizeMoney']
    else:
        age = None
        cl = None
        weight = None
        sex = None
        daysBetweenRuns = None
        prize = None

    comment = pastRace['videoComment']

    pHol = False        #This is to be determined later
    rating = pastRace['ratingHandicapPreRace']

    thisRace = ClassData(cl, weight, region, dow, track, prize, starters, distance, pHol, mpc, age, sex, place, rating, daysBetweenRuns, comment, pRace, isTrial)
    return thisRace


#cl, weight, region, dow, track, prize, starters, distance, pHol = False, mpc = None, age = None, sex = None,
# place = None, rtg = None, daysBetweenRuns = None, comment = None, pastRace = False


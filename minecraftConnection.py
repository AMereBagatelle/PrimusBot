import json
import os
from ftplib import FTP

whitelistIDs = []

def getPlayerData(outputFolder):
    #logging in to ftp
    ftp = FTP(host='na99.pebblehost.com')
    ftp.login(user='brennenputh@gmail.com.78133', passwd='Candace4551')
    #getting the whitelist
    with open('whitelist.json' , 'w') as fp:
        ftp.retrbinary('RETR whitelist.json', lambda data: fp.write(data.decode('UTF-8')))
    with open('whitelist.json', 'r') as fp:
        whitelistIDs = []
        data = json.load(fp)
        for point in data:
            whitelistIDs.append(point['uuid'] + '.json')
    ftp.cwd('/world/stats')
    #getting all files for playerstats
    for filename in ftp.nlst():
        if filename in whitelistIDs:
            with open(outputFolder + '/' + filename, 'w') as newFile:
                ftp.retrbinary('RETR ' + filename, lambda data: newFile.write(data.decode('UTF-8')))
    ftp.quit()

def getStatScoreboard(statsFolder, statToGet):
    filenames = []
    unsortedResults = []
    for file in os.listdir(statsFolder):
        if file.endswith('.json'):
            filenames.append(file)
    with open('whitelist.json') as whitelistFile:
        whitelistFileLoaded = json.load(whitelistFile)
        for filename in filenames:
            with open(statsFolder + '/' + filename) as currentFile:
                currentFileLoaded = json.load(currentFile)
                if 'stat.' + statToGet in currentFileLoaded:
                    currentUUID = filename.replace('.json', '')
                    currentScore = currentFileLoaded['stat.' + statToGet]
                    for player in whitelistFileLoaded:
                        if currentUUID in player['uuid']:
                            currentName = player['name']
                    unsortedResults.append([currentName, currentScore])
    for result in unsortedResults:
        if len(result) != 2:
            #TODO: make this a message that sends back
            print('Invalid!')
    sortedResults = sorted(unsortedResults, key=lambda x: x[1], reverse=True)
    print(sortedResults)
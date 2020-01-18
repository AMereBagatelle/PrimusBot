import json
import os
import discord
import re
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

def getStatScoreboard(statsFolder, statToGet, getAll):
    aliases = [
        ['pickup.', 'stat.pickup.minecraft.'], 
        ['drop.', 'stat.drop.minecraft.'], 
        ['use.', 'stat.useItem.minecraft.'], 
        ['mine.', 'stat.mineBlock.minecraft.'], 
        ['craft.', 'stat.craftItem.minecraft.'], 
        ['kill.', 'stat.killEntity.minecraft.']
        ]
    formattedStat = statToGet
    #getting the actual stat
    if re.search('(?:pickup|drop|use|mine|craft|kill)\.(?:minecraft\.)?\S+', statToGet):
        for alias in aliases:
            if alias[0] in formattedStat[0:8]:
                formattedStat = formattedStat.replace(alias[0], alias[1])
    #just use normal stat. approach for single worded things
    #embed handling
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
                if formattedStat in currentFileLoaded:
                    currentUUID = filename.replace('.json', '')
                    currentScore = currentFileLoaded[formattedStat]
                    for player in whitelistFileLoaded:
                        if currentUUID in player['uuid']:
                            currentName = player['name']
                    unsortedResults.append([currentName, currentScore])
    for result in unsortedResults:
        if len(result) != 2:
            #TODO: make this a message that sends back
            return discord.Embed(title='Invalid!', type='rich', description='No idea why this broke... try in a few minutes')
    sortedResults = sorted(unsortedResults, key=lambda x: x[1], reverse=True)
    if len(sortedResults) > 10 and getAll != 'all':
        sortedResults = sortedResults[0:10]
    if len(sortedResults) <= 0:
        return discord.Embed(title='Invalid!', type='rich', description='Not a stat, or nobody\'s done it')
    finalResult = ''
    for result in sortedResults:
        finalResult = finalResult + '**' + result[0] + '**: ' + str(result[1]) + '\n\n'
    return discord.Embed(title='Scoreboard for ' + statToGet, type='rich', description=finalResult)
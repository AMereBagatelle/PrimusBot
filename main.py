import discord
from discord.ext import commands
from discord.ext import tasks
import os
import re
import json
from mcrcon import MCRcon
from ftplib import FTP

import credentials

bot = commands.Bot(command_prefix='/')

# Stuff that you might want to customize for your own bot
CHAT_LINK_CHANNEL = 677582149230002176
POLL_OUTPUT_CHANNEL = 660845995080286208

PLAYER_DATA_FOLDER = 'mcPlayerData'

DIG_GOOD_LIST = ['dig good', 'Dig good', ':dig: good']
DUPE_BAD_LIST = ['doop bad', 'Doop bad', 'Dupe bad', 'dupe bad', ':doop: bad']

# Stuff that should stay constant
DISCORD_LETTERS = [
            "\N{REGIONAL INDICATOR SYMBOL LETTER A}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER B}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER C}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER D}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER E}", 
            "\N{REGIONAL INDICATOR SYMBOL LETTER F}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER G}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER H}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER I}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER J}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER K}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER L}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER M}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER N}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER O}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER P}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Q}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER R}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER S}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER T}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER U}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER V}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER W}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER X}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Y}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Z}"
        ]

WHITELIST_FILE = 'whitelist.json'
DEFENSE_MESSAGE = True

# Things that can't be done in regular bot.command
@bot.event
async def on_message(message):
    global DEFENSE_MESSAGE

    if message.author.name == 'PrimusBot':
        return

    for item in DIG_GOOD_LIST:
        if item in message.content:
            digMessage = await message.channel.send('Yes, but doop easier', delete_after=100)
    
    for item in DUPE_BAD_LIST:
        if item in message.content:
            dupeMessage = await message.channel.send('no', delete_after=100)
    
    if 'whalecum' in message.content or 'Whalecum' in message.content and DEFENSE_MESSAGE:
        DEFENSE_MESSAGE = await message.channel.send('Anti-whalecum activated.', delete_after=5)
        await message.delete(delay=4)

    for user in message.mentions:
        if user.name == 'RR':
            ping = await message.channel.send('You shouldn\'t have pinged RR... you are in for it now. (unless you had a valid reason ofc)', delete_message=5)
    
    if message.channel == bot.get_channel(CHAT_LINK_CHANNEL) and not message.content.startswith('/'):
        sendRconCommand('/say [ChatLink] <' + message.author.name + '> ' + message.content)
    
    await bot.process_commands(message)

# Sets status
@bot.event
async def on_ready():
    activity = discord.Activity(name='people, places, things', type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)

#starts a task to get the data for the scoreboards from server
@tasks.loop(hours=1)
async def get_mc_playerdata():
    print('Getting Data')
    getPlayerData(PLAYER_DATA_FOLDER)
    print('Data Sucessfully Retrieved')

# runs the channel for mc chat link
@tasks.loop(seconds=10)
async def mcChatLoop():
    if readLatestLogLine():
        #finds which channel to send results to
        sendChannel = bot.get_channel(CHAT_LINK_CHANNEL)
        with open('mcLogData/latest.log', 'r') as fp:
            data = fp.readlines()
            for line in data:
                if re.match(r"\[\d\d:\d\d:\d\d\] \[Server thread\/INFO\]: <\S+>(.+)\n", line):
                    await sendChannel.send(line[33:])

# Public Commands
@bot.command()
async def online(ctx):
    """Gets players currently online on the SMP."""
    players = sendRconCommand('/list')
    players = 'Currently online players: ' + players[31:]
    await ctx.send(players)

@bot.command()
async def list(ctx):
    """Gets players currently online on the SMP."""
    players = sendRconCommand('/list')
    players = 'Currently online players: ' + players[31:]
    await ctx.send(players)

#scoreboard-getting command
@bot.command()
async def s(ctx, arg, *arg2):
    """Shows scoreboard for stats.  Add "all" for all results.  Check pins in #primus-bot-stuff for valid stat shortcuts."""
    await ctx.send(embed=getStatScoreboard(PLAYER_DATA_FOLDER, arg, ''.join(arg2)))

@bot.command()
async def stoplazy(ctx):
    """Tell someone to stop lazy."""
    await ctx.send(file=discord.File('stop_lazy.png'))
    await ctx.message.delete()

# Member Commands
#starts poll
@bot.command()
@commands.has_role('Member')
async def poll(ctx, arg, *arg2):
    """Member Only.  Create a poll in the current channel."""
    #sends poll message
    pollMessage = await ctx.send('**' + arg + '**', embed=newPoll(arg2))
    #deletes command message
    await ctx.message.delete(delay=None)
    #tests if PollMessage failed, and if so deletes the poll message itself
    if pollMessage.embeds[0].title == 'Failed':
        await pollMessage.delete(delay=10)
    else:
        #adds reactions
        i = 0
        for choice in arg2:
            await pollMessage.add_reaction(DISCORD_LETTERS[i])
            i += 1
    
#resolves poll result and posts output in separate channel
@bot.command()
@commands.has_role('Member')
async def resolvepoll(ctx, arg):
    """Member only.  Resolves a poll in the current channel, by the name of the argument."""
    #gets poll message from arg
    pollToResolve = await ctx.channel.history().get(content='**' + arg + '**')
    #gets our messages to send from pollManager
    pollTitle, pollEmbed, pollResult = getPollResult(ctx, pollToResolve)
    sendChannel = bot.get_channel(POLL_OUTPUT_CHANNEL)
    #sends poll results out in selected channel
    await sendChannel.send(pollTitle, embed=pollEmbed)
    await sendChannel.send(pollResult)
    
    #deletes poll and command message
    await pollToResolve.delete(delay=None)
    await ctx.message.delete(delay=None)

@bot.command()
@commands.has_role('Member')
async def clear(ctx, arg):
    """Member Only. Clears argument number of messages."""
    await ctx.message.delete()
    toDelete = ctx.channel.history(limit=int(arg))
    async for m in toDelete:
        await m.delete(delay=None)
    confirmDelete = await ctx.send('Deleted {0} message(s).'.format(arg))
    await confirmDelete.delete(delay=3)

# Owner Commands
@bot.command()
@commands.has_role('Owner')
async def stop(ctx):
    """Owner Only.  Stops the bot."""
    await ctx.send('Stopping')
    await bot.logout()

@bot.command()
@commands.has_role('Owner')
async def togglewhaledefense(ctx):
    """Owner Only.  Toggles whalecum defense."""
    DEFENSE_MESSAGE = not DEFENSE_MESSAGE
    await ctx.send('Toggled, now is ' + str(DEFENSE_MESSAGE))

@bot.command()
@commands.has_role('Owner')
async def sendcommand(ctx, arg):
    """Owner only.  Can send commands to the SMP."""
    commandOutput = sendRconCommand(arg)
    if commandOutput != "":
        await ctx.send('Server: ' + commandOutput)
    else:
        fail_message = await ctx.send("Command returns nothing.", delete_after=5)

@bot.command()
@commands.has_role('Owner')
async def getmcdata():
    """Owner only.  Forces getting data for the /s scoreboards."""
    print('Getting Data')
    getPlayerData(PLAYER_DATA_FOLDER)
    print('Data Sucessfully Retrieved')

# Other functions, generally just stuff for minecraft communication.
def sendRconCommand(command):
    with MCRcon(credentials.RCON_IP, credentials.RCON_PASSWORD, port=credentials.RCON_PORT) as mcr:
        output = mcr.command(command)
        return output

# THESE VARIABLES SHOULD ONLY BE CALLED IN READLATESTLOGLINE
continuousLogLen = 0
firstTime = True
        
def readLatestLogLine():
    global continuousLogLen
    global firstTime
    fileChanged = False
    checkLogLen = continuousLogLen
    currentLogLen = os.path.getsize('mcLogData/latest.log')
    ftp = FTP(host=credentials.FTP_HOST)
    ftp.login(user=credentials.FTP_USER, passwd=credentials.FTP_PASS)
    ftp.cwd('logs')
    ftp.sendcmd('TYPE i')
    ftpFileLen = int(ftp.size('latest.log'))
    if (continuousLogLen < ftpFileLen):
        with open('mcLogData/latest.log', 'w+') as fp:
            try:
                ftp.retrbinary('RETR latest.log', lambda data: fp.write(data.decode('UTF-8')), rest=continuousLogLen)
                fileChanged = True
                continuousLogLen += ftpFileLen - continuousLogLen
            except:
                print('Was not able to get files, time is: ' + datetime.now().strftime(r"%d/%m/%Y %H:%M:%S"))
    ftp.close()
    if not fileChanged or firstTime:
        firstTime = False
        return False
    else:
        return True

def getPlayerData(outputFolder):
    #logging in to ftp
    ftp = FTP(host=credentials.FTP_HOST)
    ftp.login(user=credentials.FTP_USER, passwd=credentials.FTP_PASS)
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
        ['kill.', 'stat.killEntity.'],
        ['break.', 'stat.breakItem.minecraft.']
    ]
    formattedStat = statToGet
    #getting the actual stat
    if re.search('(?:pickup|drop|use|mine|craft|kill|break)\.(?:minecraft\.)?\S+', statToGet):
        for alias in aliases:
            if alias[0] in formattedStat[0:8]:
                formattedStat = formattedStat.replace(alias[0], alias[1])
    #just use normal stat.minecraft. approach for single worded things
    #embed handling
    filenames = []
    unsortedResults = []
    for file in os.listdir(statsFolder):
        if file.endswith('.json'):
            filenames.append(file)
    with open('whitelist.json') as WHITELIST_FILE:
        WHITELIST_FILELoaded = json.load(WHITELIST_FILE)
        for filename in filenames:
            with open(statsFolder + '/' + filename) as currentFile:
                currentFileLoaded = json.load(currentFile)
                if formattedStat in currentFileLoaded:
                    currentUUID = filename.replace('.json', '')
                    currentScore = currentFileLoaded[formattedStat]
                    for player in WHITELIST_FILELoaded:
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
    iterator = 1
    for result in sortedResults:
        finalResult = finalResult + '**' + str(iterator) + ': ' + result[0] + '**: ' + str(result[1]) + '\n\n'
        iterator += 1
    return discord.Embed(title='Scoreboard for ' + statToGet, type='rich', description=finalResult)

def newPoll(pollOptions):
    pollResult = ''
    pollFinal = ''

    # These two checks are to make sure that we don't get a invalid poll request, because that would just be no fun
    if len(pollOptions) > len(DISCORD_LETTERS):
        return discord.Embed(title='Failed', type='rich', description='Less than 26 options, please.')

    if len(pollOptions) < 2:
        return discord.Embed(title='Failed', type='rich', description='Make more options!')

    # Assigns pollResult to the definition of the poll, which is the emoji + the option + a newline
    i = 0
    for p in pollOptions:
        p = DISCORD_LETTERS[i] + ' ' + p + '\n'
        pollResult = pollResult + p
        i = i + 1

    # The finished embed object
    return discord.Embed(title='', type='rich', description=pollResult)

def getPollResult(ctx, pollToResolve):
    #getting poll contents for later
    pollTitle = pollToResolve.content
    pollEmbed = pollToResolve.embeds[0]
    pollReactions = pollToResolve.reactions
    #gets poll result
    pollReactionNumbers = []
    possibleResolution = True
    for reaction in pollReactions:
        pollReactionNumbers.append(reaction.count)
    pollReactionNumberSet = set()
    for number in pollReactionNumbers:
        if number in pollReactionNumberSet and number == max(pollReactionNumberSet):
            possibleResolution = False
        else:
            pollReactionNumberSet.add(number)  
    if possibleResolution:
        pollResultIndex = pollReactionNumbers.index(max(pollReactionNumbers))
        pollResult = str(pollReactions[pollResultIndex].emoji)
    else:
        pollResult = 'No decision, it was a tie.'
    #returns results of all things determined in here
    return pollTitle, pollEmbed, pollResult

get_mc_playerdata.start()
mcChatLoop.start()
bot.run(credentials.BOT_TOKEN)
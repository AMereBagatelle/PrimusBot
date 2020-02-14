import discord
import os
import re
from discord.ext import commands
from discord.ext import tasks

import Constants
import fileManager
import pollManager
import minecraftStats
import mcRcon

bot = commands.Bot(command_prefix='/')

CHAT_LINK_CHANNEL = 677582149230002176

@bot.event
async def on_message(message):
    if message.author.name == 'PrimusBot':
        return

    for item in Constants.DIG_GOOD_LIST:
        if item in message.content:
            digMessage = await message.channel.send('Yes, but doop easier')
            await digMessage.delete(Delay=100)
    
    for item in Constants.DUPE_BAD_LIST:
        if item in message.content:
            dupeMessage = await message.channel.send('no')
            await dupeMessage.delete(Delay=100)
    
    if Constants.DEFENSE_MESSAGE:
        if 'whalecum' in message.content or 'Whalecum' in message.content:
            DEFENSE_MESSAGE = await message.channel.send('Anti-whalecum activated.')
            await DEFENSE_MESSAGE.delete(delay=5)
            await message.delete(delay=4)

    for user in message.mentions:
        if user.name == 'RR':
            ping = await message.channel.send('You shouldn\'t have pinged RR... you are in for it now. (unless you had a valid reason ofc)')
            await ping.delete(delay=5)
    
    if message.channel == bot.get_channel(CHAT_LINK_CHANNEL):
        mcRcon.sendRconCommand('/say [ChatLink] <' + message.author.name + '> ' + message.content)
    
    await bot.process_commands(message)

@bot.event
async def on_ready():
    activity = discord.Activity(name='people, places, things', type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)
    logCurrentLen = 0

#starts a task to get the data for the scoreboards from server
@tasks.loop(hours=1)
async def get_mc_playerdata():
    print('Getting Data')
    minecraftStats.getPlayerData(Constants.PLAYER_DATA_FOLDER)
    print('Data Sucessfully Retrieved')

@tasks.loop(seconds=5)
async def mcChatLoop():
    print('running')
    if mcRcon.readLatestLogLine():
        #finds which channel to send results to
        sendChannel = bot.get_channel(CHAT_LINK_CHANNEL)
        with open('mcLogData/latest.log', 'r') as fp:
            data = fp.readlines()
            for line in data:
                if re.match(r"\[\d\d:\d\d:\d\d\] \[Server thread\/INFO\]: <\S+>(.+)\n", line):
                    await sendChannel.send(line[33:])

@bot.command()
async def rconTest(ctx, arg):
    mcRcon.sendRconCommand(arg)

@bot.command()
@commands.has_role('Admin')
async def getmcdata():
    print('Getting Data')
    minecraftStats.getPlayerData(Constants.PLAYER_DATA_FOLDER)
    print('Data Sucessfully Retrieved')

#scoreboard-getting command
@bot.command()
async def s(ctx, arg, *arg2):
    await ctx.send(embed=minecraftStats.getStatScoreboard(Constants.PLAYER_DATA_FOLDER, arg, ''.join(arg2)))

#starts poll
@bot.command()
@commands.has_role('Member')
async def poll(ctx, arg, *arg2):
    #sends poll message
    pollMessage = await ctx.send('**' + arg + '**', embed=pollManager.newPoll(arg2))
    #deletes command message
    await ctx.message.delete(delay=None)
    #tests if PollMessage failed, and if so deletes the poll message itself
    if pollMessage.embeds[0].title == 'Failed':
        await pollMessage.delete(delay=10)
    else:
        #adds reactions
        i = 0
        for choice in arg2:
            await pollMessage.add_reaction(Constants.DISCORD_LETTERS[i])
            i += 1
    
#resolves poll result and posts output in separate channel
@bot.command()
@commands.has_role('Member')
async def resolvepoll(ctx, arg):
    #gets poll message from arg
    pollToResolve = await ctx.channel.history().get(content='**' + arg + '**')
    #gets our messages to send from pollManager
    sendChannel, pollTitle, pollEmbed, pollResult = pollManager.getPollResult(ctx, pollToResolve)
    #sends poll results out in selected channel
    await sendChannel.send(pollTitle, embed=pollEmbed)
    await sendChannel.send(pollResult)
    
    #deletes poll and command message
    await pollToResolve.delete(delay=None)
    await ctx.message.delete(delay=None)

@bot.command()
@commands.has_role('Member')
async def clear(ctx, arg):
    await ctx.message.delete()
    toDelete = ctx.channel.history(limit=int(arg))
    async for m in toDelete:
        await m.delete(delay=None)
    confirmDelete = await ctx.send('Deleted {0} message(s).'.format(arg))
    await confirmDelete.delete(delay=3)

#sets channel for mod messages
@bot.command()
@commands.has_role('Admin')
async def setmodchannel(ctx):
    fileManager.writeToLineOfFile(Constants.SETTINGS_FILE, 0, 'ModChannel: {0.channel.id}'.format(ctx.message))
    await ctx.send('Mod channel set.')

#sets channel for poll outputs
@bot.command()
@commands.has_role('Admin')
async def setpolloutputchannel(ctx):
    fileManager.writeToLineOfFile(Constants.SETTINGS_FILE, 1, 'PollChannel: {0.channel.id}'.format(ctx.message))
    await ctx.send('Poll output channel set.')

@bot.command()
async def listcommands(ctx):
    #TODO: Write wiki page on this and put link in send function
    await ctx.send('Commands:\n')

@bot.command()
@commands.has_role('Owner')
async def stop(ctx):
    await ctx.send('Stopping')
    await bot.logout()

@bot.command()
@commands.has_role('Admin')
async def togglewhaledefense(ctx):
    Constants.DEFENSE_MESSAGE = not Constants.DEFENSE_MESSAGE
    await ctx.send('Toggled, now is ' + str(Constants.DEFENSE_MESSAGE))

get_mc_playerdata.start()
mcChatLoop.start()
bot.run('NjU3OTIwNzg4MDk1MTcyNjA4.Xh3EpA.TlpE6BelKCZekqmeoFDlA_vWHqU')
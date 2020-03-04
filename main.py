import discord
import os
import re
from discord.ext import commands
from discord.ext import tasks

import constants
import pollManager
import minecraftStats
import mcRcon
import credentials

bot = commands.Bot(command_prefix='/')

CHAT_LINK_CHANNEL = 677582149230002176
POLL_OUTPUT_CHANNEL = 660845995080286208

# Things that can't be done in regular bot.command
@bot.event
async def on_message(message):
    if message.author.name == 'PrimusBot':
        return

    for item in constants.DIG_GOOD_LIST:
        if item in message.content:
            digMessage = await message.channel.send('Yes, but doop easier', delete_after=100)
    
    for item in constants.DUPE_BAD_LIST:
        if item in message.content:
            dupeMessage = await message.channel.send('no', delete_after=100)
    
    if 'whalecum' in message.content or 'Whalecum' in message.content and constants.DEFENSE_MESSAGE:
        DEFENSE_MESSAGE = await message.channel.send('Anti-whalecum activated.', delete_after=5)
        await message.delete(delay=4)

    for user in message.mentions:
        if user.name == 'RR':
            ping = await message.channel.send('You shouldn\'t have pinged RR... you are in for it now. (unless you had a valid reason ofc)', delete_message=5)
    
    if message.channel == bot.get_channel(CHAT_LINK_CHANNEL) and not message.content.startswith('/'):
        mcRcon.sendRconCommand('/say [ChatLink] <' + message.author.name + '> ' + message.content)
    
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
    minecraftStats.getPlayerData(constants.PLAYER_DATA_FOLDER)
    print('Data Sucessfully Retrieved')

# runs the channel for mc chat link
@tasks.loop(seconds=10)
async def mcChatLoop():
    if mcRcon.readLatestLogLine():
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
    players = mcRcon.sendRconCommand('/list')
    players = 'Currently online players: ' + players[31:]
    await ctx.send(players)

@bot.command()
async def list(ctx):
    """Gets players currently online on the SMP."""
    players = mcRcon.sendRconCommand('/list')
    players = 'Currently online players: ' + players[31:]
    await ctx.send(players)

#scoreboard-getting command
@bot.command()
async def s(ctx, arg, *arg2):
    """Shows scoreboard for stats.  Add "all" for all results.  Check pins in #primus-bot-stuff for valid stat shortcuts."""
    await ctx.send(embed=minecraftStats.getStatScoreboard(constants.PLAYER_DATA_FOLDER, arg, ''.join(arg2)))

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
            await pollMessage.add_reaction(constants.DISCORD_LETTERS[i])
            i += 1
    
#resolves poll result and posts output in separate channel
@bot.command()
@commands.has_role('Member')
async def resolvepoll(ctx, arg):
    """Member only.  Resolves a poll in the current channel, by the name of the argument."""
    #gets poll message from arg
    pollToResolve = await ctx.channel.history().get(content='**' + arg + '**')
    #gets our messages to send from pollManager
    pollTitle, pollEmbed, pollResult = pollManager.getPollResult(ctx, pollToResolve)
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
    constants.DEFENSE_MESSAGE = not constants.DEFENSE_MESSAGE
    await ctx.send('Toggled, now is ' + str(constants.DEFENSE_MESSAGE))

@bot.command()
@commands.has_role('Owner')
async def sendcommand(ctx, arg):
    """Owner only.  Can send commands to the SMP."""
    commandOutput = mcRcon.sendRconCommand(arg)
    if commandOutput != "":
        await ctx.send('Server: ' + commandOutput)
    else:
        fail_message = await ctx.send("Command returns nothing.", delete_after=5)

@bot.command()
@commands.has_role('Owner')
async def getmcdata():
    """Owner only.  Forces getting data for the /s scoreboards."""
    print('Getting Data')
    minecraftStats.getPlayerData(constants.PLAYER_DATA_FOLDER)
    print('Data Sucessfully Retrieved')

get_mc_playerdata.start()
mcChatLoop.start()
bot.run(credentials.BOT_TOKEN)
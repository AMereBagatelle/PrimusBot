from symbol import namedexpr_test

import discord
from discord.ext import commands

import Constants
import fileManager
import pollManager

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_message(message):
    if message.content == 'dig good':
        await message.channel.send('Yes, but dupe faster')
    if message.content == 'dupe bad':
        await message.channel.send('no')

    await bot.process_commands(message)

#starts poll
@bot.command()
async def poll(ctx, arg, *arg2):
    #sends poll message
    pollMessage = await ctx.send('**' + arg + '**', embed=pollManager.newPoll(arg, arg2))
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
async def resolvePoll(ctx, arg):
    #gets poll message from arg
    pollToResolve = await ctx.channel.history().get(content='**' + arg + '**')
    #gets our messages to send from pollManager
    sendChannel, pollTitle, pollEmbed, pollResult = pollManager.resolvePoll(ctx, pollToResolve)
    #sends poll results out in selected channel
    await sendChannel.send(pollTitle, embed=pollEmbed)
    await sendChannel.send(pollResult)
    
    #deletes poll and command message
    await pollToResolve.delete(delay=None)
    await ctx.message.delete(delay=None)

#sets channel for mod messages
@bot.command()
async def setModChannel(ctx):
    fileManager.writeToLineOfFile(Constants.settingsFile, 0, 'ModChannel: {0.channel}'.format(ctx.message))
    await ctx.send('Mod channel set.')

#sets channel for poll outputs
@bot.command()
async def setPollOutputChannel(ctx):
    fileManager.writeToLineOfFile(Constants.settingsFile, 1, 'PollChannel: {0.channel}'.format(ctx.message))
    await ctx.send('Poll output channel set.')

@bot.command()
async def commands(ctx):
    #TODO: Write wiki page on this and put link in send function
    await ctx.send('')

bot.run('NjU3OTIwNzg4MDk1MTcyNjA4.Xf6NxA.S4dKtW0GOlUEQO5gUsV5DCg5fyQ')
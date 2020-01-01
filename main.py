import discord
from discord.ext import commands

import Constants
import fileManager
import pollManager

bot = commands.Bot(command_prefix=':')

@bot.event
async def on_message(message):
    for item in Constants.digGoodList:
        if item in message.content:
            digMessage = await message.channel.send('Yes, but doop easier')
            await digMessage.delete(Delay=100)
    
    for item in Constants.dupeBadList:
        if item in message.content:
            dupeMessage = await message.channel.send('no')
            await dupeMessage.delete(Delay=100)

    await bot.process_commands(message)

#starts poll
@bot.command()
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
async def resolvePoll(ctx, arg):
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
async def clear(ctx, arg):
    await ctx.message.delete()
    toDelete = ctx.channel.history(limit=int(arg))
    async for m in toDelete:
        await m.delete(delay=None)
    confirmDelete = await ctx.send('Deleted {0} message(s).'.format(arg))
    await confirmDelete.delete(delay=3)

#sets channel for mod messages
@bot.command()
async def setModChannel(ctx):
    fileManager.writeToLineOfFile(Constants.settingsFile, 0, 'ModChannel: {0.channel.id}'.format(ctx.message))
    await ctx.send('Mod channel set.')

#sets channel for poll outputs
@bot.command()
async def setPollOutputChannel(ctx):
    fileManager.writeToLineOfFile(Constants.settingsFile, 1, 'PollChannel: {0.channel.id}'.format(ctx.message))
    await ctx.send('Poll output channel set.')

@bot.command()
async def commands(ctx):
    #TODO: Write wiki page on this and put link in send function
    await ctx.send('Commands:\n')

@bot.command()
async def stop(ctx):
    await ctx.send('Stopping')
    await bot.logout()

bot.run('NjU3OTIwNzg4MDk1MTcyNjA4.Xf6NxA.S4dKtW0GOlUEQO5gUsV5DCg5fyQ')
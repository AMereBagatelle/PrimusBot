from symbol import namedexpr_test

import discord
from discord.ext import commands

import Constants
import fileManager
import pollManager

settingsFile = 'settings.txt'
bot = commands.Bot(command_prefix='.')

#starts poll
@bot.command()
async def poll(ctx, arg, *arg2):
    #sends poll message
    pollMessage = await ctx.send(arg, embed=pollManager.newPoll(arg, arg2))
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
    
@bot.command()
async def resolvePoll(ctx, arg):
    #gets poll message from arg
    pollToResolve = await ctx.channel.history().get(content=arg)
    print(pollToResolve)
    #getting poll contents for later
    pollTitle = pollToResolve.content
    pollEmbed = pollToResolve.embeds[0]
    pollReactions = pollToResolve.reactions
    print(pollReactions)
    #deletes poll and command message
    await pollToResolve.delete(delay=None)
    await ctx.message.delete(delay=None)
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
    #finds which channel to send results to
    sendChannel = fileManager.readLineOfFile(settingsFile, 1)[13:]
    server = ctx.message.channel.guild
    for channel in server.channels:
        if channel.name == sendChannel:
            sendChannel = channel
    #sends poll results out in selected channel
    await sendChannel.send(pollTitle, embed=pollEmbed)
    await sendChannel.send(pollResult)

bot.run('NjU3OTIwNzg4MDk1MTcyNjA4.Xf6NxA.S4dKtW0GOlUEQO5gUsV5DCg5fyQ')
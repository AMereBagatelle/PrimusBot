import discord
from discord.ext import commands

import fileManager
import pollManager
import Constants

settingsFile = 'settings.txt'
bot = commands.Bot(command_prefix='.')

#starts poll
@bot.command()
async def poll(ctx, arg, *arg2):
    await ctx.send(arg)
    pollMessage = await ctx.send(embed=pollManager.newPoll(arg, arg2))

    i = 0

    for choice in arg2:
        await pollMessage.add_reaction(Constants.DISCORD_LETTERS[i])
        i += 1
    
@bot.command()
async def resolvePoll(ctx, arg):
    pollToResolve = await ctx.channel.history().get(content=arg)
    print(pollToResolve)
    


bot.run('NjU3OTIwNzg4MDk1MTcyNjA4.Xf6NxA.S4dKtW0GOlUEQO5gUsV5DCg5fyQ')
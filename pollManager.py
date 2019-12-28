import discord
import Constants

def newPoll(pollTitle, pollOptions):
    pollResult = ''
    pollFinal = ''

    if len(pollOptions) > len(Constants.DISCORD_LETTERS):
        return discord.Embed(title='Failed', type='rich', description='Less than 10 options, please.')

    i = 0
    for p in pollOptions:
        p = Constants.DISCORD_LETTERS[i] + ' ' + p + '\n'
        pollResult = pollResult + p
        i = i + 1

    return discord.Embed(title='', type='rich', description=pollResult)
import discord
import Constants

def newPoll(pollTitle, pollOptions):
    pollResult = ''
    pollFinal = ''

    # These two checks are to make sure that we don't get a invalid poll request, because that would just be no fun
    if len(pollOptions) > len(Constants.DISCORD_LETTERS):
        return discord.Embed(title='Failed', type='rich', description='Less than 10 options, please.')

    if len(pollOptions) < 2:
        return discord.Embed(title='Failed', type='rich', description='Make options!')

    # Assigns pollResult to the definition of the poll, which is the emoji + the option + a newline
    i = 0
    for p in pollOptions:
        p = Constants.DISCORD_LETTERS[i] + ' ' + p + '\n'
        pollResult = pollResult + p
        i = i + 1

    # The finished embed object
    return discord.Embed(title='', type='rich', description=pollResult)
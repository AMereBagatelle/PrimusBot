import discord
import Constants
import fileManager


def newPoll(pollOptions):
    pollResult = ''
    pollFinal = ''

    # These two checks are to make sure that we don't get a invalid poll request, because that would just be no fun
    if len(pollOptions) > len(Constants.DISCORD_LETTERS):
        return discord.Embed(title='Failed', type='rich', description='Less than 26 options, please.')

    if len(pollOptions) < 2:
        return discord.Embed(title='Failed', type='rich', description='Make more options!')

    # Assigns pollResult to the definition of the poll, which is the emoji + the option + a newline
    i = 0
    for p in pollOptions:
        p = Constants.DISCORD_LETTERS[i] + ' ' + p + '\n'
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
    #finds which channel to send results to
    sendChannel = int(fileManager.readLineOfFile(Constants.SETTINGS_FILE, 1)[13:-1])
    server = ctx.message.channel.guild
    for channel in server.channels:
        if channel.id == sendChannel:
            sendChannel = channel
    #returns results of all things determined in here
    return sendChannel, pollTitle, pollEmbed, pollResult

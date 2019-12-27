import discord
import fileManager

constantsFile = 'constants.txt'
prefix = '.'

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if message.author == client.user:
            return

        if startsWith(message, prefix):

            if startsWith(message, prefix + 'setchannel'):
                await message.channel.send('Will output moderator messages to this channel from this point onward.')
                fileManager.writeToLineOfFile(constantsFile, 0, 'ModChannel: {0.channel}'.format(message))

            if startsWith(message, prefix + 'polloutputchannel'):
                await message.channel.send('Will output poll outcomes to this channel from this point onward.')
                fileManager.writeToLineOfFile(constantsFile, 1, 'PollChannel: {0.channel}'.format(message))

        if startsWith(message, 'dig good'):
            await message.channel.send('dig good but dupe faster')

        if startsWith(message, 'doop bad'):
            await message.channel.send('no')

def startsWith(message, query):
    return message.content.startswith(query)

client = MyClient()
client.run('NjU3OTIwNzg4MDk1MTcyNjA4.Xf6NxA.S4dKtW0GOlUEQO5gUsV5DCg5fyQ')

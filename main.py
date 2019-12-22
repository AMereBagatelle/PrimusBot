import discord
import fileManager

constantsFile = 'constants.txt'

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if message.author == client.user:
            return

        if message.author == discord.commands.bot:
            return

        if message.content.startswith('.set-channel'):
            await message.channel.send('Will output moderator messages to this file from this point onward.')
            fileManager.writeToLineOfFile(constantsFile, 0, '{0.channel}'.format(message))

client = MyClient()
client.run('NjU3OTIwNzg4MDk1MTcyNjA4.Xf6NxA.S4dKtW0GOlUEQO5gUsV5DCg5fyQ')

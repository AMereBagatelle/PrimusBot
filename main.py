import discord


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if message.author == client.user:
            return

        if message.content.startswith('.set-channel'):
            await message.channel.send('Setting...')


        
            
def writeToLineOfFile(filename, line, content):
    fp = open(filename, 'r')
    lines = fp.readlines()
    fp.close()
    if len(lines) == 0:
        lines = content
        with open(filename, 'w') as fp:
            fp.writelines(lines)
    else:
        lines[line] = content
        fp = open(filename, 'w')
        fp.writelines(lines)
        fp.close()
        
def readLineOfFile(filename, line):
    with open(filename) as fp:
        return fp.readlines()[line]

client = MyClient()
client.run('NjU3NzEyMzY4Mjk3NDQzMzU4.Xf1mWg.35qKCUiW8Gu1lV7AdILwUsOXIyY')

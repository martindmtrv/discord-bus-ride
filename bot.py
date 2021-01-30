# bot.py
import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()


@client.event
async def on_ready():
    client.isPlaying = False
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not client.isPlaying and message.content.startswith('~ride'):
        client.isPlaying = True
        await message.channel.send('Its time to play')
    elif client.isPlaying and message.content == "~quit":
        client.isPlaying = False
        await message.channel.send('He\'s done')

client.run(TOKEN)

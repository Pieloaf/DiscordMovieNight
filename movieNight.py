from discord.ext import commands
import discord
import os

with open('./botToken') as file:
    botToken = file.readlines()

intents = discord.Intents.default()
client = commands.Bot(command_prefix='.', help_command=None, intents=intents)
game = discord.Activity(name="Movies 🍿", type=discord.ActivityType.watching)


@client.event
async def on_ready():
    print(f'{client.user} is ready')
    await client.change_presence(status=discord.Status.online, activity=game)


def loadCogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')
            print(f'loaded {filename}')


@client.command()
async def ping(ctx):
    await ctx.send("Pong!")

client.run(f'{botToken[0]}')

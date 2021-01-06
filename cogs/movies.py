from discord.ext import commands
import requests
import discord
import json
from os import path, remove
from const import *


class Movies(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.remove = False
        self.reviewMsg = None

    @commands.command()
    async def movievote(self, ctx):
        await ctx.message.delete()
        if not path.exists(f"./{ctx.guild.id}_movie.json"):

            embed = discord.Embed.from_dict(voteEmbed)
            msg = await ctx.send(embed=embed)
            await msg.add_reaction(usefulEmotes['no'])

            moviemenu = {}
            moviemenu['movies'] = []
            moviemenu['host'] = ctx.author.id
            moviemenu['movieMsg'] = {}
            moviemenu['movieMsg']['id'] = msg.id

            with open(f"./{ctx.guild.id}_movie.json", 'w') as json_file:
                json.dump(moviemenu, json_file)
        else:
            await ctx.send(MOVIEEXISTS)
            return

    @commands.command()
    async def addmovie(self, ctx):
        moviemenu = await self.isVoteActive(ctx)
        if moviemenu == None:
            return
        msg = await ctx.channel.fetch_message(moviemenu['movieMsg']['id'])
        embed = msg.embeds[0]
        if len(embed.fields) == 5:
            await ctx.send(LISTFULL)
            return

        title = ' '.join((ctx.message.content.split())[1:])
        movie = {}
        movie['emoji'] = None

        for emoji in voteEmotes:
            if emoji not in msg.reactions.emoji:
                movie['emoji'] = emoji
                break
            else:
                pass

        embed['fields'].append(
            name=f"{movie['emoji']} {movie['name']} ({movie['year']})",
            value=f"[Rotten Tomatoes: {movie['score']}]({movie['url']})",
        )
        moviemenu['movies'].append(movie)
        await msg.edit(embed=embed)
        await msg.add_reaction(movie['emoji'])

        with open(f"./{ctx.guild.id}_movie.json", 'w') as json_file:
            json.dump(moviemenu, json_file)

    async def isVoteActive(self, ctx):
        if not path.exists(f"./{ctx.guild.id}_movie.json"):
            await ctx.channel.send(NOVOTE)
            return None
        else:
            with open(f"./{ctx.guild.id}_movie.json", 'r') as json_file:
                moviemenu = json.load(json_file)
            return moviemenu

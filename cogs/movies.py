from discord.ext import commands
import requests
import discord
import json
from os import path
from const import *
from TMDb import search
import re


class Movies(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove = []

    @commands.command()
    async def movievote(self, ctx):
        await ctx.message.delete()
        if not path.exists(f"./{ctx.guild.id}_movie.json"):

            # creating and sending embed
            embed = discord.Embed.from_dict(voteEmbed)
            msg = await ctx.send(embed=embed)
            await msg.add_reaction(usefulEmotes['no'])

            # movie json
            moviemenu = {}
            moviemenu['movies'] = []
            moviemenu['host'] = ctx.author.id
            moviemenu['movieMsg'] = msg.id

            with open(f"./{ctx.guild.id}_movie.json", 'w') as json_file:
                json.dump(moviemenu, json_file)
        else:
            await ctx.send(MOVIEEXISTS)
            return

    @commands.command()
    async def addmovie(self, ctx):
        # check for vote
        moviemenu = await self.isVoteActive(ctx)
        if moviemenu == None:
            return

        # getting vote embed
        msg = await ctx.channel.fetch_message(moviemenu['movieMsg'])
        embed = msg.embeds[0]

        # check vote full
        if len(embed.fields) == 5:
            await ctx.send(LISTFULL)
            return

        # getting movie data
        query = ' '.join((ctx.message.content.split())[1:])
        try:
            year = re.findall("\((.*?)\)", query)[0]
        except Exception:
            year = ''
        title = query.split('(')[0]
        movie = search(title, year=year)

        # assinging movie reaction emote
        for emoji in voteEmotes:
            if emoji not in msg.reactions.emoji:
                movie['emoji'] = emoji
                break

        # adding field for new movie
        embed['fields'].append(
            name=f"{movie['emoji']} {movie['name']} ({movie['year']})",
            value=f"[Reviews: {movie['score']}%]({movie['url']})",
        )
        moviemenu['movies'].append(movie)
        await msg.edit(embed=embed)
        await msg.add_reaction(movie['emoji'])

        # updating movie json
        with open(f"./{ctx.guild.id}_movie.json", 'w') as json_file:
            json.dump(moviemenu, json_file)

    @commands.command()
    async def removemovie(self, ctx):
        # check for vote
        moviemenu = await self.isVoteActive(ctx.channel)
        await ctx.message.delete()
        if moviemenu == None:
            return

        if ctx.author.id == moviemenu['host']:
            removeMsg = await ctx.send("React to remove a movie")
            self.bot.remove.append((ctx.channel.id, removeMsg.id))

    async def isVoteActive(self, ctx):
        if not path.exists(f"./{ctx.guild.id}_movie.json"):
            await ctx.channel.send(NOVOTE)
            return None
        else:
            with open(f"./{ctx.guild.id}_movie.json", 'r') as json_file:
                moviemenu = json.load(json_file)
            return moviemenu


def setup(bot):
    bot.add_cog(Movies(bot))

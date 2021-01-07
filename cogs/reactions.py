from discord.ext import commands
import discord
import json
from os import remove
from const import voteEmotes, usefulEmotes, GETIMAGE
import re
from TMDb import getThumb


class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.review = []

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return
        # init vars
        channel = self.bot.get_channel(payload.channel_id)
        user = self.bot.get_user(payload.user_id)
        emoji = payload.emoji
        msg = await channel.fetch_message(payload.message_id)

        print(self.review)
        print(msg.id)
        # post-movie review
        if msg.id in self.review:
            # ending review
            if emoji.name == usefulEmotes['yes']:

                totalcount = 0
                scoresum = 0
                votes = enumerate(
                    [reaction.count-1 for reaction in msg.reactions][1:6],
                    start=1
                )

                # calculating result
                for score, count in list(votes):
                    totalcount += count
                    scoresum += score*count
                rating = scoresum/totalcount

                # updating result embed
                ratingEmbed = msg.embeds[0].add_field(
                    name=f"Rating:", value=f"{rating}/5", inline=True
                )
                await msg.edit(embed=ratingEmbed)
                await msg.clear_reactions()
                self.review.remove(msg.id)
            return
        # Is there a vote
        try:
            with open(f"./{msg.guild.id}_movie.json", 'r') as json_file:
                moviemenu = json.load(json_file)
        except:
            return

        # Only host can edit
        if not user.id == moviemenu['host']:
            await msg.remove_reaction(usefulEmotes['no'], user)
            return

        # Ending Vote
        if msg.id == moviemenu['movieMsg']:
            if emoji.name == usefulEmotes['no']:
                await self.results(msg)
                return
        # Removing Movies
        if msg.id in self.bot.remove:
            # list of reactions excluding no
            reactEmoji = [reaction.emoji for reaction in msg.reactions][1:]

            # updating json
            moviemenu['movies'].pop(reactEmoji.index(emoji.name))
            with open(f'./{msg.guild.id}_movie.json', 'w') as json_file:
                json.dump(moviemenu, json_file)

            # updating message
            await msg.clear_reaction(emoji.name)
            embed = msg.embeds[0]
            embed.remove_field(reactEmoji.index(emoji.name))
            await msg.edit(embed=embed)

            self.bot.remove.remove(msg.id)
            return

    async def results(self, msg):
        remove(f'./{msg.guild.id}_movie.json')
        msgEmbed = msg.embeds[0].to_dict()
        movies = []
        for field in msgEmbed['fields']:
            url = re.findall("\((.*?)\)", field['value'])[0]
            movies.append(
                {
                    'title': (' ').join(field['name'].split()[1:]),
                    'url': url,
                    'description': re.findall('\[(.*?)\]', field['value'])[0],
                    'color': 11306689,
                    'thumbnail': {
                        'url': getThumb(url.split('/')[-1])
                    }
                }
            )
        votes = [reaction.count-1 for reaction in msg.reactions][1:]
        winIndex = votes.index(max(votes))

        winner = movies[winIndex]

        embed = discord.Embed.from_dict(winner)
        embed.add_field(
            name=f"Votes: {max(votes)}",
            value=f"Total Votes: {sum(votes)}",
            inline=True
        )
        await msg.delete()

        # review message
        review = await msg.channel.send(embed=embed)
        self.review.append(review.id)
        await review.add_reaction('✅')
        for emoji in voteEmotes:
            await review.add_reaction(emoji)


def setup(bot):
    bot.add_cog(Reactions(bot))

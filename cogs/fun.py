import asyncio
import random

import discord
from discord.ext import commands

from utils.scraper import Scraper


class FunCog(commands.Cog):

    hidden = False
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.hybrid_command(name='spacefacts', aliases=['spacefact'], brief='Get random facts about space!')
    async def spacefacts(self, ctx: commands.Context) -> None:
        scraper = Scraper(self.bot.session)
        fact = await scraper.scrape()
        await ctx.send(fact)

    @commands.hybrid_command(name="guesstheuniverse", aliases=['gtu'], brief="Guess the universe with the given information")
    async def guesstheuniverse(self, ctx: commands.Context) -> None:
        key = random.choice(tuple(self.bot.universe_trivia.keys()))
        info = self.bot.universe_trivia[key]
        on_basis = random.choice(['description', 'constellation'])
        on_bases_info = info[on_basis]
        embed = discord.Embed(
            title="Guess The Universe",
            description=f"**{on_basis}**: {on_bases_info}",
            color=self.bot.theme
        )
        embed.set_image(url=info['image'])
        await ctx.send(embed=embed)
        while True:
            try:
                message = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
            except asyncio.TimeoutError:
                return await ctx.send("You took too long to answer. Try again.")
            else:
                if message.content.lower() in map(lambda x: x.lower(), info['answers']):
                    return await ctx.send(f"You got it! It was {key}")
                elif message.content.lower() in ('quit', 'exit'):
                    return await ctx.send(f"You quit the game. The answer was {key}\nAlternate answers: {', '.join(info['answers'])}")
                else:
                    await ctx.send(f"Wrong, maybe try again!", ephemeral=True, delete_after=5.0)
                
    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(FunCog(bot))
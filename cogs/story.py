import json
from typing import Mapping

import discord
from discord.ext import commands

from utils.ui.view import ConfirmButton
from utils.models import SpaceBot

class StoryCog(commands.Cog):

    hidden = False
    def __init__(self, bot: SpaceBot) -> None:
        self.bot = bot
        self.missions: Mapping[str, dict] = None

    async def cog_load(self) -> None:
        with open('./information/missions.json', 'r') as f:
            self.missions = json.load(f)

    async def enable_story_mode(self, user: discord.User):
        story = self.bot.get_conn('story')
        if story:
            async with story.cursor() as cursor:
                await cursor.execute('INSERT INTO story (user_id, enabled) VALUES (?, ?)', (user.id, 1))
                await story.commit()
        self.bot.verified[user.id].story_progression = 1

    async def get_user_progression(self, user: discord.User):
        cached_progression = self.bot.verified.get(user.id).story_progression
        if cached_progression is False:
            return False
        elif cached_progression:
            return cached_progression
        else:
            story = self.bot.get_conn('story')
            if story:
                async with story.cursor() as cursor:
                    await cursor.execute('SELECT progression FROM story WHERE user_id = ?', (self.bot.user.id,))
                    result = await cursor.fetchone()
                    if result:
                        self.bot.verified[user.id].story_progression = result[0]
                        return result[0]
            return False
        

    @commands.hybrid_command(name="begin", brief="Start the story mode of the bot")
    async def begin(self, ctx: commands.Context) -> None:
        embed = discord.Embed(
            title="Story mode", 
            description="You are trying to activate the story mode of the bot.\n"
            "After initiating, be prepared to work work under limited time.\n"
            "If you fail to clear one mission, you will faill and you will have to start over.\n"
            "Are you sure you want to start the story mode?",
            )
        view = ConfirmButton(ctx)
        await ctx.send(
            embed=embed,
            view=view,
            ephemeral=True
        )
        view_not_touched = await view.wait()
        if not view_not_touched and view.confirmed:
            await self.enable_story_mode(ctx.author)
            await ctx.send("Story mode has been activated!", ephemeral=True)
        elif not view_not_touched and not view.confirmed:
            await ctx.send("Story mode has been cancelled.", ephemeral=True)

    @commands.hybrid_command(name="mission", brief="Get the current mission")
    async def mission(self, ctx: commands.Context) -> None:
        current_progress = await self.get_user_progression(ctx.author)
        match current_progress:
            case False:
                return await ctx.send(f"You have not started the story mode yet. Please use `{ctx.prefix}begin` to start the story mode.")
            case _:
                stuff = self.missions[str(current_progress)]
                embed = discord.Embed(title=stuff['name'], description=stuff['description'], color=self.bot.theme)
                embed.set_footer(text=f"Mission {current_progress}/{len(self.missions)}")
                await ctx.send(embed=embed)

async def setup(bot: SpaceBot) -> None:
    await bot.add_cog(StoryCog(bot))
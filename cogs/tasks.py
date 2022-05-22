import discord
from discord.ext import commands, tasks

from utils.models import SpaceBot

class TaskCog(commands.Cog):
    
    hidden = True
    def __init__(self, bot: SpaceBot) -> None:
        self.bot = bot
        
    async def cog_load(self) -> None:
        self.change_activities.start()

    @tasks.loop(minutes=2)
    async def change_activities(self):
        activity = discord.Activity(
            type = discord.ActivityType.watching, name=next(self.bot.activities)
        )
        await self.bot.change_presence(activity=activity)

    @change_activities.before_loop
    async def before_change_activities(self):
        await self.bot.wait_for('ready')

async def setup(bot: SpaceBot) -> None:
    await bot.add_cog(TaskCog(bot))
    
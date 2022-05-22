import sys
import traceback

import discord
from discord.ext import commands

from utils.errors import UserNotVerified
from utils.models import SpaceBot
from utils.ui.view import ConfirmButton


class ListenerCog(commands.Cog):
    
    hidden = True
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener('on_command_error')
    async def check_errors(self, ctx: commands.Context, error):
        if isinstance(error, UserNotVerified):
            embed = discord.Embed(
                title="You're not verified!", 
                description="You need to verify yourself to use this command.\n" 
                "`1.` This verification is to make you aware of the terms of service for using the bot.\n"
                "`2.` By verifying, you give the bot the permission to store information of your account available"
                " publicly in our databse. ID, name, avatar etc.\n"
                "`3.` You can request for removal at any given time, by doing so, you would no longer to use the bot and its services."
                "If you agree to the above point, you can click the confirm button below to verify yourself.", 
                color=self.bot.theme
            )
            view = ConfirmButton(ctx)
            await ctx.send(embed=embed, view=view)
            view_not_touched = await view.wait()
            if not view_not_touched and view.confirmed:
                await self.bot.verify_user(ctx.author)
                await ctx.send("You're now verified!", ephemeral=True)
            elif not view_not_touched and not view.confirmed:
                await ctx.send("You've cancelled the verification process.", ephemeral=True)
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


async def setup(bot: SpaceBot) -> None:
    await bot.add_cog(ListenerCog(bot))

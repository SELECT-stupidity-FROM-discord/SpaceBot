import os
from typing import Optional

from discord.ext import commands
from dotenv import load_dotenv

from utils.errors import UserNotVerified
from utils.models import Cache, SpaceBot, SpaceHelp

bot = SpaceBot()
bot.help_command = SpaceHelp()
load_dotenv('.env')


@bot.check
async def check_if_user_verified(ctx: commands.Context) -> Optional[bool]:
    author = bot.verified.get(ctx.author.id)
    if author:
        if author.verified:
            return True
        else:
            raise UserNotVerified(ctx.author)
    else:
        verified = bot.get_conn('verified')
        if verified:
            async with verified.cursor() as cursor:
                await cursor.execute('SELECT * FROM verified WHERE user_id = ?', (ctx.author.id,))
                record = bool(await cursor.fetchone())
            bot.verified[ctx.author.id] = Cache(verified=record)
        if record is True:
            return True
        raise UserNotVerified(ctx.author)

os.environ["JISHAKU_NO_UNDERSCORE"] = "true"
os.environ["SHELL"] = "/bin/zsh"

@bot.command(name="sync", brief="Sync slash commands")
@commands.is_owner()
async def _sync(ctx: commands.Context) -> None:
    await bot.tree.sync()
    await ctx.send("Synced slash commands to global!")


TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)

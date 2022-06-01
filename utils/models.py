import json
import os
import logging
from itertools import cycle
from dataclasses import dataclass
from typing import Dict, List, Literal, Mapping, Optional

import aiohttp
import aiosqlite
import discord
from bs4 import BeautifulSoup
from discord.ext import commands

from .ui.view import HelpView


# dataclass for caching user;s information
@dataclass(slots=True, repr=True, kw_only=True)
class Cache:
    verified: bool
    story_progression: Optional[int] = None

# Holds the bot's cache of opened databases
class Database:
    def __init__(self, connections: Mapping[str, aiosqlite.Connection]) -> None:
        self._conn = connections

    def __getitem__(self, name: str) -> Optional[aiosqlite.Connection]:
        return self._conn.get(name)


# Praser for the Scraper
class WebsiteParser(BeautifulSoup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def get_head(self, sub: Literal[1, 2, 3, 4, 5, 6], *args) -> Optional[str]:
        return self.find(f"h{sub}", *args)


# Bot class for the bot
class SpaceBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        intents = discord.Intents(
            guilds=True,
            members=True,
            emojis=True,
            messages=True,
            guild_messages=True,
            dm_messages=True,
            message_content=True,
            presences=True
        )
        super().__init__(
            command_prefix=commands.when_mentioned_or('>>'),
            intents=intents
        )

        self.verified: Dict[int, Cache] = {}
        self.activities = cycle(['Space is almost endless.', '10⁷ K?', 'No stars? No moons? No planets? Damn that\'s sad.'])
        self.logger = self.get_logger()
        self.session: Optional[aiohttp.ClientSession] = None
        self._conn: Optional[Database] = None
        self.universe_trivia = self.load_information()
        self.theme = 0xF5F5DC

    async def verify_user(self, user: discord.Member) -> None:
        verified = self.get_conn('verified')
        if verified:
            async with verified.cursor() as cursor:
                statement = 'INSERT INTO verified (user_id) VALUES (?)'
                await cursor.execute(statement, (user.id,))
                await verified.commit()
            self.verified[user.id] = Cache(verified=True)

    async def setup_hook(self) -> None:
        await self.load_extension('jishaku')
        jishaku_cog = self.get_cog('Jishaku')
        if jishaku_cog:
            jishaku_cog.hidden = True
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
        
    def get_logger(self):
        logger = logging.getLogger('discord')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('LEVEL [%(levelname)s] at (%(asctime)s): %(name)s: %(message)s'))
        logger.addHandler(handler)
        return logger

    def get_conn(self, name: str) -> Optional[aiosqlite.Connection]:
        return self._conn[name]

    def load_information(self):
        with open('./information/galaxy.json', 'r') as f:
            return json.load(f)

    async def init_database(self, **kwargs) -> None:
        self._conn = Database(kwargs)

    async def on_ready(self) -> None:
        self.logger.info(f"Logged in as {self.user} ({self.user.id}), preparing to conquer the universe.")
        print(f"Logged in as {self.user} ({self.user.id}), preparing to conquer the universe.")

    async def create_tables(self) -> None:
        SCHEMA_VERIFIED = """
                CREATE TABLE IF NOT EXISTS verified (
                        user_id INTEGER PRIMARY KEY
                );
                """
        SCHEMA_STORY = """
                CREATE TABLE IF NOT EXISTS story (
                        user_id INTEGER PRIMARY KEY,
                        enabled INTEGER,
                        progression INTEGER DEFAULT 0
                );
                """

        verified = self.get_conn('verified')
        story = self.get_conn('story')

        if verified:
            async with verified.cursor() as cursor:
                await cursor.execute(SCHEMA_VERIFIED)
        if story:
            async with story.cursor() as cursor:
                await cursor.execute(SCHEMA_STORY)


    async def start(self, *args, **kwargs) -> None:
        async with aiohttp.ClientSession() as self.session:
            async with aiosqlite.connect('./database/verified.db') as verified:
                async with aiosqlite.connect('./database/story.db') as story:
                    await self.init_database(verified=verified, story=story)
                    await self.create_tables()
                    await self.fill_verification_cache()
                    return await super().start(*args, **kwargs)

    async def fill_verification_cache(self):
        verified = self.get_conn('verified')
        if verified:
            async with verified.cursor() as cursor:
                await cursor.execute('SELECT * FROM verified')
                async for record in cursor:
                    self.verified[record[0]] = Cache(verified=True)


# Help command for the bot

class SpaceHelp(commands.HelpCommand):
    def __init__(self) -> None:
        super().__init__(command_attrs={'hidden': True})
        self.banner = "https://i.imgur.com/HIyFo04.jpg"

    async def send_bot_help(self, mapping: Dict[commands.Cog, List[commands.Command]]) -> None:
        embeds = []
        for cog, commands in mapping.items():
            if (not cog) or (cog and cog.hidden):
                continue
            commands = "\n".join(f"• {command.qualified_name} - {command.brief}" for command in commands if not command.hidden)
            embed = discord.Embed(title=f"{cog.qualified_name} Commands", description=commands, color=self.context.bot.theme)
            embed.set_image(url=self.banner)
            embed.set_footer(text=f"{self.context.bot.user.name}", icon_url=self.context.author.display_avatar.url)
            embeds.append(embed)
        view = HelpView(self.context, embeds)
        destination = self.get_destination()
        await destination.send(embed=embed, view=view)

    async def send_cog_help(self, cog: commands.Cog) -> None:
        command_list = [command for command in cog.walk_commands()]
        commands = "\n".join(f"• {command.qualified_name} - {command.brief}" for command in command_list if not command.hidden)
        embed = discord.Embed(title=f"{cog.qualified_name} Commands", description=commands, color=self.context.bot.theme)
        embed.set_image(url=self.banner)
        embed.set_footer(text=f"{self.context.bot.user.name}", icon_url=self.context.author.display_avatar.url)
        destination = self.get_destination()
        await destination.send(embed=embed)

    async def send_command_help(self, command: commands.Command) -> None:
        embed = discord.Embed(title=f"{command.qualified_name}", description=command.help, color=self.context.bot.theme)
        embed.set_image(url=self.banner)
        embed.set_footer(text=f"{self.context.bot.user.name}", icon_url=self.context.author.display_avatar.url)
        destination = self.get_destination()
        await destination.send(embed=embed)
    
            


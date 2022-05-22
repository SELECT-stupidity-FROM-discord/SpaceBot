from typing import List

import discord
from discord import ui
from discord.ext import commands

class ConfirmButton(ui.View):
    def __init__(self, ctx: commands.Context) -> None:
        super().__init__(timeout=60)
        self.confirmed = None
        self.ctx = ctx


    @ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(
        self, 
        interaction: discord.Interaction, 
        button: discord.Button
    ) -> None:
        self.confirmed = True
        if interaction.message:
            await interaction.message.delete()
        else:
            interaction.delete_original_message()
        self.stop()
    
    @ui.button(label='Cancel', style=discord.ButtonStyle.red)
    async def cancel(
        self, 
        interaction: discord.Interaction, 
        button: discord.Button
    ) -> None:
        if interaction.message:
            await interaction.message.delete()
        else:
            interaction.delete_original_message()
        self.stop()

class HelpView(ui.View):
    def __init__(self, ctx: commands.Context, embeds: List[discord.Embed]) -> None:
        super().__init__(timeout=60)
        self.embeds = embeds
        self.counter = 0

    def forward(self):
        if self.counter + 1 < len(self.embeds):
            self.counter += 1
            return self.embeds[0]
        return


    def backward(self):
        if self.counter > 0:
            self.counter -= 1
            return self.embeds[0]
        return


    def update_side(self, side: str, disabled: bool):
        match side:
            case 'left':
                for index, child in enumerate(self.children):
                    if index < 2:
                        child.disabled = disabled
                    else:
                        child.disabled = not disabled
            case 'right':
                for index, child in enumerate(self.children):
                    if index > 2:
                        child.disabled = disabled
                    else:
                        child.disabled = not disabled
            case 'all':
                for child in self.children:
                    child.disabled = True
            

    @ui.button(emoji="\N{Black Left-Pointing Double Triangle}",style=discord.ButtonStyle.blurple, disabled=True)
    async def first_embed(self, interaction: discord.Interaction, button: discord.Button):
        embed = self.embeds[0]
        self.counter = 0
        self.update_side('left', True)
        return await interaction.message.edit(embed=embed, view=self)


    @ui.button(emoji="\N{Leftwards Black Arrow}",style=discord.ButtonStyle.blurple, disabled=True)
    async def previous_embed(self, interaction: discord.Interaction, button: discord.Button):
        embed = self.backward()
        if self.counter == 0:
            self.update_side('left', True)
        else:
            self.update_side('all', False)
        if embed:
            await interaction.message.edit(embed=embed, view=self)
        return

    @ui.button(emoji="\N{Black Square for Stop}",style=discord.ButtonStyle.blurple)
    async def stop_embed(self, interaction: discord.Interaction, button: discord.Button):
        self.update_side('all', True)
        if interaction.message:
            await interaction.message.edit(view=self)
        else:
            await interaction.edit_original_message(view=self)
        self.stop()


    @ui.button(emoji="\N{Black Rightwards Arrow}",style=discord.ButtonStyle.blurple)
    async def next_embed(self, interaction: discord.Interaction, button: discord.Button):
        embed = self.forward()
        if self.counter == len(self.embeds) - 1:
            self.update_side('right', True)
        else:
            self.update_side('all', False)
        if embed:
            await interaction.message.edit(embed=embed, view=self)
        return


    @ui.button(emoji="\N{Black Right-Pointing Double Triangle}",style=discord.ButtonStyle.blurple)
    async def last_embed(self, interaction: discord.Interaction, button: discord.Button):
        embed = self.embeds[-1]
        self.counter = len(self.embeds) - 1
        self.disable_side('right')
        return await interaction.message.edit(embed=embed, view=self)
        


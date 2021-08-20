#Copyright © 2021  RockSolid1106
#This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License.
#
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

from discord.ext import commands
client=commands.Bot(command_prefix="!")
class xyz(commands.Cog, name="Hello"):
	def __init__(self, client: commands.Bot):
		self.client = commands.Bot(command_prefix="!")
	
	@commands.command(pass_context=True, brief="Timepass")
	async def sup(self, ctx):
		await ctx.send(f'Hello there {ctx.author.mention}, how are you doing?')
	@commands.command()
	async def reply(self, ctx):
		await ctx.send("sup")

def setup(client: commands.Bot):
	client.add_cog(xyz(client))
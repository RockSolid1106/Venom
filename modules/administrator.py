#Copyright © 2021  RockSolid1106
#This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License.
#
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

import pyotp
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import time
from replit import db
import os
from keep_alive import keep_alive
import datetime
import random
#from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import hmac, base64, struct, hashlib, array
errordic={}
client=commands.Bot(command_prefix="!")
class admin(commands.Cog, name="Admin", command_attrs=dict(hidden=True)):
	errordic={}
	def __init__(self, client: commands.Bot):
		self.client = commands.Bot(command_prefix="!")
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		#await ctx.send(f"An error occured: ```{str(error)}```")
		print(error)
		errordic[ctx.guild.id+ctx.channel.id]=error

	@commands.command()
	async def showerror(self, ctx):
		if ctx.author.id!=825282868028375062 and ctx.author.id==820189220185833472:
			await ctx.send("You don't have permission to use this command.")
		error=errordic[ctx.guild.id+ctx.channel.id]
		await ctx.send("Here is the last error: ```"+str(error)+"```")
		
		




def setup(client: commands.Bot):
	client.add_cog(admin(client))
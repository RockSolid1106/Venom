#Copyright © 2021  RockSolid1106
#This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License.
#
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

import pyotp
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands import Bot
from replit import db
#from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
errordic={}
client=commands.Bot(command_prefix="!")
class admin(commands.Cog, name="Admin", command_attrs=dict(hidden=True)):
	errordic={}
	def __init__(self, client: commands.Bot):
		self.client = client
	
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		#await ctx.send(f"An error occured: ```{str(error)}```")
		print(error)
		errordic[ctx.guild.id+ctx.channel.id]=error
		

	@commands.command()
	async def showerror(self, ctx):
		if ctx.author.id!=825282868028375062 and ctx.author.id!=820189220185833472:
			await ctx.send("You don't have permission to use this command.")
			return
		error=errordic[ctx.guild.id+ctx.channel.id]
		await ctx.send("Here is the last error: ```"+str(error)+"```")
	
	@commands.command()
	async def whoami(self, ctx):
		if ctx.author.id==825282868028375062:# and ctx.author.id==820189220185833472:
			await ctx.send(f"{ctx.author.mention} is my developer. He has got access to all the commands, even if he doesn't have the roles, just so you know.")
		elif ctx.author.id==820189220185833472:
			await ctx.send(f"{ctx.author.mention} is my co-developer. He has got access to all the commands, even if he doesn't have the roles, just so you know.")
		elif ctx.author.id==822679233720745984:
			await ctx.send(f"{ctx.author.mention} is poggers")
		else:
			await ctx.send("You're just the average human.")


	@commands.command()
	async def changestatus(self, ctx, status, activity_type, activity):
		if ctx.author.id!=825282868028375062 and ctx.author.id!=820189220185833472:
			await ctx.send("You don't have permission to use this command.")
			return
		if status == "idle":
			if activity_type == "listening":
				await self.client.change_presence(status = discord.Status.idle,activity=discord.Activity(type=discord.ActivityType.listening, name=activity))
			elif activity_type == "playing":
				await self.client.change_presence(status = discord.Status.idle,activity=discord.Activity(type=discord.ActivityType.playing, name=activity))
			elif activity_type == "watching":
				await self.client.change_presence(status = discord.Status.idle,activity=discord.Activity(type=discord.ActivityType.watching, name=activity))

		if status == "dnd" or status == "DND":
			if activity_type == "listening":
				await self.client.change_presence(status = discord.Status.dnd,activity=discord.Activity(type=discord.ActivityType.listening, name=activity))
			elif activity_type == "playing":
				await self.client.change_presence(status = discord.Status.dnd,activity=discord.Activity(type=discord.ActivityType.playing, name=activity))
			elif activity_type == "watching":
				await self.client.change_presence(status = discord.Status.dnd,activity=discord.Activity(type=discord.ActivityType.watching, name=activity))
				
		if status == "offline":
			if activity_type == "listening":
				await self.client.change_presence(status = discord.Status.offline,activity=discord.Activity(type=discord.ActivityType.listening, name=activity))
			elif activity_type == "playing":
				await self.client.change_presence(status = discord.Status.offline,activity=discord.Activity(type=discord.ActivityType.playing, name=activity))
			elif activity_type == "watching":
				await self.client.change_presence(status = discord.Status.offline,activity=discord.Activity(type=discord.ActivityType.watching, name=activity))

		if status == "online":
			if activity_type == "listening":
				await self.client.change_presence(status = discord.Status.online,activity=discord.Activity(type=discord.ActivityType.listening, name=activity))
			elif activity_type == "playing":
				await self.client.change_presence(status = discord.Status.online,activity=discord.Activity(type=discord.ActivityType.playing, name=activity))
			elif activity_type == "watching":
				await self.client.change_presence(status = discord.Status.online,activity=discord.Activity(type=discord.ActivityType.watching, name=activity))

		if status == "invisible":
			if activity_type == "listening":
				await self.client.change_presence(status = discord.Status.invisible,activity=discord.Activity(type=discord.ActivityType.listening, name=activity))
			elif activity_type == "playing":
				await self.client.change_presence(status = discord.Status.invisible,activity=discord.Activity(type=discord.ActivityType.playing, name=activity))
			elif activity_type == "watching":
				await self.client.change_presence(status = discord.Status.invisible,activity=discord.Activity(type=discord.ActivityType.watching, name=activity))

	


def setup(client: commands.Bot):
	client.add_cog(admin(client))
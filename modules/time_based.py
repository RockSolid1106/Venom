#Copyright © 2021  RockSolid1106
#This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License.
#
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from replit import db
#from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

client=commands.Bot(command_prefix="!")
class time_commands(commands.Cog, name="Time Based"):
	def __init__(self, client: commands.Bot):
		self.client = commands.Bot(command_prefix="!")


	def admincheck(self, ctx):
		if ctx.author.id==825282868028375062 or ctx.author.id==820189220185833472:
			return True
		role = discord.utils.find(lambda r: r.name == 'Owner', ctx.message.guild.roles)
		role2 = discord.utils.find(lambda r: r.name == 'Admin', ctx.message.guild.roles)
		if role in ctx.author.roles or role2 in ctx.author.roles:
			return True
		else:
			return False

	def modcheck(self, ctx):
		if ctx.author.id==825282868028375062 or ctx.author.id==820189220185833472:
			return True
		role = discord.utils.find(lambda r: r.name == 'Owner', ctx.message.guild.roles)
		role2 = discord.utils.find(lambda r: r.name == 'Admin', ctx.message.guild.roles)
		role3 = discord.utils.find(lambda r: r.name == 'Moderator', ctx.message.guild.roles)
		if role in ctx.author.roles or role2 in ctx.author.roles or role3 in ctx.author.roles:
			return True
		else:
			return False

	@commands.command(pass_context=True, brief="Mutes a user for specified time.", description="Mutes a user for specified time. \nExample: !tempmute @someone 10m \"test\" \nAccepted units of time are: s(Seconds), m(Months *cough cough* Minutes) and d(Days).")
	#@commands.has_any_role("Moderator", "Owner", "Admin")
	async def tempmute(self, ctx, member: discord.Member, time, reason=None):
			if self.modcheck(ctx)==False:
				await ctx.send("Tryna use mod commands huh?")
				return
			if member.id==825282868028375062 or member.id==820189220185833472:
				await ctx.send("This user cannot be temp-muted.")
				return
			unitoftime=time[-1:]
			time=time[:-1]
			time=int(time)
			if unitoftime=="s":
				timex="Seconds"
			elif unitoftime=="m":
				timex="Minutes"
			elif unitoftime=="d":
				timex="Days"
			else:
				await ctx.send("That is not a valid unit of time.")
				return
			elevperms=False
			guild = ctx.guild
			d=unitoftime
			role = discord.utils.find(lambda r: r.name == 'Moderator', ctx.message.guild.roles)
			role2 = discord.utils.find(lambda r: r.name == 'Owner', ctx.message.guild.roles)
			if role2 in ctx.author.roles or ctx.author.id==825282868028375062:
				elevperms=True

			if role in member.roles:# or role2 in member.roles:
				if elevperms!=True:
					await ctx.send("A moderator cannot mute an Owner.")
					return
				else:
					role = discord.utils.get(member.guild.roles, name="Muted")
					await member.add_roles(role)
					role = discord.utils.get(member.guild.roles, name="Member")
					await member.remove_roles(role)
					role = discord.utils.get(member.guild.roles, name="Moderator")
					await member.remove_roles(role)
					embed = discord.Embed(title="Moderator muted!", description=f"{member.mention} has been tempmuted ", colour=discord.Colour.red())
					embed.add_field(name="Reason:", value=reason, inline=False)
					embed.add_field(name="Time left for the mute:", value=f"{time} {timex}", inline=False)
					await ctx.send(embed=embed)

					if d == "s":
							await asyncio.sleep(time)

					if d == "m":
							await asyncio.sleep(time*60)

					if d == "h":
							await asyncio.sleep(time*60*60)

					if d == "d":
							await asyncio.sleep(time*60*60*24)

					role = discord.utils.get(member.guild.roles, name="Member")
					await member.add_roles(role)
					role = discord.utils.get(member.guild.roles, name="Moderator")
					await member.add_roles(role)
					role = discord.utils.get(member.guild.roles, name="Muted")
					await member.remove_roles(role)

					embed = discord.Embed(title="Temp Unmuted", description=f"Unmuted {member.mention}.", colour=discord.Colour.light_gray())
					await ctx.send(embed=embed)

					return
					
				
			
			

			guild = ctx.guild
			d=unitoftime
			
			role = discord.utils.get(member.guild.roles, name="Muted")
			await member.add_roles(role)
			role = discord.utils.get(member.guild.roles, name="Member")
			await member.remove_roles(role)

			embed = discord.Embed(title="Member muted!", description=f"{member.mention} has been tempmuted ", colour=discord.Colour.red())
			embed.add_field(name="Reason:", value=reason, inline=False)
			embed.add_field(name="Time left for the mute:", value=f"{time} {timex}", inline=False)
			await ctx.send(embed=embed)

			if d == "s":
					await asyncio.sleep(time)

			if d == "m":
					await asyncio.sleep(time*60)

			if d == "h":
					await asyncio.sleep(time*60*60)

			if d == "d":
					await asyncio.sleep(time*60*60*24)

			role = discord.utils.get(member.guild.roles, name="Member")
			await member.add_roles(role)
			role = discord.utils.get(member.guild.roles, name="Muted")
			await member.remove_roles(role)

			embed = discord.Embed(title="Temp Unmuted", description=f"Unmuted {member.mention}.", colour=discord.Colour.light_gray())
			await ctx.send(embed=embed)
			print("nonmodunmute")

			return


def setup(client: commands.Bot):
	client.add_cog(time_commands(client))
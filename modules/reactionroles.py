#Copyright © 2021  RockSolid1106
#This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License.
#
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
import emoji
import pyotp
import asyncio
import discord
from discord.utils import get
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

client=commands.Bot(command_prefix="!")
class roles(commands.Cog, name="Reaction Roles"):
	def __init__(self, client: commands.Bot):
		self.client = commands.Bot(command_prefix="!")

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		member=payload.member
		demojized=emoji.demojize(str(payload.emoji))
		print(demojized)
		if payload.message_id==878873030468710410:
			if "1" in demojized:
				print("true")
				role=discord.utils.get(member.guild.roles, name="10-A")
				await payload.member.add_roles(role)
			elif "2" in demojized:
				print("true")
				role=discord.utils.get(member.guild.roles, name="10-B")
				await payload.member.add_roles(role)

			elif "3" in demojized:
				print("true")
				role=discord.utils.get(member.guild.roles, name="10-C")
				await payload.member.add_roles(role)

			elif "4" in demojized:
				print("true")
				role=discord.utils.get(member.guild.roles, name="10-D")
				await payload.member.add_roles(role)

			elif "5" in demojized:
				print("true")
				role=discord.utils.get(member.guild.roles, name="10-E")
				await payload.member.add_roles(role)
			


def setup(client: commands.Bot):
	client.add_cog(roles(client))
#Copyright © 2021  RockSolid1106
#This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License.
#
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import time
import os
import datetime
import random
from dateutil import parser

client=commands.Bot(command_prefix="!")
class member(commands.Cog, name="Member"):
	def __init__(self, client: commands.Bot):
		self.client = commands.Bot(command_prefix="!")
	

"""
	@commands.Cog.listener()
	async def on_message_delete(self, message):
		async for entry in message.guild.audit_logs(limit=5,action=discord.AuditLogAction.message_delete):
				deleter = entry.user
		print(f"{deleter.name} deleted message a by {message.author.name}. Content: {message.content}")
		file1 = open("MyFile.txt","a")
		file1.write(f"{deleter.name} deleted a message posted by {message.author}: {message.content}")
		"""

	


def setup(client: commands.Bot):
	client.add_cog(member(client))




#Copyright © 2021  RockSolid1106
#This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License.
#
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands import Bot

client=commands.Bot(command_prefix="!")
class member(commands.Cog, name="Member"):
	def __init__(self, client: commands.Bot):
		self.client = commands.Bot(command_prefix="!")
	

	
	@commands.Cog.listener()
	async def on_message_delete(self, message):
		if len(message.attachments) == 0:
			attach = ""
		else:
			attach = "\n\tAttachment URLs: "
			for x in message.attachments:
				attach = attach + "\n\t\t" + x.url
		if (str(message.guild.id)+"_"+str(message.channel.id)) in Bot.delmessages:
			Bot.delmessages[str(message.guild.id)+"_"+str(message.channel.id)].insert(0, str(message.author) + "'s message was deleted: " + message.content + attach)
			if len(Bot.delmessages[str(message.guild.id)+"_"+str(message.channel.id)]) > 30:
				i = 30
				while i<len(Bot.delmessages[str(message.guild.id)+"_"+str(message.channel.id)]):
					Bot.delmessages[str(message.guild.id)+"_"+str(message.channel.id)].pop(i)
		else:
			Bot.delmessages[str(message.guild.id)+"_"+str(message.channel.id)] = []
			Bot.delmessages[str(message.guild.id)+"_"+str(message.channel.id)].insert(0, str(message.author) + " deleted: " + message.content)


	@commands.Cog.listener()
	async def on_message_edit(self, message_before, message_after):

		if str(message_before.id) in Bot.editmessages:
			Bot.editmessages[str(message_before.id)].insert(0, str(message_before.author) + "'s message was edited \nfrom: " + message_before.content + "\nto: " + message_after.content)

		else:
			Bot.editmessages[str(message_before.id)] = []
			Bot.editmessages[str(message_before.id)].insert(0, str(message_before.author) + "'s message was edited \nfrom: " + message_before.content + "\nto: " + message_after.content)


def setup(client: commands.Bot):
	client.add_cog(member(client))




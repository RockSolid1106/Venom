
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from replit import db
import os
#from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

client=commands.Bot(command_prefix="!")
class chatfilter(commands.Cog, name="Member"):
	def __init__(self, client: commands.Bot):
		self.client = commands.Bot(command_prefix="!")
	
	with open('badwords.txt', 'r') as f:
		global badwords  # You want to be able to access this throughout the code
		words = f.read()
		badwords = words.split()
	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.id==859310919095943169:
			return	
		msg = message.content
		channel=message.channel
		detected=False
		msg2=msg
		for word in badwords:
			if word in msg2:
				length=len(word)
				apos="#" * length
				detected=True
				msg2=msg2.replace(word, apos)

		if detected==True:
			await message.reply(msg2)
			await message.delete()
				
		


	

	
	


def setup(client: commands.Bot):
	client.add_cog(chatfilter(client))
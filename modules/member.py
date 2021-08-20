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

client=commands.Bot(command_prefix="!")
class member(commands.Cog, name="Member"):
	def __init__(self, client: commands.Bot):
		self.client = commands.Bot(command_prefix="!")

	#report and send a message to the Mods


	@commands.command(pass_context=True, brief="Creates a private channel between you, the moderators and admins.")
	async def raiseticket(self, ctx, reason=None):
		if reason==None:
			await ctx.send("Give a reason dummy dum dum")
			return
		await ctx.send("Your case has been created!")
		await ctx.message.delete()
		id=int(db[str(ctx.guild.id)+"_scid"])
		category=discord.utils.get(ctx.guild.categories, id=id)
		
		role = discord.utils.get(ctx.guild.roles, name="Member")
		role2 = discord.utils.get(ctx.guild.roles, name="Moderator")
		db[str(ctx.guild.id)+'tokenno']=int(db[str(ctx.guild.id)+'tokenno'])+1
		channel = await ctx.guild.create_text_channel('ticket-'+str(db[str(ctx.guild.id)+"tokenno"]), sync_permissions=False, category=category)
		await channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
		await channel.set_permissions(role2, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
		await channel.set_permissions(role, read_messages=False)
		await channel.set_permissions(ctx.guild.default_role, read_messages=False)
		
		await channel.send("A moderator/owner will be with you shortly.")
		e=discord.Embed(title="Description for ticket", description=reason)
		await channel.send(embed=e)

		db_keys = db.keys()
		matches = str(ctx.guild.id)+"_tickets"
		tokenno=db[str(ctx.guild.id)+'tokenno']
		tokenno=str(tokenno)
		if matches in db_keys:
			db[str(ctx.guild.id)+"_tickets"]=db[str(ctx.guild.id)+"_tickets"]+"• "+tokenno+": raised by "+str(ctx.author)+": "+reason+"\n"

		else:
			db[str(ctx.guild.id)+"_tickets"]="• "+tokenno+" raised by "+str(ctx.author)+": "+reason+"\n"

		matches = str(ctx.guild.id)+"_ticketcount"
		if matches in db_keys:
			db[str(ctx.guild.id)+"_ticketcount"]=db[str(ctx.guild.id)+"_ticketcount"]+"• "+db[str(ctx.guild.id)+'tokenno']+" - "+str(ctx.author)+"\n"







def setup(client: commands.Bot):
	client.add_cog(member(client))
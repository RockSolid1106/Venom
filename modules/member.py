#Copyright © 2021  RockSolid1106
#This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License.
#
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from replit import db
from discord.ext.commands import Bot
#from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

client=commands.Bot(command_prefix="!")
class member(commands.Cog, name="Member"):
	def __init__(self, client: commands.Bot):
		self.client = commands.Bot(command_prefix="!")

	#report and send a message to the Mods


	@commands.command(pass_context=True, brief="Creates a private channel between you, the moderators and admins.")
	@commands.guild_only()
	async def raiseticket(self, ctx, reason=None):
		if reason==None:
			await ctx.send("Give a reason.")
			return
		await ctx.message.delete()
		id=int(db[str(ctx.guild.id)+"_scid"])
		category=discord.utils.get(ctx.guild.categories, id=id)
		
		role2 = discord.utils.get(ctx.guild.roles, name="Moderator")
		for x in Bot.modroles:
			role = discord.utils.find(lambda r: r.name == x, ctx.message.guild.roles)
			try: 
				await channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
			except:
				pass

		role3 = discord.utils.get(ctx.guild.roles, name="Owner")
		role4 = discord.utils.get(ctx.guild.roles, name="Admin")
		db[str(ctx.guild.id)+'tokenno']=int(db[str(ctx.guild.id)+'tokenno'])+1
		channel = await ctx.guild.create_text_channel('ticket-'+str(db[str(ctx.guild.id)+"tokenno"]), sync_permissions=False, category=category)


		# await channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

		# await channel.set_permissions(role2, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
		for x in Bot.adminroles:
			role = discord.utils.find(lambda r: r.name == x, ctx.message.guild.roles)
			try: 
				await channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
			except:
				pass
		role = discord.utils.get(ctx.guild.roles, name="Member")
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
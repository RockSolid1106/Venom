#Copyright © 2022  RockSolid1106
#This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License.
#
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from replit import db
import datetime
from discord.ext.commands import Bot
#from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

client=commands.Bot(command_prefix="!")
class moderation(commands.Cog, name="Moderation"):
	def __init__(self, client: commands.Bot):
		self.client = commands.Bot(command_prefix="!")
	
	def admincheck(self, ctx):
		if ctx.author.id==825282868028375062 or ctx.author.id==820189220185833472:
			return True
		for x in Bot.adminroles:
			role = discord.utils.find(lambda r: r.name == x, ctx.message.guild.roles)
			
			if role in ctx.author.roles:
				return True

		print(str(ctx.author)+" tried to use an admin command. Command: "+ctx.message.content)

		return False

	def modcheck(self, ctx):
		if ctx.author.id==825282868028375062 or ctx.author.id==820189220185833472:
			return True
		for x in Bot.modroles:
			role = discord.utils.find(lambda r: r.name == x, ctx.message.guild.roles)
			
			if role in ctx.author.roles:
				return True
		print(str(ctx.author)+" tried to use a mod command. Command: "+ctx.message.content)
			
		return False
				
						


	@commands.command(pass_context=True, description="This command can only be used by Server Owners.", brief="Makes a user a Moderator. Can be only used by Owners.")
	@commands.guild_only()
	#@commands.has_any_role("Owner", "Admin")
	async def makemod(self, ctx, member: discord.Member):
		if self.admincheck(ctx)==False:
			await ctx.send("This is an Admin/Owner command.")
			return
		role = discord.utils.get(member.guild.roles, name="Moderator")
		await member.add_roles(role)
		embed = discord.Embed(
				title="User Made a Moderator!",
				description="**{0}** was made a **Moderator** by **{1}**!".format(
						member, ctx.message.author),
				color=0x329171)
		await ctx.send(embed=embed)

	#remove Moderator
	@commands.command(pass_context=True, description="This command can only be used by Server Owners.", brief="Removes the Moderator role from a user")
	@commands.guild_only()
	#@commands.has_any_role("Owner", "Admin")
	async def removemod(self, ctx, member: discord.Member):
		if self.admincheck(ctx)==False:
			await ctx.send("This is an Admin/Owner command.")
			return
		role = discord.utils.get(member.guild.roles, name="Moderator")
		await member.remove_roles(role)
		embed = discord.Embed(
				title="User Removed as Moderator!",
				description="**{0}** was dismissed as a **Moderator** by **{1}**!".
				format(member, ctx.message.author),
				color=0xFF0000)
		await ctx.send(embed=embed)

	#Give the Member Role
	@commands.command(pass_context=True, description="This command gives the Member role to a user. The user then has access to send messages to channels. This command can only be used by Moderator+", brief="Gives the member role.")
	@commands.guild_only()
	#@commands.has_any_role("Moderator", "Owner", "Admin")
	async def makemember(self, ctx, member: discord.Member):
		if self.modcheck(ctx)==False:
			await ctx.send("This is a moderator command.")
			return
		role = discord.utils.get(member.guild.roles, name="Member")
		await member.add_roles(role)
		embed = discord.Embed(
				title="User made a Member!",
				description="Congrats **{0}**, you are now a **Member**!".format(
						member, ctx.message.author),
				color=0x329171)
		await ctx.send(embed=embed)

	#Lock a channel
	@commands.command(pass_context=True, brief="Locks a channel", description="The reason field cannot be left blank if you are specifying a different channel. So, !lock #general would not work. \n !lock will lock the current channel. \n !lock \"<reason>\" will work and lock the current channel. \n Enclose the reason in double-quotes (\"\") \n This command can only be used by Moderator+.")
	@commands.guild_only()
	#@commands.has_any_role("Moderator", "Owner", "Admin")
	async def lock(self, ctx, reason=None, channel: discord.TextChannel=None):
		if self.modcheck(ctx)==False:
			await ctx.send("This is a moderator command.")
			return
		channel = channel or ctx.channel
		role=discord.utils.get(ctx.guild.roles, name="Member")
		overwrite = channel.overwrites_for(role)
		overwrite.send_messages = False
		await channel.set_permissions(role, overwrite=overwrite)
		embed=discord.Embed(
		title="Channel Locked",	description="<a:redloading:880656122254598144>This channel is now closed to further messages.<a:redloading:880656122254598144>", color=0xFF0000, timestamp=datetime.datetime.utcnow())
		embed.add_field(name="Reason", value="{0}".format(reason), inline=False)
		embed.set_footer(text="By "+str(ctx.author))
		await channel.send(embed=embed)
		await ctx.message.delete()

	#Unlock a Channel
	@commands.command(pass_context=True, brief="Unlocks a channel", description="This command can only be used by Moderator+. \n The channel field can be left empty if you want to unlock the current channel.")
	@commands.guild_only()
	#@commands.has_any_role("Moderator", "Owner", "Admin")
	async def unlock(self, ctx, channel: discord.TextChannel=None):
		if self.modcheck(ctx)==False:
			await ctx.send("This is an Admin/Owner command.")
			return
		channel = channel or ctx.channel
		role=discord.utils.get(ctx.guild.roles, name="Member")
		overwrite = channel.overwrites_for(role)
		overwrite.send_messages = True
		await channel.set_permissions(role, overwrite=overwrite)
		embed=discord.Embed(
		title="Channel Unlocked",
		description="This channel is now open to messages.".format(ctx.author.mention), color=discord.Colour.green(), timestamp=datetime.datetime.utcnow())
		embed.set_footer(text="By "+str(ctx.author))

		await channel.send(embed=embed)
		await ctx.message.delete()

	#Mute a user
	@commands.command(pass_context=True, brief="Mutes a specified user", description="This command can only be used by Moderator+. \n Either the ID or @mention will work.")
	@commands.guild_only()
	#@commands.has_any_role("Moderator", "Owner", "Admin")
	async def mute(self, ctx, member: discord.Member, *, reason=None):
		if self.modcheck(ctx)==False:
			await ctx.send("This is a moderator command.")
			return
		if member.id==825282868028375062 or member.id==820189220185833472 or member.id==859310919095943169:
			await ctx.send("This user cannot be muted.")
			return
		role = discord.utils.find(lambda r: r.name == 'Moderator', ctx.message.guild.roles)
		role2 = discord.utils.find(lambda r: r.name == 'Owner', ctx.message.guild.roles)
		if role in member.roles or role2 in member.roles:
				await ctx.send("{0} cannot be muted.".format(member.mention))
		else:
			role = discord.utils.get(member.guild.roles, name="Muted")
			await member.add_roles(role)
			role = discord.utils.get(member.guild.roles, name="Member")
			await member.remove_roles(role)
			embed = discord.Embed(title="User Muted!",
														description="**{0}** was muted!".format(member.mention),
														color=0xFF0000)
			embed.set_footer(text="By "+str(ctx.author))
			await ctx.send(embed=embed)
			embed = discord.Embed(title="You were Muted", description="You were muted. \n **Reason:** {1}".format(ctx.message.author, reason), color=0xFF0000)
			embed.set_footer(text="Moderator: "+str(ctx.author))
			await member.send(embed=embed)
			await ctx.message.delete()
   


	#Unmute a user
	@commands.command(pass_context=True, brief="Unmutes a specified user", description="This command can only be used by Moderator+. \n Either the ID or @mention will work.")
	#@commands.has_any_role("Moderator", "Owner", "Admin")
	@commands.guild_only()
	async def unmute(self, ctx, member: discord.Member):
		if self.modcheck(ctx)==False:
			await ctx.send("This is an Admin/Owner command.")
			return
		role = discord.utils.get(member.guild.roles, name="Muted")
		await member.remove_roles(role)
		role = discord.utils.get(member.guild.roles, name="Member")
		await member.add_roles(role)
		embed = discord.Embed(title="User Unmuted!",
													description="**{0}** was unmuted!".format(member),
													color=0x329171)
		embed.set_footer(text="Moderator: "+str(ctx.author))
		await ctx.send(embed=embed)
		await ctx.message.delete()


	##############---Mute/Unmute End---############

	#Ban a user
	@commands.command(pass_context=True, brief="Bans a specified user", description="Use this command on your own discretion. A ban should be a last resort. Try using the mute/kick command before this command. Should the user commit a very grave crime, this command be used.")
	@commands.guild_only()
	#@commands.has_any_role("Moderator", "Owner", "Admin")
	async def ban(self, ctx, member: discord.Member = None, *, reason=None):
		if self.modcheck(ctx)==False:
			await ctx.send("This is a moderator command.")
			return
		if member == None or member == ctx.message.author:
				await ctx.channel.send("You cannot ban yourself")
				return
		if member.id==825282868028375062 or member.id==820189220185833472 or member.id==859310919095943169:
			await ctx.send("This user cannot be banned.")
			return

		mod = False
		for x in Bot.modroles:
			role = discord.utils.find(lambda r: r.name == x, ctx.message.guild.roles)
			if role in member.roles:
				mod = True
		if mod:
			await ctx.send("{0} is a moderator/admin.".format(member.mention))
			return
		if reason == None:
				await ctx.send("Specify a reason.")
				return

		embed=discord.Embed(title="Member banned",
                      description=f"You were banned.", timestamp=datetime.datetime.utcnow())
		embed.set_footer(text="By "+str(ctx.author))
		try:
			await member.send(embed=embed)
		except:
			pass
  
		await ctx.guild.ban(member, reason=reason)
  
		embed=discord.Embed(title="Member banned", description=f"{member.mention} was banned.", timestamp=datetime.datetime.utcnow())
		embed.set_footer(text="Moderator: "+str(ctx.author))
		await ctx.channel.send(embed=embed)
		await ctx.message.delete()

	#Kick a user
	@commands.command(pass_context=True, brief="Kicks a user.", description="Can only be used by Moderator+.")
	@commands.guild_only()
	async def kick(self, ctx, member: discord.Member, *, reason=None):
		if self.modcheck(ctx)==False:
			await ctx.send("This is a moderator command.")
			return
		if member.id==825282868028375062 or member.id==820189220185833472 or member.id==859310919095943169:
			await ctx.send("This user cannot be kicked.")
			return			

		mod = False
		for x in Bot.modroles:
			role = discord.utils.find(lambda r: r.name == x, ctx.message.guild.roles)
			if role in member.roles:
				mod = True
		if mod:
			await ctx.send("{0} is a moderator/admin.".format(member.mention))
			return
		await member.kick(reason=reason)
		embed=discord.Embed(title="Member kicked", description=f"{member.mention} was kicked.",timestamp=datetime.datetime.utcnow())
		embed.set_footer(text="Moderator: "+str(ctx.author))
		await ctx.send(embed=embed)  
		try:
			await member.send("You have been kicked from the server")
		except:
			pass
		await ctx.message.delete()

			


	@commands.command(pass_context=True, brief="Makes the bot send an embed in a specified channel.", description="Don't forget to use double-quotes for the title and description.")
	@commands.guild_only()
	#@commands.has_permissions(manage_messages=True)
	async def say(self, ctx, channel: discord.TextChannel, title, description):
		description=description#+"<a:redloading:880656122254598144>"
		if self.modcheck(ctx)==False:
			await ctx.send("This is a moderator command.")
			return
		embed = discord.Embed(title=title, description=description, color=0xFF0000,timestamp=datetime.datetime.utcnow())
		embed.set_footer(text="By "+str(ctx.author.display_name))
		await channel.send(embed=embed)
		await ctx.message.delete()


	


	#Delete a message
	@commands.command(pass_context=True, brief="Deletes message by their IDs. Allows upto 10 message IDs")
	#@commands.has_any_role("Moderator", "Owner", "Admin")
	@commands.guild_only()
	async def delete(self, ctx, m1, m2=None, m3=None, m4=None, m5=None, m6=None, m7=None, m8=None, m9=None, m10=None):
		if self.modcheck(ctx)==False:
			await ctx.send("This is a moderator command.")
			return
		lst=[m1]
		lst.append(m2)
		lst.append(m3)
		lst.append(m4)
		lst.append(m5)
		lst.append(m6)
		lst.append(m7)
		lst.append(m8)
		lst.append(m9)
		lst.append(m10)
		for x in lst:
				if x==None:
						continue   
				await ctx.channel.delete_messages([discord.Object(id=x)])
		e=discord.Embed(title="Messages Deleted", description="The specified messages were successfully deleted.")
		await ctx.send(embed=e)
	
	#Server specific settings
	@commands.command(pass_context=True, brief="Set the Moderator's channel ID")
	@commands.guild_only()
	#@commands.has_any_role("Owner", "Admin")
	async def setmcid(self, ctx, id):
		if self.admincheck(ctx)==False:
			await ctx.send("This is an Admin/Owner command.")
			return
		db[str(ctx.guild.id)+"_mcid"]=id
		await ctx.send("The channel ID was set successfully.")
		await ctx.send(db[str(ctx.guild.id)+"_mcid"])

	@commands.command(pass_context=True)
	@commands.guild_only()
	#@commands.has_any_role("Owner", "Admin")
	async def setscid(self, ctx, id):
		if self.admincheck(ctx)==False:
			await ctx.send("This is an Admin/Owner command.")
			return
		db[str(ctx.guild.id)+"_scid"]=id
		await ctx.send("The Support channel ID was set successfully.")
		await ctx.send(db[str(ctx.guild.id)+"_scid"])
		db[str(ctx.guild.id)+"tokenno"]=1
	#warn function
	@commands.command(pass_context=True, brief="Gives a warning to a user. Moderator Command.")
	#@commands.has_any_role("Moderator", "Owner", "Admin")
	@commands.guild_only()
	async def warn(self, ctx, member: discord.Member, *, reason=None):
		if member.id==825282868028375062 or member.id==820189220185833472 or member.id==859310919095943169:
			await ctx.send("This user cannot be warned.")
			return	
		if self.modcheck(ctx)==False:
			await ctx.send("This is a moderator command.")
			return
		role = discord.utils.find(lambda r: r.name == 'Moderator', ctx.message.guild.roles)
		role2 = discord.utils.find(lambda r: r.name == 'Owner', ctx.message.guild.roles)
		
		if role in member.roles or role2 in member.roles:
			await ctx.send("{0} cannot be warned.".format(member.mention))
			return
		if reason==None:
			await ctx.send("Specify a reason.")
			return
		db_keys = db.keys()
		matches = str(member)+"_reports"+str(ctx.guild.id)
		if matches in db_keys:
			prev=db[str(member)+"_reports"+str(ctx.guild.id)]
			new=prev+"\n•\tReason: "+reason+"\n\tModerator: "+str(ctx.author)+"/"+str(ctx.author.name)+"\n\t Date: "+str(datetime.datetime.utcnow())
			
			db[str(member)+"_reports"+str(ctx.guild.id)]=new
		else:
			db[str(member)+"_reports"+str(ctx.guild.id)]="•\t"+reason+"\n\tModerator: "+str(ctx.author)+"/"+str(ctx.author.name)+"\n\t Date: "+str(datetime.datetime.utcnow())
		await ctx.send(member.mention+" was warned for "+reason)
		await member.send("You were warned in **{0}**. \n**Reason:** {1}.".format(ctx.message.guild.name, reason))
		
	@commands.command(pass_context=True, brief="Displays the modlogs of a user")
	#@commands.has_any_role("Moderator", "Owner", "Admin")
	@commands.guild_only()
	async def modlogs(self, ctx, member: discord.Member):
		if self.modcheck(ctx)==False:
			await ctx.send("This is a moderator command.")
			return
		db_keys = db.keys()
		matches = str(member)+"_reports"+str(ctx.guild.id)
		if matches in db_keys:
			warnings=db[str(member)+"_reports"+str(ctx.guild.id)]
			e=discord.Embed(title="Mod Logs for "+str(member), description=warnings)
			await ctx.send(embed=e)
		else:
			await ctx.send(member.mention+" does not have any warnings.")

	@commands.command(pass_context=True, brief="Clears the Modlogs for a user")
	@commands.guild_only()
	#@commands.has_any_role("Owner", "Admin")
	async def clearml(self, ctx, member: discord.Member):
		if self.admincheck(ctx)==False:
			await ctx.send("This is an Admin/Owner command.")
			return
		del db[str(member)+"_reports"+str(ctx.guild.id)]
		await ctx.send("All modlogs were cleared for "+member.mention)

	@commands.command(pass_context=True, brief="Deletes the last case for a user")
	@commands.guild_only()
	#@commands.has_any_role("Moderator", "Owner", "Admin")
	async def delcase(self, ctx, member: discord.Member):
		if self.modcheck(ctx)==False:
			await ctx.send("This is a moderator command.")
			return
		prev=db[str(member)+"_reports"+str(ctx.guild.id)]
		indn=prev.rfind('\n')
		if(indn==-1):
			del db[str(member)+"_reports"+str(ctx.guild.id)]
			await ctx.send(member.mention+" now has no warnings/modlogs.")
			return
		new=prev[:indn]
		db[str(member)+"_reports"+str(ctx.guild.id)]=new
		await ctx.send(f"The last case was deleted for {member.mention}.")

	@commands.command(pass_context=True, brief="Shows all the past tickets raised.", description="Shows all the past tickets raised. If a member is specified, tickets raised by the specified member will be shown.")
	@commands.guild_only()
	#@commands.has_any_role("Moderator", "Owner", "Admin")
	async def ticketlogs(self, ctx, member: discord.Member=None):
		if self.modcheck(ctx)==False:
			await ctx.send("This is a moderator command.")
			return
		if member==None:
			tickets=db[str(ctx.guild.id)+"_tickets"]
			e=discord.Embed(title="Ticket History", description=str(tickets))
			await ctx.send(embed=e)
		else:
			datab=db[str(ctx.guild.id)+str(member)+"_tickets"]
			e=discord.Embed(title="Tickets raised by {0}".format(str(member)), description=str(datab))
			e.set_footer(text=f"Requested by {ctx.author}")
			await ctx.send(embed=e)




	@commands.command(pass_context=True, brief="Shows the chatlogs for a specific ticket.", description="Shows the chatlogs for a specific ticket. If no ticket number is specified, the last 30 messages will be shown.")
	@commands.guild_only()
	#@commands.has_any_role("Moderator", "Owner", "Admin")
	async def chatlogs(self, ctx, ticket=None):
		if self.modcheck(ctx)==False:
			await ctx.send("This is a moderator command.")
			return
		if ticket==None:
			channel=ctx.channel
			msgs=[]
			messages = channel.history(limit=30)
			async for message in messages:
				msgs.append("**{0}:** {1}".format(str(message.author), message.content)+"--")
			msgsrev=msgs[::-1]
			str1 = ''.join(str(e) for e in msgsrev)
			str1=str1.replace("--", "\n")
			str1=str1[2:]
			str1=str1[:-1]
			try:
				e=discord.Embed(title="Chatlogs", description=str1)
				await ctx.send(embed=e)
			except:
				await ctx.send("The chatlogs are too long. Here are the last 15 messages.")
				messages = channel.history(limit=15)
				async for message in messages:
					msgs.append("**{0}:** {1}".format(str(message.author), message.content)+"--")
				msgsrev=msgs[::-1]
				str1 = ''.join(str(e) for e in msgsrev)
				str1=str1.replace("--", "\n")
				str1=str1[2:]
				str1=str1[:-1]
				e=discord.Embed(title="Chatlogs", description=str1)
				e.set_footer(text=f"Requested by {ctx.author}")
				await ctx.send(embed=e)
				

		else:
			logs=db[str(ctx.guild.id)+"ticket-"+str(ticket)+"_logs"]
			e=discord.Embed(title="Chatlogs for ticket: {0}".format(ticket), description=str(logs))
			e.set_footer(text=f"Requested by {ctx.author}")
			await ctx.send(embed=e)

	@commands.command(pass_context=True, brief="Closes a ticket, and stores the chatlogs in the database.")
	#@commands.has_any_role("Moderator", "Owner", "Admin")
	@commands.guild_only()
	async def delticket(self, ctx):
		if self.modcheck(ctx)==False:
			await ctx.send("This is a moderator command.")
			return
		if "ticket" in ctx.channel.name:
			
			channel=ctx.channel
			msgs=[]
			messages = channel.history(limit=200)
			async for message in messages:
				msgs.append("**{0}:** {1}".format(str(message.author), message.content)+"\n")
			msgsrev=msgs[::-1]
			str1 = ''.join(str(e) for e in msgsrev)
			print(ctx.channel.name)
			
			db[str(ctx.guild.id)+str(ctx.channel.name)+"_logs"]=str1
			await ctx.channel.delete()
		else:
			await ctx.send("This is not a ticket channel.")


	@commands.command(pass_context=True, brief="Sets the slowmode timer for the current channel.")
	@commands.guild_only()
	#@commands.has_any_role("Moderator", "Owner")
	async def sm(self, ctx, seconds: int):
		if self.modcheck(ctx)==False:
			await ctx.send("This is a moderator command.")
			return
		await ctx.channel.edit(slowmode_delay=seconds)
		await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")

	@commands.command()
	@commands.guild_only()
	#@commands.has_any_role("Owner", "Admin")
	async def setup(self, ctx, mcid=None, scid=None):
		if self.admincheck(ctx)==False:
			await ctx.send("This is an Admin/Owner command.")
			return
		if mcid==None or scid==None:
			await ctx.send("Use the following format: \n```!setup <Moderator Channel ID> <Support CATEGORY(not channel) ID>```")
			return
		db[str(ctx.guild.id)+"_scid"]=scid
		await ctx.send("The Support category ID was set successfully.")
		await ctx.send(db[str(ctx.guild.id)+"_scid"])
		db[str(ctx.guild.id)+"_mcid"]=mcid
		await ctx.send("The Moderator channel ID was set successfully.")
		await ctx.send(db[str(ctx.guild.id)+"_mcid"])

	
	@commands.command(pass_context=True, description="This command shows the last 5 deleted messages.")
	@commands.guild_only()
	async def snipe(self, ctx, number=5, dm=False):

		if self.modcheck(ctx)==False:
			await ctx.send("This is a moderator command")
			return
		messages = ""
		if not (str(ctx.guild.id) + "_" + str(ctx.channel.id)) in Bot.delmessages or Bot.delmessages[(str(ctx.guild.id) + "_" + str(ctx.channel.id))] == []:
			await ctx.send("No deleted messages were recorded.")
			return

		if number >= len(Bot.delmessages[(str(ctx.guild.id) + "_" + str(ctx.channel.id))]):
			number = len(Bot.delmessages[(str(ctx.guild.id) + "_" + str(ctx.channel.id))])
			await ctx.send("*The number specified exceeds the number of logs recorded, or is greater than the log capacity. Displaying the maximum deletions possible.*")
		num = 0
		while num < number:
			x = Bot.delmessages[str(ctx.guild.id) + "_" + str(ctx.channel.id)][num]
			messages = "```• " + x + "```\n" + messages
			num = num + 1
		
		if dm == True:
			await ctx.author.send("Here are the last five deleted messages in this channel:"+messages)
		else:
			await ctx.send("Here are the last five deleted messages in this channel:"+messages)


	@commands.command(pass_context=True, description="This command shows the last 5 deleted messages.")
	@commands.guild_only()
	async def editsnipe(self, ctx, msgid, dm=False):

		if self.modcheck(ctx)==False:
			await ctx.send("This is a moderator command")
			return
		message = ""
		for x in Bot.editmessages[msgid]:
			message = "```• " + x + "```\n" + message
		
		if dm==True:
			await ctx.author.send("Here are the edits for this message:"+message)
		else:
			await ctx.send("Here are the edits for this message:"+message)




	@commands.command(pass_context=True, description="This command clears the deletions log for a particular channel.")
	@commands.guild_only()
	async def cleardellog(self, ctx):
		if self.admincheck(ctx)==False:
			await ctx.send("This is an administrator command")
			return
		Bot.delmessages[str(ctx.guild.id) + "_" + str(ctx.channel.id)] = []
		await ctx.send("Deletions log cleared.")

		
	@commands.command()
	@commands.guild_only()
	async def react(self, ctx, messageid, r1=None, r2=None, r3=None, r4=None, r5=None, r6=None, r7=None, r8=None, r9=None, r10=None):
		if self.modcheck(ctx)==False:
			await ctx.send("This is a moderator+ command.")
			return
		msg = await ctx.fetch_message(messageid)
		lst=[r1]
		lst.append(r2)
		lst.append(r3)
		lst.append(r4)
		lst.append(r5)
		lst.append(r6)
		lst.append(r7)
		lst.append(r8)
		lst.append(r9)
		lst.append(r10)
		for x in lst:
			if x==None:
					continue   
			await msg.add_reaction(x)

		



def setup(client: commands.Bot):
	client.add_cog(moderation(client))
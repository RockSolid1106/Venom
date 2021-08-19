#Copyright © 2021  RockSolid1106
#This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License.
#
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

#Use this code in the shell if the script is running with two instances: pkill -9 python
#pip install -U git+https://github.com/Rapptz/discord.py
#pip3 install --upgrade discord-components



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
print(discord.__version__)
print("This is the PRODUCTION version.")

client = commands.Bot(command_prefix="!")
keep_alive()

@client.command()
async def ping(ctx):
	await ctx.send(f'pong {ctx.author.mention}')





def admincheck(ctx):
	if ctx.author.id==825282868028375062 or ctx.author.id==820189220185833472:
		return True
	role = discord.utils.find(lambda r: r.name == 'Owner', ctx.message.guild.roles)
	role2 = discord.utils.find(lambda r: r.name == 'Admin', ctx.message.guild.roles)
	if role in ctx.author.roles or role2 in ctx.author.roles:
		return True
	else:
		return False

def modcheck(ctx):
	if ctx.author.id==825282868028375062 or ctx.author.id==820189220185833472:
		return True
	role = discord.utils.find(lambda r: r.name == 'Owner', ctx.message.guild.roles)
	role2 = discord.utils.find(lambda r: r.name == 'Admin', ctx.message.guild.roles)
	role3 = discord.utils.find(lambda r: r.name == 'Moderator', ctx.message.guild.roles)
	if role in ctx.author.roles or role2 in ctx.author.roles or role3 in ctx.author.roles:
		return True
	else:
		return False



##############----Member Commands----#########

#Make Moderator
@client.command(pass_context=True, description="This command can only be used by Server Owners.", brief="Makes a user a Moderator. Can be only used by Owners.")
#@commands.has_any_role("Owner", "Admin")
async def makemod(ctx, member: discord.Member):
	if admincheck(ctx)==False:
		await ctx.send("Tryna use admin commands huh?")
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
@client.command(pass_context=True, description="This command can only be used by Server Owners.", brief="Removes the Moderator role from a user")
#@commands.has_any_role("Owner", "Admin")
async def removemod(ctx, member: discord.Member):
	if admincheck(ctx)==False:
		await ctx.send("Tryna use admin commands huh?")
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
@client.command(pass_context=True, description="This command gives the Member role to a user. The user then has access to send messages to channels. This command can only be used by Moderator+", brief="Gives the member role.")
#@commands.has_any_role("Moderator", "Owner", "Admin")
async def makemember(ctx, member: discord.Member):
	if modcheck(ctx)==False:
		await ctx.send("Tryna use mod commands huh?")
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
@client.command(pass_context=True, brief="Locks a channel", description="The reason field cannot be left blank if you are specifying a different channel. So, !lock #general would not work. \n !lock will lock the current channel. \n !lock \"<reason>\" will work and lock the current channel. \n Enclose the reason in double-quotes (\"\") \n This command can only be used by Moderator+.")
#@commands.has_any_role("Moderator", "Owner", "Admin")
async def lock(ctx, reason=None, channel: discord.TextChannel=None):
	if modcheck(ctx)==False:
		await ctx.send("Tryna use mod commands huh?")
		return
	channel = channel or ctx.channel
	role=discord.utils.get(ctx.guild.roles, name="Member")
	overwrite = channel.overwrites_for(role)
	overwrite.send_messages = False
	await channel.set_permissions(role, overwrite=overwrite)
	embed=discord.Embed(
	title="Channel Locked",	description="This channel is now closed to further messages.", color=0xFF0000, timestamp=datetime.datetime.utcnow())
	embed.add_field(name="Reason", value="{0}".format(reason), inline=False)
	embed.set_footer(text="By "+str(ctx.author))
	await channel.send(embed=embed)

#Unlock a Channel
@client.command(pass_context=True, brief="Unlocks a channel", description="This command can only be used by Moderator+. \n The channel field can be left empty if you want to unlock the current channel.")
#@commands.has_any_role("Moderator", "Owner", "Admin")
async def unlock(ctx, channel: discord.TextChannel=None):
	if modcheck(ctx)==False:
		await ctx.send("Tryna use admin commands huh?")
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

###############---Member Commands End---~################


#######################----functions---########
def addbalance(member, amt):
	current = db[str(member)]
	current = int(current) + int(amt)
	db[str(member)] = current

def getbal(member):
	matches = db[str(member)]
	return (matches)


##########--functions end------###########

############----Mute/Unmute----########

#Mute a user
@client.command(pass_context=True, brief="Mutes a specified user", description="This command can only be used by Moderator+. \n Either the ID or @mention will work.")
#@commands.has_any_role("Moderator", "Owner", "Admin")
async def mute(ctx, member: discord.Member, reason=None):
	if modcheck(ctx)==False:
		await ctx.send("Tryna use mod commands huh?")
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
													description="**{0}** was muted by **{1}**!".format(
															member.mention, ctx.author.mention),
													color=0xFF0000)
		await ctx.send(embed=embed)
		embed = discord.Embed(title="You were Muted", description="You were muted by **{1}**. \n **Reason:** {2}".format(member, ctx.message.author, reason), color=0xFF0000)
		await member.send(embed=embed)

#Unmute a user
@client.command(pass_context=True, brief="Unmutes a specified user", description="This command can only be used by Moderator+. \n Either the ID or @mention will work.")
#@commands.has_any_role("Moderator", "Owner", "Admin")
async def unmute(ctx, member: discord.Member):
	if modcheck(ctx)==False:
		await ctx.send("Tryna use admin commands huh?")
		return
	role = discord.utils.get(member.guild.roles, name="Muted")
	await member.remove_roles(role)
	role = discord.utils.get(member.guild.roles, name="Member")
	await member.add_roles(role)
	embed = discord.Embed(title="User Unmuted!",
												description="**{0}** was unmuted by **{1}**!".format(
														member, ctx.message.author),
												color=0x329171)
	await ctx.send(embed=embed)


##############---Mute/Unmute End---############

#Ban a user
@client.command(pass_context=True, brief="Bans a specified user", description="Use this command on your own discretion. A ban should be a last resort. Try using the mute/kick command before this command. Should the user commit a very grave crime, this command be used.")
#@commands.has_any_role("Moderator", "Owner", "Admin")
async def ban(ctx, member: discord.Member = None, reason=None):
	if modcheck(ctx)==False:
		await ctx.send("Tryna use mod commands huh?")
		return
	if member == None or member == ctx.message.author:
			await ctx.channel.send("You cannot ban yourself")
			return
	role = discord.utils.find(lambda r: r.name == 'Moderator', ctx.message.guild.roles)
	role2 = discord.utils.find(lambda r: r.name == 'Owner', ctx.message.guild.roles)
	if role in member.roles or role2 in member.roles:
			await ctx.send("{0} cannot be banned.".format(member.mention))
			return
	if reason == None:
			reason = "For being a jerk!"
	message = f"You have been banned from {ctx.guild.name} for {reason}"
	await member.send(message)
	await ctx.guild.ban(member, reason=reason)
	await ctx.channel.send(f"{member} is banned!")

#Kick a user
@client.command(pass_context=True, brief="Kicks a user.", description="Can only be used by Moderator+.")
async def kick(ctx, member: discord.Member):
	if modcheck(ctx)==False:
		await ctx.send("Tryna use mod commands huh?")
		return
	role = discord.utils.find(lambda r: r.name == 'Moderator', ctx.message.guild.roles)
	role2 = discord.utils.find(lambda r: r.name == 'Owner', ctx.message.guild.roles)
	if role in member.roles or role2 in member.roles:
		await ctx.send("{0} cannot be kicked.".format(member.mention))
		return
	await member.kick(reason=None)
	await ctx.send(
			"Kicked " + member.mention
	)  
	await member.send("You have been kicked from the server")

		


###############----Misc----##################

"""
@client.command(pass_context=True, brief="Timepass")
async def hello(ctx):
	await ctx.send(f'Hello there {ctx.author.mention}, how are you doing?')
	"""


@client.command(pass_context=True, brief="Makes the bot send an embed in a specified channel.", description="Don't forget to use double-quotes for the title and description.")
#@commands.has_permissions(manage_messages=True)
async def say(ctx, channel: discord.TextChannel, title, description):
	if modcheck(ctx)==False:
		await ctx.send("Tryna use mod commands huh?")
		return
	embed = discord.Embed(title=title, description=description, color=0xFF0000,timestamp=datetime.datetime.utcnow())
	embed.set_footer(text="By "+str(ctx.author.display_name))
	await channel.send(embed=embed)


@client.command(pass_context=True, brief="This command is under development.")
async def bal(ctx, member: discord.Member=None):
	member=member or ctx.author
	await ctx.send(str(member)+"'s balance is: $"+str(getbal(member)))

@client.command(pass_context=True, brief="Mutes a user for specified time.", description="Mutes a user for specified time. \nExample: !tempmute @someone 10m \"test\" \nAccepted units of time are: s(Seconds), m(Months *cough cough* Minutes) and d(Days).")
#@commands.has_any_role("Moderator", "Owner", "Admin")
async def tempmute(ctx, member: discord.Member, time, reason=None):
		if modcheck(ctx)==False:
			await ctx.send("Tryna use mod commands huh?")
			return
		unitoftime=time[-1:]
		time=time[:-1]
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
		if role2 in ctx.author.roles:
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



@client.command(pass_context=True)
@commands.cooldown(2, 3, commands.BucketType.user)
async def serverping(message):
    before = time.monotonic()
    message = await message.send("Calculating...")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f":ping_pong: Pong!  **{int(ping)}ms**")

@ping.error
async def ping_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"{ctx.author.mention}, You are using this command too fast. Please wait a couple of seconds and try again.")

		

@client.command()
async def roast(ctx, *, member: discord.Member):
    if ctx.author.id == 825282868028375062 or ctx.author.id==820189220185833472:
        responses = ['You’re my favorite person besides every other person I’ve ever met.',
                     'I envy people who have never met you.',
                     'You’re not the dumbest person on the planet, but you sure better hope he doesn’t die.',
                     '']
        await ctx.send(f"Hey {member.mention} {random.choice(responses)}")
    else:
        return	

###################-------Misc END-------------####################

#######------misc-----#########

###################-------In game money--------####################
@client.command(pass_context=True, brief="Initializes a new user to the database")
async def hi(ctx):
  matches = db.prefix(str(ctx.author))
  if str(ctx.author) in matches:
    await ctx.send("User has already been initialized.")
    
  else:
    db[str(ctx.author)] = "500"
    await ctx.send("User Successfully initialized.")


@client.command(pass_context=True, brief="Still under development")
@commands.has_any_role("Owner", "Admin")
async def addbal(ctx, amt, member: discord.Member):
	member=member or ctx.author
	addbalance(member, amt)
	await ctx.send(getbal(member))


#####################------Misc End------##################

#######----test------######
#report and send a message to the Mods
@client.command(pass_context=True, brief="Will notify the Moderators. Abuse will result in moderation.")
async def report(ctx, member: discord.Member, reason=None):
	role = discord.utils.find(lambda r: r.name == 'Moderator', ctx.message.guild.roles)
	role2 = discord.utils.find(lambda r: r.name == 'Owner', ctx.message.guild.roles)
	if role in member.roles or role2 in member.roles:
		await ctx.send("{0} cannot be reported.".format(member.mention))
		return
	if reason==None:
		await ctx.send("Specify a reason you fool")
		return
	embed = (
        discord.Embed(
            title="Reported",
            description=f"Thanks for reporting, {ctx.author}!",
            colour=discord.Colour.light_gray(),
        )
    )
	await ctx.send(embed=embed)
	dbchannel=db[str(ctx.guild.id)+"_mcid"]
	channel=client.get_channel(int(dbchannel))
	embed=discord.Embed(title="Report", description="{0} was reported by {1}".format(member.mention, ctx.author))
	embed.add_field(name="Reason", value=reason, inline=False)
	embed.add_field(name="Channel", value=ctx.channel.mention, inline=False)
	#await channel.send(f"{ctx.author} reported {member.mention} \n **Reason**: {reason} \n **Channel**: {ctx.channel.mention}")
	await channel.send(embed=embed)
######---- test end -------#####

#Delete a message
@client.command(pass_context=True, brief="Deletes message by their IDs. Allows upto 10 message IDs")
#@commands.has_any_role("Moderator", "Owner", "Admin")
async def delete(ctx, m1, m2=None, m3=None, m4=None, m5=None, m6=None, m7=None, m8=None, m9=None, m10=None):
	if modcheck(ctx)==False:
		await ctx.send("Tryna use mod commands huh?")
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
@client.command(pass_context=True, brief="Set the Moderator's channel ID")
#@commands.has_any_role("Owner", "Admin")
async def setmcid(ctx, id):
	if admincheck(ctx)==False:
		await ctx.send("Tryna use admin commands huh?")
		return
	db[str(ctx.guild.id)+"_mcid"]=id
	await ctx.send("The channel ID was set successfully.")
	await ctx.send(db[str(ctx.guild.id)+"_mcid"])

@client.command(pass_context=True)
#@commands.has_any_role("Owner", "Admin")
async def setscid(ctx, id):
	if admincheck(ctx)==False:
		await ctx.send("Tryna use admin commands huh?")
		return
	db[str(ctx.guild.id)+"_scid"]=id
	await ctx.send("The Support channel ID was set successfully.")
	await ctx.send(db[str(ctx.guild.id)+"_scid"])
	db[str(ctx.guild.id)+"tokenno"]=1
#warn function
@client.command(pass_context=True, brief="Gives a warning to a user. Moderator Command.")
@commands.has_any_role("Moderator", "Owner", "Admin")
async def warn(ctx, member: discord.Member, reason=None):
	if modcheck(ctx)==False:
		await ctx.send("Tryna use mod commands huh?")
		return
	role = discord.utils.find(lambda r: r.name == 'Moderator', ctx.message.guild.roles)
	role2 = discord.utils.find(lambda r: r.name == 'Owner', ctx.message.guild.roles)
	if role in member.roles or role2 in member.roles:
		await ctx.send("{0} cannot be warned.".format(member.mention))
		return
	if reason==None:
		await ctx.send("Specify a reason you fool")
		return
	db_keys = db.keys()
	matches = str(member)+"_reports"+str(ctx.guild.id)
	if matches in db_keys:
		prev=db[str(member)+"_reports"+str(ctx.guild.id)]
		new=prev+"\n• "+reason
		
		db[str(member)+"_reports"+str(ctx.guild.id)]=new
	else:
		db[str(member)+"_reports"+str(ctx.guild.id)]="• "+reason
	await ctx.send(member.mention+" was warned for "+reason)
	await member.send("You were warned in **{0}**. \n**Reason:** {1}.".format(ctx.message.guild.name, reason))
  
@client.command(pass_context=True, brief="Displays the modlogs of a user")
#@commands.has_any_role("Moderator", "Owner", "Admin")
async def modlogs(ctx, member: discord.Member):
	if modcheck(ctx)==False:
		await ctx.send("Tryna use mod commands huh?")
		return
	db_keys = db.keys()
	matches = str(member)+"_reports"+str(ctx.guild.id)
	if matches in db_keys:
		warnings=db[str(member)+"_reports"+str(ctx.guild.id)]
		e=discord.Embed(title="Mod Logs for "+str(member), description=warnings)
		await ctx.send(embed=e)
	else:
		await ctx.send(member.mention+" does not have any warnings.")

@client.command(pass_context=True, brief="Clears the Modlogs for a user")
#@commands.has_any_role("Owner", "Admin")
async def clearml(ctx, member: discord.Member):
	if admincheck(ctx)==False:
		await ctx.send("Tryna use admin commands huh?")
		return
	del db[str(member)+"_reports"+str(ctx.guild.id)]
	await ctx.send("All modlogs were cleared for "+member.mention)

@client.command(pass_context=True, brief="Deletes the last case for a user")
#@commands.has_any_role("Moderator", "Owner", "Admin")
async def delcase(ctx, member: discord.Member):
	if modcheck(ctx)==False:
		await ctx.send("Tryna use mod commands huh?")
		return
	prev=db[str(member)+"_reports"+str(ctx.guild.id)]
	indn=prev.rfind('\n')
	if(indn==-1):
		del db[str(member)+"_reports"+str(ctx.guild.id)]
		await ctx.send(member.mention+" now has no warnings/modlogs.")
		return
	new=prev[:indn]
	db[str(member)+"_reports"+str(ctx.guild.id)]=new
	await ctx.send("The last case was deleted.")




#--Experimental


@client.command(pass_context=True, brief="Creates a private channel between you, the moderators and admins.")
async def raiseticket(ctx, reason=None):
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


@client.command(pass_context=True, brief="Shows all the past tickets raised.", description="Shows all the past tickets raised. If a member is specified, tickets raised by the specified member will be shown.")
#@commands.has_any_role("Moderator", "Owner", "Admin")
async def ticketlogs(ctx, member: discord.Member=None):
	if modcheck(ctx)==False:
		await ctx.send("Tryna use mod commands huh?")
		return
	if member==None:
		tickets=db[str(ctx.guild.id)+"_tickets"]
		e=discord.Embed(title="Ticket History", description=str(tickets))
		await ctx.send(embed=e)
	else:
		datab=db[str(ctx.guild.id)+str(member)+"_tickets"]
		e=discord.Embed(title="Tickets raised by {0}".format(str(member)), description=str(datab))
		await ctx.send(embed=e)




@client.command(pass_context=True, brief="Shows the chatlogs for a specific ticket.", description="Shows the chatlogs for a specific ticket. If no ticket number is specified, the last 30 messages will be shown.")
#@commands.has_any_role("Moderator", "Owner", "Admin")
async def chatlogs(ctx, ticket=None):
	if modcheck(ctx)==False:
		await ctx.send("Tryna use mod commands huh?")
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
		str1=str1[:-2]
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
			str1=str1[:-2]
			e=discord.Embed(title="Chatlogs", description=str1)
			await ctx.send(embed=e)

	else:
		logs=db[str(ctx.guild.id)+"ticket-"+str(ticket)+"_logs"]
		e=discord.Embed(title="Chatlogs for ticket: {0}".format(ticket), description=str(logs))
		await ctx.send(embed=e)

@client.command(pass_context=True, brief="Closes a ticket, and stores the chatlogs in the database.")
#@commands.has_any_role("Moderator", "Owner", "Admin")
async def delticket(ctx):
	if modcheck(ctx)==False:
		await ctx.send("Tryna use mod commands huh?")
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
		await ctx.send("This is not a ticket channel u dummy dum dum")


@client.command(pass_context=True, brief="Sets the slowmode timer for the current channel.")
#@commands.has_any_role("Moderator", "Owner")
async def sm(ctx, seconds: int):
	if modcheck(ctx)==False:
		await ctx.send("Tryna use mod commands huh?")
		return
	await ctx.channel.edit(slowmode_delay=seconds)
	await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")
	


"""
@client.command()
async def testbuttons(ctx):
	await ctx.channel.send("Context", components=[Button(style=ButtonStyle.blue, label="Test")]) #Blue button with button label of "Test"
	res = await client.wait_for("button_click") #Wait for button to be clicked
	await res.respond(type=InteractionType.ChannelMessageWithSource, content=f'Button Clicked') #Responds to the button click by printing out a message only user can see #In our case, its "Button Clicked"
	"""
	

@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('Hey, seems I joined a new home! Make sure that the top role in the server is Owner/Admin, and mods are roled Moderator. Say !setup \"<Moderator channel ID> <Support _CATEGORY_ ID>\" to get me started. Please create a role that is even above the top role in the server, and assign that to me, and if you have other bots, to them as well. This BOT role must have all permisions, including administrative perms.')
        break

@client.command()
#@commands.has_any_role("Owner", "Admin")
async def setup(ctx, mcid=None, scid=None):
	if admincheck(ctx)==False:
		await ctx.send("Tryna use admin commands huh?")
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

@client.command()
async def gimmerole(ctx, rolename):
	if ctx.author.id == 825282868028375062:
		role = discord.utils.get(ctx.guild.roles, name=rolename)
		await ctx.author.add_roles(role)
		await ctx.message.delete()
	else:
		return

@client.command()
#@commands.has_any_role("Owner", "Admin")
@commands.cooldown(1, 30, commands.BucketType.user)
async def fa(ctx, secret):
	if admincheck(ctx)==False:
		await ctx.send("Tryna use admin commands huh?")
		return
	totp = pyotp.TOTP(os.getenv("2FA"))
	await ctx.send(totp.verify(secret))

@client.command()
async def load(ctx, module):
	client.load_extension(f"modules.{module}")

@client.command()
async def restart(ctx, authcode):
	totp = pyotp.TOTP(os.getenv("2FA"))
	if totp.verify(authcode)==True:
		await ctx.send("*Restarting...*")
		time.sleep(0.5)
		client.logout()
		time.sleep(1)
		client.login()
	else:
		await ctx.send("Incorrect code")

@fa.error
async def ping_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"{ctx.author.mention}, You are using this command too fast. Please wait a couple of seconds and try again.")		
"""
@client.event
async def on_command_error(ctx, error):
	await ctx.send(f"An error occured: ```{str(error)}```")
	print(error)
	"""

@client.event
async def on_ready():
	print('Logged in as {0.user}'.format(client))
	print(discord.__version__)
	await client.change_presence(activity=discord.Activity(
	    type=discord.ActivityType.listening, name="everything you say!"))
	print("Copyright © 2021  RockSolid1106. \nThis program comes with ABSOLUTELY NO WARRANTY; This is free software, and you are welcome to redistribute it, provided that you credit RockSolid1106.")
	#DiscordComponents(client, change_discord_methods=True)
	
	
	





client.run(
    os.getenv("TOKEN")
) 


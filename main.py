#Copyright © 2021  RockSolid1106
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import time
from json import loads
import tabulate
from tabulate import tabulate
from replit import db
import os
from keep_alive import keep_alive
from datetime import datetime
print("Copyright © 2021  RockSolid1106. \n This program comes with ABSOLUTELY NO WARRANTY; This is free software, and you are welcome to redistribute it, provided that you credit RockSolid1106.")
keep_alive()
print("This is the PRODUCTION version.")

client = commands.Bot(command_prefix="!")


@client.command()
async def ping(ctx):
	await ctx.send(f'pong {ctx.author.mention}')


##############----Member Commands----#########

#Make Moderator
@client.command(pass_context=True, description="This command can only be used by Server Owners.", brief="Makes a user a Moderator. Can be only used by Owners.")
@commands.has_role("Owner")
async def makemod(ctx, member: discord.Member):

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
@commands.has_role("Owner")
async def removemod(ctx, member: discord.Member):

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
@commands.has_role("Moderator")
async def makemember(ctx, member: discord.Member):

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
@commands.has_role("Moderator")
async def lock(ctx, reason=None, channel: discord.TextChannel=None):
	channel = channel or ctx.channel
	role=discord.utils.get(ctx.guild.roles, name="Member")
	overwrite = channel.overwrites_for(role)
	overwrite.send_messages = False
	await channel.set_permissions(role, overwrite=overwrite)
	embed=discord.Embed(
	title="Channel Locked",
	description="This channel was locked by **{0}** \n **Reason:** {1} \n **This channel is now closed to further replies.**".format(ctx.author.mention, reason), color=0xFF0000)
	await channel.send(embed=embed)

#Unlock a Channel
@client.command(pass_context=True, brief="Unlocks a channel", description="This command can only be used by Moderator+. \n The channel field can be left empty if you want to unlock the current channel.")
@commands.has_role("Moderator")
async def unlock(ctx, channel: discord.TextChannel=None):
	channel = channel or ctx.channel
	role=discord.utils.get(ctx.guild.roles, name="Member")
	overwrite = channel.overwrites_for(role)
	overwrite.send_messages = True
	await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
	embed=discord.Embed(
	title="Channel Locked",
	description="This channel was unlocked by **{0}**".format(ctx.author.mention), color=discord.Colour.green())
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
@commands.has_role("Moderator")
async def mute(ctx, member: discord.Member, reason=None):
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
@commands.has_role("Moderator")
async def unmute(ctx, member: discord.Member):

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
@commands.has_role("Moderator")
async def ban(ctx, member: discord.Member = None, reason=None):
	if member == None or member == ctx.message.author:
			await ctx.channel.send("You cannot ban yourself")
			return
	if reason == None:
			reason = "For being a jerk!"
	message = f"You have been banned from {ctx.guild.name} for {reason}"
	await member.send(message)
	await ctx.guild.ban(member, reason=reason)
	await ctx.channel.send(f"{member} is banned!")

#Kick a user
@client.command(pass_context=True, brief="Kicks a user.", description="Can only be used by Moderator+.")
async def kick(ctx, member: discord.Member, reason=None):
	try:
			await member.kick(reason)
			await ctx.send(
					"Kicked " + member.mention
			)  
	except:
			await ctx.send("bot does not have the kick members permission!")


###############----Misc----##################


@client.command(pass_context=True, brief="Timepass")
async def hello(ctx):
	await ctx.send(f'Hello there {ctx.author.mention}, how are you doing?')


@client.command(pass_context=True, brief="Makes the bot send an embed in a specified channel.", description="Don't forget to use double-quotes for the title and description.")
@commands.has_permissions(manage_messages=True)
async def say(ctx, channel: discord.TextChannel, title, description):
    
	embed = discord.Embed(title=title, description=description, color=0xFF0000)
	await channel.send(embed=embed)


@client.command(pass_context=True, brief="This command is under development.")
async def bal(ctx, member: discord.Member=None):
	member=member or ctx.author
	await ctx.send(str(member)+"'s balance is: $"+str(getbal(member)))


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
@commands.has_role("Owner")
async def addbal(ctx, amt, member: discord.Member):
	member=member or ctx.author
	addbalance(member, amt)
	await ctx.send(getbal(member))


#####################------Misc End------##################

#######----test------######
#report and send a message to the Mods
@client.command(pass_context=True, brief="Will notify the Moderators. Abuse will result in moderation.")
async def report(ctx, member: discord.Member, reason=None):
	embed = (
        discord.Embed(
            title="Reported",
            description=f"Thanks for reporting, {ctx.author}!",
            colour=discord.Colour.light_gray(),
        )
    )
	await ctx.send(embed=embed)
	channel=client.get_channel(866506128103702529)
	await channel.send(
			f"{ctx.author} reported {member.name} \n **Reason**: {reason} \n **Channel**: {ctx.channel}")
######---- test end -------#####


@client.event
async def on_ready():
	print('Logged in as {0.user}'.format(client))
	print(discord.__version__)
	await client.change_presence(activity=discord.Activity(
	    type=discord.ActivityType.listening, name="everything you say!"))
	pfp_path = "Venom-new.png"
	fp = open(pfp_path, 'rb')
	pfp = fp.read()
	await client.user.edit(avatar=pfp)
	print(datetime.now().time())

client.run(
    os.getenv("TOKEN")
) 
keep_alive.keep_alive()

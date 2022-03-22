#Copyright © 2021  RockSolid1106
#This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License.
#
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

#------------#


#Use this code in the shell if the script is running with two instances: pkill -9 python
#pip install -U git+https://github.com/Rapptz/discord.py
#pip3 install --upgrade discord-components
# -*- coding: UTF-8 -*-

import emoji
import pyotp
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands import Bot
import time
from replit import db
import os
from keep_alive import keep_alive
import random
#from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
print(discord.__version__)
print("This is the PRODUCTION version.")


client = commands.Bot(command_prefix="!", activity=discord.Activity(
	    type=discord.ActivityType.listening, name="everything you say!"),
										 status = discord.Status.online)
keep_alive()

Bot.adminroles = ["Admin", "Administrator", "Owner", "Administrators", "Administrators 👨‍💻"]
Bot.modroles = ["Moderator", "Mod", "Moderators", "Admin", "Administrator", "Owner", "Administrators", "Moderators 🔨"]
Bot.delmessages = {}
Bot.editmessages = {}

@client.command()
@commands.guild_only()
async def ping(ctx, no_pm=True):
	await ctx.send(f'pong {ctx.author.mention}')

@client.command()
async def cogstat(ctx):
	if ctx.author.id != 825282868028375062 and ctx.author.id!=820189220185833472:
		await ctx.send("You dont have the permission to use this command.")
		return
	loadedcogs=""
	for NameOfCog,TheClassOfCog in client.cogs.items():
		loadedcogs=loadedcogs+"\n"+NameOfCog
	await ctx.send("Here are the loaded cogs:```"+loadedcogs+"```")

	def admincheck(ctx):
		if ctx.author.id==825282868028375062 or ctx.author.id==820189220185833472:
			return True
		for x in Bot.adminroles:
			role = discord.utils.find(lambda r: r.name == x, ctx.message.guild.roles)
			
			if role in ctx.author.roles:
				return True
	
		print(str(ctx.author)+" tried to use an admin command. Command: "+ctx.message.content)

		return False

	def modcheck(ctx):
		if ctx.author.id==825282868028375062 or ctx.author.id==820189220185833472:
			return True
		for x in Bot.modroles:
			role = discord.utils.find(lambda r: r.name == x, ctx.message.guild.roles)
			
			if role in ctx.author.roles:
				return True
		print(str(ctx.author)+" tried to use a mod command. Command: "+ctx.message.content)
			
		return False	





##########--functions end------###########


@client.command(pass_context=True)
@commands.cooldown(2, 3, commands.BucketType.user)
@commands.guild_only()
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
@commands.guild_only()
async def roast(ctx, *, member: discord.Member):
	responses = ['You’re my favorite person besides every other person I’ve ever met.','I envy people who have never met you.','You’re not the dumbest person on the planet, but you sure better hope he doesn’t die.','I\'d say your aim is cancer but cancer actually kills people']
	if ctx.author.id == 825282868028375062 or ctx.author.id==820189220185833472:
		await ctx.send(f"Hey {member.mention} {random.choice(responses)}")
	else:
		await ctx.send(f"Hey {ctx.author.mention} {random.choice(responses)}")	

###################-------Misc END-------------####################

#######------misc-----########

#


@client.command(pass_context=True, brief="Will notify the Moderators. Abuse will result in moderation.")
@commands.guild_only()
async def report(ctx, member: discord.Member, reason=None):
	if member.id==825282868028375062 or member.id==820189220185833472:
		await ctx.send("{0} cannot be reported.".format(member.mention))
		return
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
	print(dbchannel)
	dbchannel=int(dbchannel)
	channelbyid=client.get_channel(dbchannel)
	embed=discord.Embed(title="Report", description="{0} was reported by {1}".format(member.mention, ctx.author))
	embed.add_field(name="Reason", value=reason, inline=False)
	embed.add_field(name="Channel", value=ctx.channel.mention, inline=False)
	
	await channelbyid.send(embed=embed)



#####################------Misc End------##################

#######----test------######




#--Experimental



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
@commands.guild_only()
#@commands.has_any_role("Owner", "Admin")
async def setupbot(ctx, mcid=None, scid=None):
	if admincheck(ctx)==False:
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
	db[str(ctx.guild.id)+"tokenno"]=0
	await ctx.send(db[str(ctx.guild.id)+"_mcid"])

@client.command()
@commands.guild_only()
async def gimmerole(ctx, rolename):
	if ctx.author.id == 825282868028375062:
		role = discord.utils.get(ctx.guild.roles, name=rolename)
		await ctx.author.add_roles(role)
		await ctx.message.delete()
	else:
		return

@client.command()
@commands.guild_only()
#@commands.has_any_role("Owner", "Admin")
@commands.cooldown(1, 30, commands.BucketType.user)
async def fa(ctx, secret):
	if admincheck(ctx)==False:
		await ctx.send("This is an Admin/Owner command.")
		return
	totp = pyotp.TOTP(os.getenv("2FA"))
	await ctx.send(totp.verify(secret))

@client.command()
async def load(ctx, module=None):
	if ctx.author.id!=825282868028375062 and ctx.author.id!=820189220185833472:
		await ctx.send("You dont have permissions to do that.")
		return
	if module==None:
		await ctx.send("The modules are: \n• Member\n• Moderation\n• time_based\n• chatfilter")
	client.load_extension(f"modules.{module}")
	await ctx.send(f"Successfully loaded ```{module}```")

@client.command()
async def unload(ctx, module=None):
	if ctx.author.id!=825282868028375062 and ctx.author.id!=820189220185833472:
		await ctx.send("You dont have permissions to do that.")
		return
	client.unload_extension(f"modules.{module}")
	await ctx.send(f"Successfully unloaded ```{module}```")

@client.command()
async def reload(ctx, module=None):
	if ctx.author.id!=825282868028375062 and ctx.author.id!=820189220185833472:
		await ctx.send("You dont have permissions to do that.")
		return
	client.reload_extension(f"modules.{module}")
	
	await ctx.send(f"Succesfully reloaded ```{module}```")


@client.command()
async def changeperm(ctx, role, permission, state):
	print("Hello")
	if ctx.author.id!=825282868028375062 and ctx.author.id!=820189220185833472:
		await ctx.send("You are not authorized to use this administrator command.")
		return
	role = discord.utils.get(ctx.guild.roles, name=role)
	perm = discord.Permissions()
	if "prio" in permission:
		if "tr" in state: 
			perm.update(priority_speaker=True)
		else:
			perm.update(priority_speaker=False)
	elif "managethreads" in permission:
		if "tr" in state:
			perm.update(manage_threads = True)
		else:
			perm.update(manage_threads = False)

	
	await role.edit(permission=perm)

@client.command()
async def disablecommand(ctx, command_name):
	if ctx.author.id!=825282868028375062 and ctx.author.id!=820189220185833472:
		await ctx.send("You don't have permission to use this command.")
		return
	command = client.get_command(command_name)
	command.update(enabled=False)
	await ctx.send("Command disabled.")

@client.command()
async def enablecommand(ctx, command_name):
	if ctx.author.id!=825282868028375062 and ctx.author.id!=820189220185833472:
		await ctx.send("You don't have permission to use this command.")
		return
	command = client.get_command(command_name)
	command.update(enabled=True)
	await ctx.send("Command enabled.")

@client.event
async def on_ready():
	print('Logged in as {0.user}'.format(client))
	print(discord.__version__)

	print("Copyright © 2021  RockSolid1106. \nThis program comes with ABSOLUTELY NO WARRANTY; This is free software, and you are welcome to redistribute it, provided that you credit RockSolid1106.")
	client.load_extension(f"modules.moderation")
	client.load_extension(f"modules.member")
	client.load_extension(f"modules.time_based")
	#client.load_extension(f"modules.chatfilter")
	client.load_extension(f"modules.reactionroles")
	client.load_extension(f"modules.administrator")
	client.load_extension(f"modules.logger")
	#DiscordComponents(client, change_discord_methods=True)
	


@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.DisabledCommand):
		await ctx.send("This command has been disabled. You may not use it until it has been enabled again.")
	elif isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("A required parameter is missing.")
	elif isinstance(error, commands.MemberNotFound):
		await ctx.send("The member specified was not found.")
	elif isinstance(error, commands.UserNotFound):
		await ctx.send("The member specified was not found.")
	elif isinstance(error, commands.ExtensionNotFound):
		await ctx.send("The extension was not found.")




client.run(
    os.getenv("TOKEN")
) 


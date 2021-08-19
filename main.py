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







##########--functions end------###########


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
#@commands.has_any_role("Owner", "Admin")
async def setupbot(ctx, mcid=None, scid=None):
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
	if ctx.author.id!=825282868028375062 or ctx.author.id!=820189220185833472:
		await ctx.send("You dont have permissions to do that.")
		return
	client.load_extension(f"modules.{module}")
	await ctx.send(f"Successfully loaded ```{module}```")

@client.command()
async def unload(ctx, module):
	if ctx.author.id!=825282868028375062 or ctx.author.id!=820189220185833472:
		await ctx.send("You dont have permissions to do that.")
		return
	client.unload_extension(f"modules.{module}")
	await ctx.send(f"Successfully unloaded ```{module}```")

@client.command()
async def reload(ctx, module):
	if ctx.author.id!=825282868028375062 and ctx.author.id!=820189220185833472:
		await ctx.send("You dont have permissions to do that.")
		return
	client.unload_extension(f"modules.{module}")
	time.sleep(0.5)
	client.load_extension(f"modules.{module}")
	await ctx.send(f"Succesfully reloaded ```{module}```")



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
	client.load_extension(f"modules.moderation")
	client.load_extension(f"modules.member")
	client.load_extension(f"modules.hello")
	#DiscordComponents(client, change_discord_methods=True)
	
	
	





client.run(
    os.getenv("TOKEN")
) 


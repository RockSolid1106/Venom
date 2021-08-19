from discord.ext import commands
client=commands.Bot(command_prefix="!")
class xyz(commands.Cog, name="Hello"):
	def __init__(self, client: commands.Bot):
		self.client = commands.Bot(command_prefix="!")
	
	@commands.command(pass_context=True, brief="Timepass")
	async def sup(self, ctx):
		await ctx.send(f'Hello there {ctx.author.mention}, how are you doing?')
	@commands.command()
	async def reply(ctx):
		await ctx.send("Sup")

def setup(client: commands.Bot):
	client.add_cog(xyz(client))
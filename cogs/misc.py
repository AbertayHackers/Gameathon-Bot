import discord
from tabulate import tabulate
from discord.ext import commands
from libs.loadconf import config, strings
from libs.format import formatHelp

class Misc(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		@bot.command(name="ping", description=formatHelp("ping", "desc"), usage=formatHelp("ping", "usage"))
		async def ping(ctx):
			await ctx.send("Pong!")

		@bot.command(name="github", description=formatHelp("github", "desc"), usage=formatHelp("github", "usage"))
		async def github(ctx):
			embed = discord.Embed(colour=discord.Colour.green())
			embed.title = "Github"
			embed.description = config["github"]
			await ctx.channel.send(embed=embed)


		@bot.command(name="help", description=formatHelp("help", "desc"), usage=formatHelp("help", "usage"))
		async def help(ctx, cmd = None):
			embed = discord.Embed(colour=discord.Colour.blue())
			if cmd != None:
				if cmd not in config["hiddenCommands"]:
					found = False
					for command in bot.commands:
						if cmd == command.name:
							embed.title = f"**{command.name.capitalize()}**"
							embed.description = f"__*Description:*__ ```{command.description}```\n__*Usage:*__ ```{command.usage}```"
							found = True
							break;
					if not found:
						await ctx.channel.send(strings["errors"]["commandNotFound"].format(cmd))
						return		
			else:
				embed.title = "**Help**"
				for command in bot.commands:
					embed.add_field(
						name=f"\n\n===================================================\n**__{command.name}__**\n",
						value=f"__*Description:*__ ```{command.description}```\n__*Usage:*__ ```{command.usage}```",
						inline=False
					)
			try:
				await ctx.author.send(embed=embed)
				await ctx.message.add_reaction('\U0001F44D')
			except discord.errors.Forbidden:
				await ctx.channel.send(strings["errors"]["botBlocked"].format(ctx.message.author.id))

				
def setup(bot):
	bot.add_cog(Misc(bot))

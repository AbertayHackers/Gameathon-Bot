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
		async def help(ctx):
			commands = []	
			text = f"{strings['help']['title']}\n{strings['help']['overview']}\n"
			for command in bot.commands:
				tempCmd = []
				if not command.name or command.name in config["hiddenCommands"]:
					continue
				tempCmd.append(command.name)
				tempCmd.append(command.description) if command.description else tempCmd.append("No Description")
				tempCmd.append(command.usage) if command.usage else tempCmd.append("No Usage Information")
				commands.append(tempCmd)
			text += f"```\n{tabulate(commands, ['Command', 'Description', 'Usage'], tablefmt='grid')}\n```"
			
			try:
				await ctx.author.send(text)
				await ctx.message.add_reaction('\U0001F44D')
			except discord.errors.Forbidden:
				await ctx.channel.send(strings["errors"]["botBlocked"].format(ctx.message.author.id))

def setup(bot):
	bot.add_cog(Misc(bot))

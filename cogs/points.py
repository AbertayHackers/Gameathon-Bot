"""
Title:			Points
Type:			Cog
Purpose:		Handles the points commands (leaderboard and individual points)
Author: 		AG | MuirlandOracle
Last Updated:	24/02/21
"""
import discord
from tabulate import tabulate
from discord.ext import commands
from libs.loadconf import config, strings
from libs.format import formatHelp
from libs.calc import Calc
from libs.db import DBHandle
from libs.logging import Log as log

class Points(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		#Initialise instances of the DB and calc auxiliary class
		self.db = DBHandle()
		self.calc = Calc()

		#Define the leaderboard command
		@bot.command(name="leaderboard", description=formatHelp("leaderboard", "desc"), usage=formatHelp("leaderboard", "usage"))
		async def leaderboard(ctx):
			#If the user has used the command recently and is not an admin, given them an error message (hopefully this will prevent HTB's shitty API from blocking us)
			if not self.db.checkTime(ctx.message.author.id) and ctx.message.author.id not in config["admins"]:
				print (type(ctx.message.author.id))
				await ctx.channel.send(strings["errors"]["leaderboardCooldown"].format(config["prefix"], config["leaderboard"]["cooldown"] // 60))
				return
			#Log a points update then update all the points
			log.updateAllPoints(ctx.message.author.id)
			self.calc.updateAllPoints()
			#Set up the leaderboard embed then send it
			embed = discord.Embed(colour=discord.Colour.blue())
			embed.title="Leaderboard"
			raw = self.db.leaderboard()
			leaderboard = []
			for index,value in enumerate(raw):
				temp = [index+1]
				temp.append(bot.get_user(int(value[0])).name)
				temp.append(value[1])
				leaderboard.append(temp)
			leaderboard = tabulate(leaderboard, ["Rank", "Username", "Points"], tablefmt="fancy_grid")
			embed.description=f"```\n{leaderboard}```"
			await ctx.channel.send(embed=embed)


		#Get an individual's points. No rate limit on this, but may need to implement one
		@bot.command(name="points", description=formatHelp("points", "desc"), usage=formatHelp("points", "usage"))
		async def points(ctx):
			self.calc.updatePoints(ctx.message.author.id)
			points = self.db.getPoints(ctx.message.author.id)
			await ctx.channel.send(strings["points"].format(bot.get_user(ctx.message.author.id).name, points))
				
def setup(bot):
	bot.add_cog(Points(bot))

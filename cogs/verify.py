"""
Title:			Verify
Type:			Cog
Purpose:		Handles user verification
Author: 		AG | MuirlandOracle
Last Updated:	24/02/21
"""
import discord, requests, asyncio, re, json, os
from bs4 import BeautifulSoup as bs4
from discord.ext import commands
from libs.loadconf import strings, endpoints, config
from libs.format import formatHelp
from libs.db import DBHandle
from libs.req import Api

class Verify(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		#Initialises instances of the DB and api auxiliary class
		self.db = DBHandle()
		self.api = Api()

		#Link a THM account
		@bot.command(name="thmlink", description=formatHelp("thmlink", "desc"), usage=formatHelp("thmlink", "usage"))
		async def thmlink(ctx, token = None):
			#Sort out the token to ensure that it's sanitised (and exists)
			discordID, token = await preprocess(ctx, token)	
			if not discordID:
				return

			#Get the user info
			userHandle = self.db.getUser(discordID)
			if userHandle["thmUser"] != None:
				await ctx.channel.send(strings["errors"]["alreadyLinked"])
				return

			#Get requisite variables
			username = self.api.getTHMProfile(token)
			points = self.api.getTHMPoints(username)
			self.db.addTHMUser(discordID, username, points, token)
			await ctx.channel.send(strings["success"]["linked"])
		
		

		@bot.command(name="htblink", description=formatHelp("htblink", "desc"), usage=formatHelp("htblink", "usage"))
		async def htblink(ctx, token = None):
			#Same as the thmlink command from here on out
			discordID, token = await preprocess(ctx, token)	
			if not discordID:
				return
			
			#Get user info
			userHandle = self.db.getUser(discordID)
			if userHandle["htbID"] != None:
				await ctx.channel.send(strings["errors"]["alreadyLinked"])
				return

			username, userid = self.api.getHTBProfile(token)
			points = self.api.getHTBPoints(userid)
			#If it wasn't possible to retrieve points then the user hasn't set their HTB profile to public. Yes, this is a shitty way to scrape points, but HTB haven't bothered publishing API docs
			#and I already called in my favours to get the user endpoint ¯\_(ツ)_/¯
			if(points == None):
				await ctx.channel.send(strings["errors"]["profileNotPublic"])
				return
			self.db.addHTBUser(discordID, username, userid, points, token)
			await ctx.channel.send(strings["success"]["linked"])



		##Helper Funcs
		def stripToken(token):
			return re.sub("[\W_]", "", token)

		async def checkDM(ctx):
			if not isinstance(ctx.channel, discord.channel.DMChannel):
				await ctx.message.delete() 
				res = await ctx.channel.send(strings["errors"]["noDM"])			
				await asyncio.sleep(5)
				await res.delete()
				return False
			return True

		async def preprocess(ctx, token):
			if not await checkDM(ctx):
				return False, False
			elif not token:
				await ctx.channel.send(strings["errors"]["noToken"])
				return False, False
			discordID = ctx.message.author.id
			token = stripToken(token)
			return discordID, token



def setup(bot):
	bot.add_cog(Verify(bot))

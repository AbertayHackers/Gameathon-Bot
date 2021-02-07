import discord, requests, asyncio, re, json, os
from bs4 import BeautifulSoup as bs4
from discord.ext import commands
from libs.loadconf import strings, endpoints, config
from libs.format import formatHelp
from libs.db import DBHandle

class Verify(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.db = DBHandle()

		@bot.command(name="thmlink", description=formatHelp("thmlink", "desc"), usage=formatHelp("thmlink", "usage"))
		async def thmlink(ctx, token = None):
			discordID, token = await preprocess(ctx, token)	
			if not discordID:
				return

			#Get the user info
			userHandle = self.db.getUser(discordID)
			if userHandle["thmUser"] != None:
				await ctx.channel.send(strings["errors"]["alreadyLinked"])
				return

			#If not already verified, verify
			r = requests.get(endpoints["thm"]["verify"].format(token))
			username = json.loads(r.text)["username"]
			r = requests.get(endpoints["thm"]["user"].format(username))
			points = json.loads(r.text)["points"]
			self.db.addTHMUser(discordID, username, points, token)
			await ctx.channel.send(strings["success"]["linked"])
		
		
		@bot.command(name="htblink", description=formatHelp("htblink", "desc"), usage=formatHelp("htblink", "usage"))
		async def htblink(ctx, token = None):
			sess = requests.session()
			sess.headers = config["reqHeaders"]
			discordID, token = await preprocess(ctx, token)	
			if not discordID:
				return
			
			#Get user info
			userHandle = self.db.getUser(discordID)
			if userHandle["htbID"] != None:
				await ctx.channel.send(strings["errors"]["alreadyLinked"])
				return

			#Verify the user
			r = sess.get(endpoints["htb"]["verify"].format(token))
			data = json.loads(r.text)
			username = data["user_name"]
			userid = data["user_id"]
			#Get the points
			r = sess.get(endpoints["htb"]["points"].format(userid))
			soup = bs4(r.text, 'html.parser')
			points = soup.find('span', {"title":"Points"}).get_text().strip()
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
				return False
			elif not token:
				await ctx.channel.send(strings["errors"]["noToken"])
				return False
			discordID = ctx.message.author.id
			token = stripToken(token)
			return discordID, token



def setup(bot):
	bot.add_cog(Verify(bot))

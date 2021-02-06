import discord, requests, asyncio, re, json, os
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
			if not await checkDM(ctx):
				return
			elif not token:
				await ctx.channel.send(strings["errors"]["noToken"])
				return

			#Get Discord ID
			discordID = ctx.message.author.id

			#Sanitise Token
			token = stripToken(token)

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
			if(self.db.addTHMUser(discordID, username, points, token)):
				await ctx.channel.send(strings["success"]["linked"])
			else:
				await ctx.channel.send(strings["errors"]["failedLink"])

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



def setup(bot):
	bot.add_cog(Verify(bot))

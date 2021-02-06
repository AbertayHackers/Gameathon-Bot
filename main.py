#!/usr/bin/python3
import discord, asyncio, os, argparse, sys, datetime, signal
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingRequiredArgument
from dotenv import load_dotenv
from libs.loadconf import config, secrets
from libs.colours import Colours as colours

#Signal Handling 
def exiting():
	colours.success("Exiting...")
	sys.exit(0)

def sigHandle(sig, frame):
	exiting()
signal.signal(signal.SIGINT, sigHandle)


#Bot Setup
bot = commands.Bot(command_prefix=config["prefix"])
bot.remove_command("help")


#Record start time in environment variable
os.environ["GAMEATHON-START"] = str(datetime.date.today())


#Loading Cogs
def loadCogs():
	for cog in config["cogs"]:
		try:
			bot.load_extension(cog)
			colours.success(f"{cog} loaded successfully")
		except Exception as e:
			colours.warn(f"{cog} failed to load: {e}")


@bot.event
async def on_ready():
	if config["status"] != "":
		await bot.change_presence(activity=discord.Game(config["status"]))
	colours.success("Connected")

@bot.event
async def on_command_error(ctx, error):
    error_to_skip = [CommandNotFound, MissingRequiredArgument]
    for error_type in error_to_skip:
        if isinstance(error, error_type):
            return
    raise error

if __name__ == "__main__":
	loadCogs()
	try:
		bot.run(secrets["TOKEN"])
	except RuntimeError:
		exiting()	

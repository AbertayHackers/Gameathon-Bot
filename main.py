#!/usr/bin/python3
"""
Title:            Main
Type:            Main Program
Purpose:        Start the whole thing!
Author:         AG | MuirlandOracle
Last Updated:    24/02/21
"""
import discord, asyncio, os, argparse, sys, datetime, signal
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingRequiredArgument
from dotenv import load_dotenv
from libs.loadconf import config, secrets
from libs.colours import Colours as colours
from libs.logging import Log as log

#Signal Handling 
def exiting():
    log.end()
    colours.success("Exiting...")
    sys.exit(0)

def sigHandle(sig, frame):
    exiting()
signal.signal(signal.SIGINT, sigHandle)


#Bot Setup
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=config["prefix"], intents=intents)
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

#Change the status of the bot once connected to the server
@bot.event
async def on_ready():
    if config["status"] != "":
        await bot.change_presence(activity=discord.Game(config["status"]))
    colours.success("Connected")


#Get rid of the output from people typing commands that don't exist (or forgetting to add a command argument)
@bot.event
async def on_command_error(ctx, error):
    error_to_skip = [CommandNotFound, MissingRequiredArgument]
    for error_type in error_to_skip:
        if isinstance(error, error_type):
            return
    raise error


#Release the bot!
if __name__ == "__main__":
    log.start() #Start Logging
    loadCogs() #Load the cogs
    try:
        bot.run(secrets["TOKEN"]) #Start the bot -- if the token doesn't exist, maybe try adding this
    except RuntimeError:
        exiting()    

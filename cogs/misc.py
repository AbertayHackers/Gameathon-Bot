"""
Title:            Misc
Type:            Cog
Purpose:        Handles miscellaneous commands (help, ping, etc)
Author:         AG | MuirlandOracle
Last Updated:    24/02/21
"""
import discord
import discord
from discord.ext import commands
from libs.loadconf import config, strings
from libs.format import formatHelp

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        #Simple ping command to check bot status
        @bot.command(name="ping", description=formatHelp("ping", "desc"), usage=formatHelp("ping", "usage"))
        async def ping(ctx):
            await ctx.send("Pong!")


        #Provide a link to the bot's github repo
        @bot.command(name="github", description=formatHelp("github", "desc"), usage=formatHelp("github", "usage"))
        async def github(ctx):
            embed = discord.Embed(colour=discord.Colour.green())
            embed.title = "Github"
            embed.description = config["github"]
            await ctx.channel.send(embed=embed)


        #Help command for the bot
        @bot.command(name="help", description=formatHelp("help", "desc"), usage=formatHelp("help", "usage"))
        async def help(ctx, cmd = None):
            embed = discord.Embed(colour=discord.Colour.blue())
            #Check to see if the user specified a command to get help for
            if cmd != None:
                found = False
                #Check if the command exists but is hidden
                if cmd not in config["hiddenCommands"]:
                    for command in bot.commands:
                        if cmd == command.name:
                            embed.title = f"**{command.name.capitalize()}**"
                            embed.description = f"__*Description:*__ ```{command.description}```\n__*Usage:*__ ```{command.usage}```"
                            found = True
                            break;
                #If the command was hidden (or doesn't exist), send an error
                if not found:
                    await ctx.channel.send(strings["errors"]["commandNotFound"].format(cmd))
                    return

            #If no argument was given, send all the commands
            else:
                embed.title = "**Help**"
                desc = strings["help"]["helpHelp"].format(config["prefix"])
                desc += "```"
                for command in bot.commands:
                    if command.name not in config["hiddenCommands"]:
                        desc += f"\n{command.name}"
                embed.description=f"{desc}```"
            try:
                await ctx.author.send(embed=embed)
                await ctx.message.add_reaction('\U0001F44D')
            except discord.errors.Forbidden:
                await ctx.channel.send(strings["errors"]["botBlocked"].format(ctx.message.author.id))

                
def setup(bot):
    bot.add_cog(Misc(bot))

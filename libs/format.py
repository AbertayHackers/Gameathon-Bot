"""
Title:			Format
Type:			Helper functions
Purpose:		Grabs complex stuff from the config files and formats them nicely
Author: 		AG | MuirlandOracle
Last Updated:	24/02/21

"""
from libs.loadconf import strings, config


#Format the help command info
def formatHelp(cmd, arg):
	return strings["commands"][cmd][arg].format(config["prefix"])

#Take raw DB output for a user and format it into a proper dictionary
def formatUser(user):
	userDict = {}
	for index, value in enumerate(config["db"]["dbUserCols"].keys()):
		userDict[value] = user[index]
	return userDict

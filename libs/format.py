from libs.loadconf import strings, config


def formatHelp(cmd, arg):
	return strings["commands"][cmd][arg].format(config["prefix"])

def formatUser(user):
	userDict = {}
	for index, value in enumerate(config["db"]["dbUserRows"].keys()):
		userDict[value] = user[index]
	return userDict

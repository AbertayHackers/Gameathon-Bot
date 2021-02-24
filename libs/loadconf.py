"""
Title:			Load Conf
Type:			Auxiliary Functions / Variables
Purpose:		Loads all the configs and stores them in memory for access by other modules
Author: 		AG | MuirlandOracle
Last Updated:	24/02/21

"""
import json, re, datetime, os

#Open all the config files
with open("config/secret.json") as secretData,\
	 	open("config/config.json") as configData,\
	 	open("config/apiEndpoints.json") as epData,\
	 	open("config/contributors.json") as contribData,\
	 	open("config/logMessages.json") as logMessages,\
	 	open("config/strings.json") as stringData:
	secrets = json.load(secretData)
	config = json.load(configData)
	endpoints = json.load(epData)
	strings = json.load(stringData)
	logMsg = json.load(logMessages)
	contributors = json.load(contribData)


#Get the name of the current database
def getDB():
	dbname = config["db"]["path"]
	dbname = re.sub("DATE", os.environ.get("GAMEATHON-START"), dbname)
	return dbname

#Get the name of the current logfile
def getLog():
	logName = config["logs"]["path"]
	logName = re.sub("DATE", os.environ.get("GAMEATHON-START"), logName)
	return logName

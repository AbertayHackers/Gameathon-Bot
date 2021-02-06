import json, re, datetime, os

with open("config/secret.json") as secretData,\
	 	open("config/config.json") as configData,\
	 	open("config/apiEndpoints.json") as epData,\
	 	open("config/contributors.json") as contribData,\
	 	open("config/strings.json") as stringData:
	secrets = json.load(secretData)
	config = json.load(configData)
	endpoints = json.load(epData)
	strings = json.load(stringData)
	contributors = json.load(contribData)


def getDB():
	dbname = config["db"]["path"]
	dbname = re.sub("DATE", os.environ.get("GAMEATHON-START"), dbname)
	return dbname


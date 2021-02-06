import sqlite3, datetime, os, sys
from libs.colours import Colours as colours
from libs.loadconf import config, getDB
from libs.format import formatUser

class DBHandle():
	def __init__(self):
		self.dbname = getDB()
		self.connect()

	def __del__(self):
		self.curs.close()
		self.conn.close()

	def connect(self):
		self.conn = sqlite3.connect(self.dbname)
		self.curs = self.conn.cursor()

		tableList = self.conn.execute("SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name").fetchall()
		for i in tableList:
			if i[0] == "users":
				return
		self.setup()
	
	def addTHMUser(self, discordID, user, points, token):
		userHandle = self.getUser(discordID)
		if userHandle["thmUser"] != None:
			return False
		cmd = "UPDATE users SET thmUser=?, thmPoints=?, thmToken=? WHERE discordID = ?"
		self.curs.execute(cmd, (user, points, token, discordID))
		self.conn.commit()
		return True

	def setup(self):
		colours.info(f"New Database {self.dbname}. Creating tables...")
		setup = ""
		for i in config["db"]["dbUserRows"].keys():
			setup += f"{i} {config['db']['dbUserRows'][i]}, "
		setup = setup[:-2]
		self.conn.execute(f"CREATE TABLE {config['db']['tableName']} ({setup})")
		self.conn.commit()
		
	def getUser(self, discordID):
		checkId = "SELECT * FROM users WHERE discordID=?"
		entered = self.curs.execute(checkId, (discordID,)).fetchall()
		if len(entered) < 1:
			self.addUser(discordID)
			return self.getUser(discordID)
		return formatUser(entered[0])

	def addUser(self, discordID):
		cmd = "INSERT INTO users (discordID) VALUES(?)"
		self.curs.execute(cmd, (discordID,)).fetchall()
		self.conn.commit()


	def printInfo(self):
		print(f"DB Name: {self.dbname}")



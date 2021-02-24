"""
Title:			DB
Type:			Auxiliary Class
Purpose:		Handles all Database operations
Author: 		AG | MuirlandOracle
Last Updated:	24/02/21

"""
import sqlite3, datetime, os, sys, time
from libs.colours import Colours as colours
from libs.loadconf import config, getDB, strings
from libs.format import formatUser
from libs.logging import Log as log

class DBHandle():
	def __init__(self):
		self.dbname = getDB()
		self.connect()

	def __del__(self):
		if(hasattr(self, 'curs')):
			self.curs.close()
		if(hasattr(self, 'conn')):
			self.conn.close()

	#Attempt a DB connection
	def connect(self):
		try:
			self.conn = sqlite3.connect(self.dbname)
		except:
			colours.fail(strings["errors"]["dbConnectFail"]) 
		self.curs = self.conn.cursor()
		
		#Check to see if the database contains a "users" table
		tableList = self.conn.execute("SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name").fetchall()
		for i in tableList:
			if i[0] == "users":
				return
		#If not, create it!
		self.setup()
	
	#Add a THM user into the DB
	def addTHMUser(self, discordID, user, points, token):
		log.linkAccount(discordID, "THM", user, points)
		cmd = "UPDATE users SET thmUser=?, thmPoints=?, thmToken=? WHERE discordID = ?"
		self.curs.execute(cmd, (user, points, token, discordID))
		self.conn.commit()

	#Add a HTB user into the DB
	def addHTBUser(self, discordID, user, ID, points, token):
		log.linkAccount(discordID, "HTB", user, points)
		cmd = "UPDATE users SET htbUser=?, htbID=?, htbPoints=?, htbToken=? WHERE discordID=?"
		self.curs.execute(cmd, (user, ID, points, token, discordID))
		self.conn.commit()

	#Set up the DB
	def setup(self):
		#Log this
		log.dbCreate(self.dbname)
		#Get the rows from the DB
		setup = ""
		for i in config["db"]["dbUserCols"].keys():
			setup += f"{i} {config['db']['dbUserCols'][i]}, "
		setup = setup[:-2]
		#Set up the users table
		self.conn.execute(f"CREATE TABLE users({setup})")
		self.conn.commit()

	#Get the points for a single user
	def getPoints(self, discordID):
		cmd = "SELECT points FROM users WHERE discordID=?"
		points = self.curs.execute(cmd, (discordID,)).fetchall()
		return points[0][0]


	#Update the points for the user
	def updatePoints(self, discordID, points):
		log.updatePoints(discordID, points)
		cmd = "UPDATE users SET points=? WHERE discordID=?"
		self.curs.execute(cmd, (points, discordID))
		self.conn.commit()

	#Get the leaderboard
	def leaderboard(self):
		return self.conn.execute(f"SELECT discordID, points FROM users ORDER BY points DESC LIMIT {config['leaderboard']['limit']}").fetchall()
	
	#Return a single user record from the DB
	def getUser(self, discordID):
		checkId = "SELECT * FROM users WHERE discordID=?"
		entered = self.curs.execute(checkId, (discordID,)).fetchall()
		#If the user doesn't exist, add them!
		if len(entered) < 1:
			self.addUser(discordID)
			return self.getUser(discordID)
		return formatUser(entered[0])

	#Get all information from all users
	def getUsers(self):
		users = []
		for i in self.conn.execute("SELECT * FROM users").fetchall():
			users.append(formatUser(i))
		return users

	#Get all user IDs
	def getUserIDs(self):
		try:
			return list(self.conn.execute("SELECT discordID FROM users").fetchall()[0])
		except:
			return False

	#Add a new (blank) user into the DB. This adds their ID with 0 points, ready for account linkage
	def addUser(self, discordID):
		cmd = "INSERT INTO users (discordID) VALUES(?)"
		self.curs.execute(cmd, (discordID,)).fetchall()
		self.conn.commit()

	#Check when the user last used the leaderboard command
	def checkTime(self, discordID, difference=config["leaderboard"]["cooldown"]):
		self.getUser(discordID)
		sql = "SELECT lastLeaderboard FROM users WHERE discordID = ?"
		storedTime = self.curs.execute(sql, (discordID,)).fetchone()[0]
		currentTime = int(time.time())
		if currentTime - storedTime <= difference:
			return False
		else:
			sql = "UPDATE users SET lastLeaderboard = ? WHERE discordID = ?"
			self.curs.execute(sql, (currentTime, discordID))
			self.conn.commit()
			return True
		

	#Get the DB name. This isn't actually used, but meh
	def printInfo(self):
		print(f"DB Name: {self.dbname}")



"""
Title:			API
Type:			Auxiliary Class
Purpose:		Makes all the requests to the various APis
Author: 		AG | MuirlandOracle
Last Updated:	24/02/21

"""
import requests, json
from bs4 import BeautifulSoup as bs4
from libs.loadconf import config, endpoints

class Api():
	def __init__(self):
		self.sess = requests.session()
		self.sess.headers = config["reqHeaders"]

	def getTHMProfile(self, token):
		r = self.sess.get(endpoints["thm"]["verify"].format(token))
		username = json.loads(r.text)["username"]
		return username

	def getTHMPoints(self, username):
		r = self.sess.get(endpoints["thm"]["user"].format(username))
		points = json.loads(r.text)["points"]
		return points

	def getHTBProfile(self, token):
		r = self.sess.get(endpoints["htb"]["verify"].format(token))
		data = json.loads(r.text)
		username = data["user_name"]
		userid = data["user_id"]
		return username, userid

	#Don't even ask about this one...
	#HTB don't bother releasing API docks, so....
	def getHTBPoints(self, userid):
		r = self.sess.get(endpoints["htb"]["points"].format(userid))
		soup = bs4(r.text, 'html.parser')
		try:
			points = soup.find('span', {"title":"Points"}).get_text().strip()
		except:
			return None
		return int(points)

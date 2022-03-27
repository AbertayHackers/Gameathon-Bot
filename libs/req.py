"""
Title:            API
Type:            Auxiliary Class
Purpose:        Makes all the requests to the various APis
Author:         AG | MuirlandOracle
Last Updated:    24/02/21

"""
import requests, json
from bs4 import BeautifulSoup as bs4
from libs.loadconf import config, endpoints
from libs.colours import Colours as colours

class Api():
    def __init__(self):
        self.sess = requests.session()
        self.sess.headers = config["reqHeaders"]

    def getTHMProfile(self, token):
        r = self.sess.get(endpoints["thm"]["verify"].format(token))
        if r.status_code != 200:
            return False
        try:
            username = json.loads(r.text)["username"]
        except json.decoder.JSONDecodeError:
            colours.fail("THM has Cloudflare active...")
            
        return username

    def getTHMPoints(self, username):
        r = self.sess.get(endpoints["thm"]["user"].format(username))
        if r.status_code != 200:
            return False
        points = json.loads(r.text)["points"]
        return points

    def getHTBProfile(self, token):
        r = self.sess.get(endpoints["htb"]["verify"].format(token))
        if r.status_code != 200:
            return False, False
        data = json.loads(r.text)
        username = data["user_name"]
        userid = data["user_id"]
        return username, userid

    def getHTBPoints(self, userid):
        r = self.sess.get(endpoints["htb"]["points"].format(userid))
        if r.status_code != 200:
            return None
        points = json.loads(r.text)["profile"]["points"]
        return int(points)

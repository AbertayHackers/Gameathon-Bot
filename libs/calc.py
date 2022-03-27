"""
Title:            Calc
Type:            Auxiliary Class
Purpose:        Calculate points
Author:         AG | MuirlandOracle
Last Updated:    24/02/21
"""
from libs.db import DBHandle
from libs.req import Api
from multiprocessing.pool import ThreadPool

class Calc():
    def __init__(self):
        self.db = DBHandle()
        self.api = Api()


    #Update points for a single user
    def updatePoints(self, discordID):
        db = DBHandle()
        userHandle = db.getUser(discordID)
        points = self.getPoints(userHandle["thmUser"], userHandle["thmPoints"], userHandle["htbID"], userHandle["htbPoints"])
        if(points != userHandle["points"]):
            db.updatePoints(discordID, points)

    #Do the actual calculation
    def getPoints(self, thmUser, thmPoints, htbID, htbPoints):
        points = 0
        if(thmUser != None):
            newTHMPoints = self.api.getTHMPoints(thmUser)
            points += (newTHMPoints - thmPoints)
        if(htbID != None):
            newHTBPoints = self.api.getHTBPoints(htbID)
            if(newHTBPoints != None):
                points += (newHTBPoints - htbPoints)
        return points

    #Simultaneously update all points -- use with caution!
    def updateAllPoints(self):
        users = self.db.getUserIDs()
        if not users:
            return False
        with ThreadPool(processes=5) as p:
            p.map(self.updatePoints, users)
        return True

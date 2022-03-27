"""
Title:            Logging
Type:            Auxiliary Class
Purpose:        Keep track of the logs
Author:         AG | MuirlandOracle
Last Updated:    24/02/21

"""
import os
from datetime import datetime
from libs.colours import Colours as colours
from libs.loadconf import getLog, logMsg

#Log class -- mainly static
class Log():
    #Get the current date
    date = lambda: datetime.utcnow()


    #Write out to the log file
    @classmethod
    def writeToFile(self, msg):
        if not os.path.isdir("logs"):
            try:
                os.mkdir("logs")
            except:
                colours.fail("Couldn't create the log directory -- check your file permissions")

        #Handle for the log file -- opening in append mode
        with open(getLog(), "a") as handle:
            handle.write(f"{msg}\n")

    #If these aren't self explanatory, please close this file and back away slowly
    @classmethod
    def start(self):
        colours.info(f"Starting Log {getLog()}...")
        self.writeToFile(logMsg["initialise"].format(self.date()))

    @classmethod
    def end(self):
        colours.info(f"Ending Log {getLog()}...")
        self.writeToFile(logMsg["end"].format(self.date()))
        
    @classmethod
    def linkAccount(self, user, account, username, points):
        self.writeToFile(logMsg["linkAccount"].format(self.date(), user, account, username, points))


    @classmethod
    def updatePoints(self, user, points):
        self.writeToFile(logMsg["pointsUpdate"].format(self.date(), user, points))    

    @classmethod
    def updateAllPoints(self, user="Unknown"):
        self.writeToFile(logMsg["allPointsUpdate"].format(self.date(), user))

    @classmethod
    def dbCreate(self, dbname):
        colours.info(f"New Database {dbname}. Creating tables...")
        self.writeToFile(logMsg["dbCreate"].format(self.date(), dbname))




# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 18:33:16 2021

@author: Flirno
"""

import api
from flask import Flask, render_template
import json 
from datetime import date  
from datetime import datetime

app = Flask(__name__)


today = str(date.today())
now = datetime.now()
current_time = now.strftime("%H:%M:%S")

@app.route("/")
@app.route("/home")
@app.route("/index")
def hello():
    return ('<!DOCTYPE html><html><head><title>TrackmaniaStats</title></head><body><h1>Welcome to the TrackmaniaStats api</h1><p>Latest heroku deploy : '+ today + " " + str(current_time)+'</p><h2>Available public endpoint :</h2> <p><a href="https://trackmaniastats.herokuapp.com/api/searchPlayer/playerName">https://trackmaniastats.herokuapp.com/api/searchPlayer/playerName</a> put a player name in that url to get that player ingame ID</p> <p><a href="https://trackmaniastats.herokuapp.com/api/playerProfiles/playerID">https://trackmaniastats.herokuapp.com/api/playerProfiles/playerID</a> put a player ID to get their profile</p> <p><a href="https://trackmaniastats.herokuapp.com/api/playerList">https://trackmaniastats.herokuapp.com/api/playerList</a> to directly get the list of all the players with their corresponding ID</p> <p><a href="https://trackmaniastats.herokuapp.com/api/cotd/compID">https://trackmaniastats.herokuapp.com/api/cotd/compID</a> get the global results of a cotd (compID can be found on trackmania.io)</p> </body></html>')


@app.route("/admin")
def admin():
    return ('<!DOCTYPE html><html><head><title>TrackmaniaStats</title></head><body><h1>Welcome to the TrackmaniaStats api</h1><p>Latest heroku deploy : '+ today + " " + str(current_time)+'</p><h2>Available admin endpoint :</h2> <p><a href="https://trackmaniastats.herokuapp.com/api/createLatestcotdJSON/">https://trackmaniastats.herokuapp.com/api/createLatestcotdJSON/</a> get latest cotd result and upload to github ID</p> <p><a href="https://trackmaniastats.herokuapp.com/api/updatePlayers/">https://trackmaniastats.herokuapp.com/api/updatePlayers/</a> update Player profiles ID</p> <p><a href="https://trackmaniastats.herokuapp.com/api/sortPlayerList/">https://trackmaniastats.herokuapp.com/api/sortPlayerList/</a> Sort player list (just fun)</p> </body></html>')



#---------------------PUBLIC-----------------------#

@app.route('/api/searchPlayer/<playerName>')
def searchPlayer(playerName):
    
    playerID = api.searchPlayerByName(playerName)
    
    if playerID == "":
        return "Sorry, player not found."
        
    return ('<a href="https://trackmaniastats.herokuapp.com/api/playerProfile' + str(playerID) + '">https://trackmaniastats.herokuapp.com/api/playerProfile' + str(playerID)+'</a>')

@app.route('/api/playerList')
def playerList():
    
    fileName = 'json/playerList.json'
    
    with open(fileName,'r') as json_file:
       playerList = json.load(json_file)

    return playerList


@app.route('/api/playerProfiles/<playerID>')
def playerProfiles(playerID):
    
    fileName = 'json/playerProfiles/' + playerID + '.json'
    
    with open(fileName,'r') as json_file:
       playerJSON = json.load(json_file)

    return playerJSON

@app.route('/api/cotd/<string:compID>')
def cotd(compID):
    
    fileName = 'json/cotd/cotd-' + compID + '.json'
    
    with open(fileName,'r') as json_file:
       cotdJSON = json.load(json_file)

    return cotdJSON



#---------------------ADMIN FOR DATABASE UPDATE-----------------------#



@app.route('/api/createLatestcotdJSON/')
def createLatestcotdJSON():
    result = api.createLatestcotdJSON()
    return result


@app.route('/api/updatePlayers/<pwd>')
def updatePlayers():
    api.updatePlayersProfile(api.getLatestFinishedcotdID())



@app.route('/api/sortPlayerList/<pwd>')
def sortPlayerList():
    api.sortAlphabeticalOrder()


@app.route('/api/testUpload')
def testUpload():
    api.testUpload()

    
    
    
    
    
    
if __name__ == "__main__":
    app.run(debug=True)

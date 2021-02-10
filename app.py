# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 18:33:16 2021

@author: Flirno
"""

import api
from flask import Flask, render_template
import json 

app = Flask(__name__)

@app.route("/")
@app.route("/home")
@app.route("/index")
def hello():
    return ("<!DOCTYPE html><html><head><title>TrackmaniaStats</title></head><body><h1>Welcome to the TrackmaniaStats api</h1><h2>Available public endpoint :</h2> <p><a href="https://trackmaniastats.herokuapp.com/api/searchPlayer/<playerName>">https://trackmaniastats.herokuapp.com/api/searchPlayer/<playerName></a> put a player name in that url to get that player game ID</p> <p><a href="https://trackmaniastats.herokuapp.com/api/playerProfiles/<playerID>">https://trackmaniastats.herokuapp.com/api/playerProfiles/<playerID></a> put a player ID to get their profile</p> <p><a href="https://trackmaniastats.herokuapp.com/api/playerList">https://trackmaniastats.herokuapp.com/api/playerList</a> to directly get the list of all the players with their corresponding ID</p>  <p><a href="https://trackmaniastats.herokuapp.com/api/cotd/<compID>">https://trackmaniastats.herokuapp.com/api/cotd/<compID></a> get the gloabl result of a cotd (compID can be found on trackmania.io)</p> </body></html>")




@app.route('/api/playerList')
def playerList(compID):
    
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


@app.route('/api/searchPlayer/<playerName>')
def searchPlayer(playerName):
    
    playerID = api.searchPlayerByName(playerName)
    
    if playerID == "":
        playerID = "Sorry, player not found."
        
    return playerID

@app.route('/api/cotd/<compID>')
def cotd(compID):
    
    fileName = 'json/cotd/cotd-' + compID + '.json'
    
    with open(fileName,'r') as json_file:
       cotdJSON = json.load(json_file)

    return cotdJSON


@app.route('/api/updateCOTD/fetchLatest/<pwd>')
def fetchLatest(pwd):
    if pwd == "verySecuredPWD":
        result = api.createLatestcotdJSON()
        return result
    else:
        return "wrong password"

@app.route('/api/updatePlayers/<pwd>')
def updatePlayers(pwd):
    if pwd == "verySecuredPWD":
        api.updatePlayersProfile(api.getLatestFinishedcotdID())
    else:
        return "wrong password"


@app.route('/api/sortPlayerList/<pwd>')
def sortPlayerList(pwd):
    if pwd == "verySecuredPWD":
        api.sortAlphabeticalOrder()
    else:
        return "wrong password"
    
    
    
    
    
    
if __name__ == "__main__":
    app.run(debug=True)

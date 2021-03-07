# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 17:12:05 2021

@author: Flirno
"""

import urllib.request, json 
import time
"""
import os
import copy
import math
"""
from os import path
from datetime import date
from os import listdir
from os.path import isfile, join
#from github import Github

#------------------------------------------FUNCTIONS---------------------------------------------------#


def getJsonFromURL(url):
    req = urllib.request.Request(url) 
    req.add_header('User-Agent', 'Flirno COTD')
    resp = urllib.request.urlopen(req).read().decode()  
    page = json.loads(resp)
    return(page)


#return the position of every player of a given cotd with the form a list like 
#[[serverRank, globaRank, Pseudo, playerID], [...], ...]
#IS WORKING
def getCOMPresults(compID):
    url = "https://trackmania.io/api/comp/" + compID
    page = getJsonFromURL(url)
    
    resultsList = []
    
    matches = page.get("rounds")[0].get("matches")
    i = 0
    u = 1
    addedID = []
    
    for match in matches:
        url = "https://trackmania.io/api/comp/"+ str(compID) +"/results/" + str(match.get("id")) + "/" + str(i)
        print(url)
        results = getJsonFromURL(url)
        results = results.get("results")
        
    
        while results != []:
    
            for player in results:
                #sometimes it servers can bug...
                if player.get("accountid") in addedID:
                        pass
                    
                else:
                    if player.get("position") != 0:
                        resultsList += [[player.get("position"), u, player.get("displayname"), player.get("accountid")]]
                    else:
                        resultsList += [["DNF", u, player.get("displayname"), player.get("accountid")]]
                    
                    addedID += [player.get("accountid")]
                
                u += 1
            
            i+=1
            
            url = "https://trackmania.io/api/comp/"+ str(compID) +"/results/" + str(match.get("id")) + "/" + str(i)
            print(url)
            results = getJsonFromURL(url)
            results = results.get("results")
            time.sleep(0.1) #prevent overload of Miss' server
            #print(resultsList)
            
        print(match.get("name"),"done!")
        i = 0
    
    #totdInfo = getJsonFromURL("https://trackmania.io/api/totd/0")
    

    totdInfo = [page.get("id"), page.get("name")[15:], page.get("numplayers")]
    
    return (totdInfo,resultsList)


#NOT NECESSARY ANYMORE BECAUSE ID ALREADY IN /api/cotd/0
"""
def getCOTDresults(compID):
    url = "https://trackmania.io/api/comp/" + compID
    
    page = getJsonFromURL(url)
    name = page.get("name")
    #print(type(data),data,type(name),name)
        
    if "Cup of the Day" in name:
        results = getCOMPresults(page)
        return results
   
    else:
        pass
"""

#For first initialising or hard database reset only
def getAllCOTDcompID():
    u = 0
    
    cotdPage = getJsonFromURL("https://trackmania.io/api/cotd/0")
    COTDcompIDList = []
    
    while cotdPage.get("competitions") != []:
        
        for COTDcomp in cotdPage.get("competitions"):
            COTDcompIDList += [str(COTDcomp.get("id"))]
        
        u += 1
        cotdPage = getJsonFromURL("https://trackmania.io/api/cotd/" + str(u))
    
        time.sleep(0.1) #prevent overload of Miss' server
    return (COTDcompIDList)




def getLatestFinishedcotdID():
    cotd = getJsonFromURL("https://trackmania.io/api/cotd/0")
    
    #print("COTD over")
    i=0
    found =  False
    while cotd.get("competitions")[i].get("players") == 0 or found == False:
        
        compID = cotd.get("competitions")[i].get("id")
        checkcotd = getJsonFromURL("https://trackmania.io/api/comp/"+ str(compID) )
        if checkcotd.get('rounds')[0].get('matches') == []:
            pass
        else:
            print(compID,"check")
            if verifIfOver(str(compID)):
                found = True
                print("Over")
            else:
                pass
            
        #time.sleep(0.1)
        #print(compID)
        i+=1
    
    return str(compID)


def verifIfOver(compID):
    checkcotd = getJsonFromURL("https://trackmania.io/api/comp/"+compID)
    for match in checkcotd["rounds"][0]["matches"]:
        #print(match["completed"])
        if match["completed"] == False:
            return False
        else:
            pass
    return True
    
    
#--------------------------------------------for local use----------------------------------------------



def addToPlayerList(player):  
    playerName = player.get("playerName").lower()
    
    playerListName = 'json/playerList.json'
    
    with open(playerListName,'r') as json_file:
        playerProfile = json.load(json_file)
    
    if playerName not in playerProfile:
        print("new name in playerList", player.get("playerName").lower())
        #As we know this player already has a profile, we'll keep previous Name and store same id for 2 different name, this will be useful to search a player if we only know their pseudo from a long time ago
        print(player.get("playerID"))
        print("Saving new name in playerList")
        playerProfile[playerName] = player.get("playerID")
                
        with open(playerListName, 'w') as outfile:
            json.dump(playerProfile, outfile)
                    
            
    #if there is a copycat (same login / different ID)
    if (playerName in playerProfile) and player.get("playerID") != playerProfile[playerName]:
                
        p = 1
        out = False
        while (playerName + '(' + str(p) + ')') in playerProfile and out == False:
            #print("here",(playerName + '(' + str(p) + ')') in playerProfile, out == False )
            #print(playerName + '(' + str(p) + ')')
            if player.get("playerID") != playerProfile[playerName + '(' + str(p) + ')']:
                p+=1
            else:
                out = True
                
        if out == False:
            playerProfile[playerName + '(' + str(p) + ')'] = player.get("playerID")
                
            with open(playerListName, 'w') as outfile:
                json.dump(playerProfile, outfile)

"""
def OPENaddToPlayerList(player):  
    playerName = player.get("nameOnPlatform").lower()
    
    playerListName = 'json/playerList.json'
    
    with open(playerListName,'r') as json_file:
        playerProfile = json.load(json_file)
    
    if playerName not in playerProfile:
        #print("new name in playerList", player.get("nameOnPlatform").lower())
        #As we know this player already has a profile, we'll keep previous Name and store same id for 2 different name, this will be useful to search a player if we only know their pseudo from a long time ago
        #print(player.get("accountId"))
        print("Saving new name in playerList")
        playerProfile[playerName] = player.get("accountId")
                
        with open(playerListName, 'w') as outfile:
            json.dump(playerProfile, outfile)
                    
            
    #if there is a copycat (same login / different ID)
    if (playerName in playerProfile) and player.get("accountId") != playerProfile[playerName]:
        print("copy-pasta")
        p = 1
        out = False
        while (playerName + '(' + str(p) + ')') in playerProfile and out == False:
            #print("here",(playerName + '(' + str(p) + ')') in playerProfile, out == False )
            #print(playerName + '(' + str(p) + ')')
            if player.get("accountId") != playerProfile[playerName + '(' + str(p) + ')']:
                p+=1
            else:
                out = True
                
        if out == False:
            playerProfile[playerName + '(' + str(p) + ')'] = player.get("accountId")
                
            with open(playerListName, 'w') as outfile:
                json.dump(playerProfile, outfile)

def getOpenTrackmaniaPlayers():    
    page = getJsonFromURL("https://api.opentrackmania.com/players/rankings")
    
    players = page[0]['players']
    
    path = "json/openTrackmaniaPlayers.json"
    
    with open(path, 'w') as outfile:
        json.dump(players, outfile)
    

def addOpenTrackmaniaPlayers():
    today = str(date.today())
    
    file = "json/openTrackmaniaPlayers.json"
            
    with open(file,'r') as json_file:
        players = json.load(json_file)
    
    #playerListName = 'json/playerList.json'
            
    
    for player in players: 
    
        #with open(playerListName,'r') as json_file:
            #playerList = json.load(json_file)
        
        #print(player["nameOnPlatform"], " : ", player["accountId"])
                        
        fileName = 'json/playerProfiles/'+ player["accountId"] + '.json'
        
        
        if path.exists(fileName): #add new name if necessary 
            pass
            #print("player profile already exist")
    
            
        else:  #create Profile with cotd results empty
            print(player["nameOnPlatform"], " : ", player["accountId"])
            print("is NEW from opentrackmania")
           
            data = {}
            data['playerID'] = player.get("accountId")
            data['playerNames'] = []
            data['playerNames'].append({'playerName' : player.get("nameOnPlatform"),
                                        'sinceDate' : today
                                              
            })
            data['results'] = {}
            data['results']['cotd'] = []   
                 
            with open(fileName, 'w') as outfile:
                json.dump(data, outfile)
            
            OPENaddToPlayerList(player)
                         
            

def deleteOPENtrackmaniaPlaers():
    playerListName = 'json/playerList.json'
    
    with open(playerListName,'r') as json_file:
        playerList = json.load(json_file)
        
    
    for playerID in playerList.values():

        #playerID = player["accountId"]
        fileName = "json/playerProfiles/"+playerID+".json"
        
        with open(fileName,'r') as json_file:
            playerProfile = json.load(json_file)
        
        
        if playerProfile["results"]["cotd"]==[]:
            #print(path.exists(fileName))
            print(playerID)
            #os.remove(fileName)
            #print(path.exists(fileName))
        
#deleteOPENtrackmaniaPlaers()


def delOpenfromPlayerList():
    playerListName = 'json/playerList.json'
    
    with open(playerListName,'r') as json_file:
        playerList = json.load(json_file)
    
    newPlayerList = copy.deepcopy(playerList)
    print(len(playerList))
    
    for playerName in playerList:
        playerID = playerList[playerName]
        fileName = "json/playerProfiles/"+playerID+".json"
        if not(path.exists(fileName)):
            print("llol")
        else:
            print("exist")
            
delOpenfromPlayerList()
"""

def my_max_by_weight(sequence):
    if not sequence:
        raise ValueError('empty sequence')

    maximum = sequence[0]

    for item in sequence:
        # Compare elements by their weight stored
        # in their second element.
        if item[1] > maximum[1]:
            maximum = item

    return maximum

def SortTheALL(All):
    
    newAll = []
    
    for element in All:
        #print(newAll, element)
        if newAll==[]:
            newAll += [element]
        else:
            i=0
            #print(element[0])
            #print(newAll[i][0])
            while i < len(newAll) and element[0] > newAll[i][0]:
                i += 1

            if i < len(newAll) and element[0] == newAll[i][0]:
                while i < len(newAll) and  element[1] < newAll[i][1] and element[0] == newAll[i][0]:
                    i+=1

            newAll.insert(i, element)
            

    return newAll

def createCOTDRankingLastxCOTD():
    
    fileName = "json/COTDRankingCompleteStep10.json"
    
    with open(fileName,'r') as json_file:
        COTDRankings = json.load(json_file)
        
    alldata = COTDRankings
    alldata["last"] = {}
    

    playerListName = 'json/playerList.json'
    
    with open(playerListName,'r') as json_file:
        playerList = json.load(json_file)
    
    alldata = {'last':{}}
    I = [10*i for i in range(1,15)]

    for i in range(14):
        x = I[i]
        #10% best and worst remove
        toRemove = int(x*0.1)
        #print(toRemove)
        
            
        data = []
        total = 0
    
        doneID = []
        for playerName in playerList:
            total+=1
            totalPlacement = 0
            totalPlayers = 0 
        
            playerID = playerList[playerName]
            All = []
            
            if  playerID not in doneID:
                doneID += [playerID]
                fileName = 'json/playerProfiles/' + playerID + '.json'
                
                
                with open(fileName,'r') as json_file:
                    playerProfile = json.load(json_file)    
                    
                playerName = playerProfile['playerNames'][-1]['playerName']
                
                if len(playerProfile["results"]["cotd"]) >= x:
                    for result in playerProfile["results"]["cotd"][-1:-(x+1):-1]:

                        All += [[result["globalRank"],result["totalPlayer"]]]
                        

                    All = SortTheALL(All)
                    #print(All)
                    #print(All[0:x])
                    #add results
                    #print(All)
                    for element in All[0:x]:
                        totalPlacement += element[0]
                        totalPlayers += element[1]
                    #print(totalPlacement,totalPlayers)
                        
                    #remove for mean
                    for i in range(toRemove):
                        #if playerName == "aTTaX.GranaDy":
                            #print(totalPlacement,totalPlayers)
                        totalPlacement -= All[i][0] + All[(-i)+(x-1)][0]
                        totalPlayers -= All[i][1] + All[(-i)+(x-1)][1]
                        
                    #print(totalPlacement,totalPlayers)
                      
                    averagePosition = round(totalPlacement / (x-(2*toRemove)),3)
                    averagePositionRelative = round((totalPlacement/totalPlayers)*100,3)
                    #playerPoint = ((totalPlacement)/(totalPlayers))*totalNumberOfCOTD
        
                    data += [[('playerName',playerName),("averagePosition", averagePosition),("averagePositionRelative", averagePositionRelative)]]
                    
                    print(total," / ", len(playerList) ,"done")
        
        data = sorted(data, key=lambda x: x[2][1])
        #print(data)
        dataa = []

        for player in data:
            dataa += [dict(player)]
        
        alldata["last"][str(I[i])] = dataa
        
        print(x,'finished')
        
    
    #print(dataa)
    fileName = "json/COTDRankingCompleteStep10.json"
    with open(fileName, 'w') as outfile:
        json.dump(alldata, outfile)

#createCOTDRankingLastxCOTD()



def createCOTDRankingBestxCOTD():
    
    fileName = "json/COTDRankingCompleteStep10.json"
    
    with open(fileName,'r') as json_file:
        COTDRankings = json.load(json_file)
        
    alldata = COTDRankings
    alldata["best"] = {}
    
    playerListName = 'json/playerList.json'
    
    with open(playerListName,'r') as json_file:
        playerList = json.load(json_file)
    
    
    I = [10*i for i in range(1,15)]

    for i in range(14):
        x = I[i]
        #10% best and worst remove
        toRemove = int(x*0.1)
        #print(toRemove)
        
        data = []
        total = 0
    
        doneID = []
        for playerName in playerList:
            total+=1
            totalPlacement = 0
            totalPlayers = 0 
        
            playerID = playerList[playerName]
            All = []
            
            if  playerID not in doneID:
                doneID += [playerID]
                fileName = 'json/playerProfiles/' + playerID + '.json'
                
                
                with open(fileName,'r') as json_file:
                    playerProfile = json.load(json_file)    
                    
                playerName = playerProfile['playerNames'][-1]['playerName']
                
                if len(playerProfile["results"]["cotd"]) >= x:
                    
                    for result in playerProfile["results"]["cotd"]:

                        All += [[result["globalRank"],result["totalPlayer"]]]
                    
                    #print(All)
                    #All = sorted(All)
                    All = SortTheALL(All)
                    #print(All)
                    #All = sorted(All, key=lambda x: x[1], reverse=True)
                    
                    #print(All)
                    
                    for element in All[0:x]:
                        totalPlacement += element[0]
                        totalPlayers += element[1]
                        
                    for i in range(toRemove):
                        #if playerName == "aTTaX.GranaDy":
                            #print(totalPlacement,totalPlayers)
                        totalPlacement -= All[i][0] + All[(-i)+(x-1)][0]
                        totalPlayers -= All[i][1] + All[(-i)+(x-1)][1]
                        
                    #print(totalPlacement)
                    #if playerName == "aTTaX.GranaDy":
                        #print(All,totalPlacement,totalPlayers,x,toRemove,round(totalPlacement / (x-(2*toRemove)),3))
                        
                    averagePosition = round(totalPlacement / (x-(2*toRemove)),3)
                    averagePositionRelative = round((totalPlacement/totalPlayers)*100,3)
                    #playerPoint = ((totalPlacement)/(totalPlayers))*totalNumberOfCOTD
                    
                    data += [[('playerName',playerName),("averagePosition", averagePosition),("averagePositionRelative", averagePositionRelative)]]
        
                    print(total," / ", len(playerList) ,"done")
        
        data = sorted(data, key=lambda x: x[2][1])
        #print(data)
        dataa = []

        for player in data:
            dataa += [dict(player)]
        
        alldata["best"][str(I[i])] = dataa
        
        print(x,'finished')
        
    
    #print(dataa)
    fileName = "json/COTDRankingCompleteStep10.json"
    with open(fileName, 'w') as outfile:
        json.dump(alldata, outfile)

#createCOTDRankingBestxCOTD()



def updatePlayersProfile(compID):
    #compID is str
    fileName = 'json/cotd/cotd-'+ compID + '.json'

    with open(fileName,'r') as json_file:
       cotdJSON = json.load(json_file)
       
    #print(type(cotdJSON))
    
    
    players = cotdJSON.get("players")
    
    
    #today = str(date.today())
    #today = "2021-02-25"
    today = cotdJSON.get("date")
    
    #print("Today's date:", today)
    file = open("json/newCOTDPlayers.json","r+")
    file.truncate(0)
    file.close()
    
    file = open("json/newNamePlayers.json","r+")
    file.truncate(0)
    file.close()
    
    newCOTDPlayers = {}
    newNamePlayers = {}
    
    for player in players:
        
        fileName = 'json/playerProfiles/'+ player.get("playerID") + '.json'
        
        if path.exists(fileName): #the player already played at least one cotd before
                   
            
            with open(fileName,'r') as json_file:
                playerProfile = json.load(json_file)
            
            #print(playerProfile)
            #print(type(playerProfile))
            
            data = {}
            
            data['playerID'] = player.get("playerID")
            
            nameList = playerProfile.get('playerNames')
            data['playerNames'] = nameList
            
            
            
            #Update player name if necessary (in comparaison with the latest one used)
            #for i in range(len(nameList)):
            if nameList[-1].get('playerName') == player.get("playerName"):
                same =  True
            else:
                same = False
            
            

            if same == False:
                print("NEW NAME for : ", player.get("playerName"))
                data['playerNames'].append({'playerName' : player.get("playerName"),
                                            'sinceDate' : today
                                              
                })
                
                #key = NEW and value = OLD
                newNamePlayers[player.get("playerName")] = data['playerNames'][-2]['playerName']
                
                
                
                
                
                
                
            #else:
                #print("Not new login")
            
            #add new results only if cotd was not already added (in case of bug)
            l=0
            for i in range(len(playerProfile.get('results').get('cotd'))):
                if cotdJSON.get("date") != playerProfile.get('results').get('cotd')[i].get('date'):
                    l+=1

            
            if l == len(playerProfile.get('results').get('cotd')):
                #print("doing something")
                #print("Updating player : ",player.get("playerID"))
                
                
                data['results'] = {}
                data['results']['cotd'] = []
                
                data['results']['cotd'] = playerProfile.get('results').get('cotd')

                #need to add results from oldest to newest to have them ordered
                data['results']['cotd'].append({
                    'date' : cotdJSON.get("date"),
                    'server' : player.get("server"),
                    'serverRank' : player.get("serverRank"),
                    'globalRank' : player.get("globalRank"),
                    'totalPlayer' : cotdJSON.get("totalPlayer")
                    })
                
                with open(fileName, 'w') as outfile:
                    json.dump(data, outfile)
                
            #else:
                #print("results already existing for player : ",player.get("playerID"))
            
            
            #add the new player profile in the playerList file if necessary
            addToPlayerList(player)

        else: #this is their firt cotd, create new profile
            print("New player : ",player.get("playerID"))
            
            data = {}
    
            data['playerID'] = player.get("playerID")
            
            data['playerNames'] = []
            data['playerNames'].append({'playerName' : player.get("playerName"),
                                        'sinceDate' : today
                                              
            })
            
        
            data['results'] = {}
            
            #print(data)
            
            data['results']['cotd'] = []
            
            #print(data)

            data['results']['cotd'].append({
                'date' : cotdJSON.get("date"),
                'server' : player.get("server"),
                'serverRank' : player.get("serverRank"),
                'globalRank' : player.get("globalRank"),
                'totalPlayer' : cotdJSON.get("totalPlayer")
                })
            
            
            #uploadFiletoPath(str(data),fileName)
            
        
            with open(fileName, 'w') as outfile:
                json.dump(data, outfile)
            
            newCOTDPlayers[player.get("playerName")] = player.get("playerID")
            
                    
            #add the new player to the playerList file  
            addToPlayerList(player)
    
    newCOTDPlayerspath = "json/newCOTDPlayers.json"
    
    with open(newCOTDPlayerspath, 'w') as outfile:
        json.dump(newCOTDPlayers, outfile)
        
    #Keep track of number of new players every Day
    numberNewPlayersPath = "json/newCOTDPlayersDays.json"
    
    with open(numberNewPlayersPath,'r') as json_file:
        newPlayersData = json.load(json_file)
        
    numberNewPlayers = len(newCOTDPlayers)
    #print(newPlayersData)
    newPlayersData[today] = numberNewPlayers
    #print(newPlayersData)
   
    with open(numberNewPlayersPath, 'w') as outfile:
        json.dump(newPlayersData, outfile)
        
    newNamePlayerspath = 'json/newNamePlayers.json'
    
    with open(newNamePlayerspath, 'w') as outfile:
        json.dump(newNamePlayers, outfile)
    
    #Keep track of pseudo change every Day
    newNamePlayersDaysPath = 'json/newNamePlayersDays.json'
    
    with open(newNamePlayersDaysPath,'r') as json_file:
        newNamePlayersDays = json.load(json_file)
    
    #print("")
    newNamePlayersDays[today] = newNamePlayers
    
    with open(newNamePlayersDaysPath, 'w') as outfile:
        json.dump(newNamePlayersDays, outfile)
    
    
    

def sortAlphabeticalOrder():
    
    fileName = 'json/playerList.json'

    with open(fileName,'r') as json_file:
       playerList = json.load(json_file)
    
    sortedPseudo = sorted(playerList.keys(), key=lambda x:x.lower())
    
    newplayerList = {}
    
    for pseudo in sortedPseudo:
        newplayerList[pseudo] = playerList[pseudo]
    
    with open(fileName,'w') as json_file:
        json.dump(newplayerList, json_file)
       
        
def writeCotdJSONoutput(totdInfo,playersList):
    
    data = {}
    
    data['compID'] = totdInfo[0]
    data['date'] = totdInfo[1]
    #data['Map'] = "test"
    data['totalPlayer'] = totdInfo[2]
    #data['totdTmioLink'] = "https://trackmania.io/#/totd/leaderboard/<leaderboarduid>/<mapUid>"
    
    data['players'] = []

    for player in playersList:
            data['players'].append({'server': ((player[1]-1)//64)+1,'serverRank': player[0],'globalRank': player[1], 'playerName': player[2], 'playerID': player[3]})
    

    with open('json/cotd/cotd-'+ str(totdInfo[0]) + '.json', 'w') as outfile:
        json.dump(data, outfile)
        

#--------------------------------------------for web use----------------------------------------------


#-------------------------FUNCTIONS ONLY FOR APP.PY--------------------------------------


def searchPlayerByName(playerName):
    
    
    fileName = 'json/playerList.json'

    with open(fileName,'r') as json_file:
       playerList = json.load(json_file)
    
    allIDs = [value  for key, value  in playerList.items() if playerName in key]
    pseudo = [key  for key, value  in playerList.items() if playerName in key]
    data = {}
    
    for i in range(len(allIDs)):
        data[pseudo[i]] = allIDs[i]

    return data
    
    """
    if playerName in playerList:
        playerID = playerList.get(playerName)
    else :
        playerID = ""    
        
    return (playerID)
    """

def totalPlayer():
    
    fileName = 'json/playerList.json'

    with open(fileName,'r') as json_file:
       playerList = json.load(json_file)
       
    number = len(playerList)
    
    data = {'totalPlayer':number}
    
    return data

def numberNewCOTDPlayers():
    fileName = 'json/newCOTDPlayers.json'

    with open(fileName,'r') as json_file:
       playerList = json.load(json_file)
       
    number = len(playerList)
    
    data = {'numberNewCOTDPlayers':number}
    
    return data
    

def newCOTDPlayers():
    fileName = 'json/newCOTDPlayers.json'

    with open(fileName,'r') as json_file:
       playerList = json.load(json_file)
       
    return playerList


def numberNewNamePlayers():
    fileName = 'json/newNamePlayers.json'

    with open(fileName,'r') as json_file:
       playerList = json.load(json_file)
       
    number = len(playerList)
    
    data = {'numberNewNamePlayers':number}
    
    return data
    
def newNamePlayers():
    fileName = 'json/newNamePlayers.json'

    with open(fileName,'r') as json_file:
       playerList = json.load(json_file)
       
    return playerList

def COTDRankings():
    fileName = "json/COTDRankingCompleteStep10.json"
    print(fileName)
    with open(fileName,'r') as json_file:
        COTDRankings = json.load(json_file)
    
    return COTDRankings



def cotdLatest():
    COTDcompID = getLatestFinishedcotdID()
    
    fileName = 'json/cotd/cotd-'+ COTDcompID + '.json'
    
    if path.exists(fileName):
        
        with open(fileName,'r') as json_file:
            cotdJSON = json.load(json_file)

        return cotdJSON
    else:
        return "COTD not added yet."
    
def dayLastAddedCOTD():
    mypath = 'json/cotd/'

    onlyfiles = [int(f[:].replace('.json','').replace('cotd-','')) for f in listdir(mypath) if isfile(join(mypath, f))]
   
    maxi = max(onlyfiles)

    fileName = 'json/cotd/cotd-'+ str(maxi) + '.json'

    with open(fileName,'r') as json_file:
        cotdJSON = json.load(json_file)
     
    dateMaxi = cotdJSON['date']
    
    data = {'dayLastAddedCOTD':dateMaxi}

    return(data)

def cotdResultsServers(playerID):
    
    fileName = 'json/playerProfiles/' + playerID + '.json'
    
    with open(fileName,'r') as json_file:
        playerProfile = json.load(json_file)
    
    data = {"servers":[]}
    A = []
    done = []
    
    serverL = []
    for server in playerProfile["results"]["cotd"]:
        serverL += [server["server"]]
    maxi = max(serverL)
    #print(maxi)
    n=1
    while n<=maxi:
        A += [[n,0,0,0]] #server, played, finished, averageposi
        n+=1
        done+=[n]
    
    for server in playerProfile["results"]["cotd"]:
        A[server["server"]-1][0] += 0
        A[server["server"]-1][1] += 1
        if server["serverRank"] == "DNF" and A[server["server"]-1][3] == 0:
            A[server["server"]-1][3] = server["serverRank"]
            
        elif server["serverRank"] != "DNF" and A[server["server"]-1][3] == "DNF":
            A[server["server"]-1][3] = server["serverRank"]
            A[server["server"]-1][2] += 1
            
        elif server["serverRank"] != "DNF" and A[server["server"]-1][3] != "DNF":
            A[server["server"]-1][3] += server["serverRank"]
            A[server["server"]-1][2] += 1

    #print(A) 
    for server in A:
        
        if server[1]!=0 and server[3]!="DNF":
            server[3] = round(server[3]/server[2],2)
        
        #print(type(data["servers"]))
        data["servers"] += [{"server":server[0], "iteration":server[1], "averagePosi":server[3]}]
    
    #print(A)
    #{"servers": [{"server":1, "iteration":0, "averagePosi":0},{"server":2, "iteration":3, "averagePosi":24}]}
    #print(data)
    
    return data 
    
"""
def createLatestcotdJSON():

    compID = str(getLatestFinishedcotdID())
    
    if not(checkFileExist(compID)):
        totdInfo, results = getCOMPresults(compID)
        #writeCotdJSONoutput(totdInfo, results)
        uploadCotdJSONoutput(totdInfo, results)
        
        return("DONE, now wait for heroku to deploy new githubbranche and update player profiles")
       
    
    return("cotd "+str(compID)+" already on github")

def testUpload():
    print("test")
    uploadFiletoPath("text",'json/test.txt')
    print("here")
"""   
#------------------------------------------CALLS------------------------------------------------------#


"""
getOpenTrackmaniaPlayers()
addOpenTrackmaniaPlayers()
sortAlphabeticalOrder()
"""

"""
compID = getLatestFinishedcotdID()
#compID = "246"
print(compID)

if verifIfOver(compID):
    print("over")
    totdInfo, results = getCOMPresults(compID)
    writeCotdJSONoutput(totdInfo, results)
    updatePlayersProfile(compID)
    sortAlphabeticalOrder()
   
else:
    print("not over")

createCOTDRankingLastxCOTD()
createCOTDRankingBestxCOTD()
"""
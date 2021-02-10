# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 17:12:05 2021

@author: Flirno
"""

import urllib.request, json 
import time
from os import path
from datetime import date   
from github import Github

#------------------------------------------FUNCTIONS---------------------------------------------------#


def substringINstring(substring,string):
    return substring in string



#IS WORKING
def getJsonFromURL(url):
       
    content = urllib.request.urlopen(url).read().decode()    
    page = json.loads(content)
    
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


def getLatestFinishedcotdID():
    cotd = getJsonFromURL("https://trackmania.io/api/cotd/0")
    i=0
    while cotd.get("competitions")[i].get("players") == 0:
        i+=1
        
    compID = cotd.get("competitions")[i].get("id")
    
    return str(compID)


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


def createLatestcotdJSON():
       compID = getLatestFinishedcotdID()
       
       fileName = 'json/cotd/cotd-'+ compID + '.json'
       
       if not(path.exists(fileName)):
              totdInfo, results = getCOMPresults(compID)
              #writeCotdJSONoutput(totdInfo, results)
              uploadCotdJSONoutput(totdInfo, results)



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
        


def updatePlayersProfile(compID):
    #compID is str
    fileName = 'json/cotd/cotd-'+ compID + '.json'

    with open(fileName,'r') as json_file:
       cotdJSON = json.load(json_file)
       
    #print(type(cotdJSON))
    
    
    players = cotdJSON.get("players")
    
    
    #today = str(date.today())
    today = "2021-02-09"
    
    #print("Today's date:", today)
    
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
            for i in range(len(nameList)):
                if nameList[i].get('playerName') == player.get("playerName"):
                    same =  True
                else:
                    same = False
            
            

            if same == False:
                print("NEW NAME for : ", player.get("playerName"))
                data['playerNames'].append({'playerName' : player.get("playerName"),
                                            'sinceDate' : today
                                              
                })
            
            #add new results only if cotd was not already added (in case of bug)
            l=0
            for i in range(len(playerProfile.get('results').get('cotd'))):
                if cotdJSON.get("date") != playerProfile.get('results').get('cotd')[i].get('date'):
                    l+=1

            
            if l == len(playerProfile.get('results').get('cotd')):
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
            
            
            
            #update the new player profile in the playerList file if necessary
            
            playerListName = 'json/playerList.json'
            
            with open(playerListName,'r') as json_file:
                playerProfile = json.load(json_file)
            
            
            playerName = player.get("playerName").lower()
            
            
            if playerName not in playerProfile:
                #As we know this player already has a profile, we'll keep previous Name and store same id for 2 different name, this will be useful to search a player if we only know their pseudo from a long time ago
                print("Saving new name in playerList")
                print(player.get("playerID"))
                
                
                playerProfile[playerName] = player.get("playerID")
                
                with open(playerListName, 'w') as outfile:
                    json.dump(playerProfile, outfile)
                    
                    
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
                    
            #else: #no need to update
                #print("playeraa already in playerList")
                
            
            
        else: #this is their firt cotd, create new profile
            #print("New player : ",player.get("playerID"))
            
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
            

            with open(fileName, 'w') as outfile:
                json.dump(data, outfile)
            
            #print(data)
            
            #add the new player to the playerList file  
            
            playerListName = 'json/playerList.json'
            
            playerName = player.get("playerName").lower()
            
            with open(playerListName,'r') as json_file:
                playerProfile = json.load(json_file)
                
            playerProfile[playerName] = player.get("playerID")
            
            with open(playerListName, 'w') as outfile:
                json.dump(playerProfile, outfile)
            
        

        
def searchPlayerByName(playerName):
    
    
    fileName = 'json/playerList.json'

    with open(fileName,'r') as json_file:
       playerList = json.load(json_file)
       
    if playerName in playerList:
        playerID = playerList.get(playerName)
    else :
        playerID = ""    
        
    return (playerID)
    

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
    
    


def uploadFiletoPath(data, path):
    g = Github("37dc2d66429fd7886413ea750afe8e250babdcc9")

    #repo = g.get_user().get_repo('TrackmaniaStats')
    repo = g.get_user().get_repo('pygithub-test')

    all_files = []
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file = file_content
            all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))

    #uplaod files to github
    if path in all_files:
        contents = repo.get_contents(path)
        repo.update_file(contents.path, "committing files", data, contents.sha, branch="master")
        print(path + ' UPDATED')
    else:
        repo.create_file(path, "committing files", data, branch="master")
        print(path + ' CREATED')
    

def uploadCotdJSONoutput(totdInfo,playersList):
    
    data = {}
    
    data['compID'] = totdInfo[0]
    data['date'] = totdInfo[1]
    data['totalPlayer'] = totdInfo[2]
    
    
    data['players'] = []

    for player in playersList:
            data['players'].append({'server': ((player[1]-1)//64)+1,'serverRank': player[0],'globalRank': player[1], 'playerName': player[2], 'playerID': player[3]})
    
    path = 'json/cotd/cotd-'+ str(totdInfo[0]) + '.json'
    
    data = str(data).replace("'",'"')
    
    uploadFiletoPath(str(data),path)
    

    
    
#------------------------------------------CALLS------------------------------------------------------#


#searchPlayerByName("riolu-tm")

#done one time
#COTDcompIDList = getAllCOTDcompID() 
#COTDcompIDList = ['205', '204', '203', '202', '201', '200', '199', '197', '196', '195', '193', '192', '190', '189', '188', '187', '186', '182', '178', '174', '173', '172', '165', '164', '163', '161', '159', '158', '157', '156', '155', '154', '151', '149', '148', '144', '142', '140', '139', '138', '136', '133', '132', '131', '130', '129', '128', '127', '126', '123', '122', '121', '119', '118', '116', '113', '109', '107', '105', '104', '103', '101', '100', '99', '98', '97', '96', '94', '92', '91', '90', '84', '81', '76', '75', '74', '73', '71', '70', '69', '66', '65', '62', '61', '59', '58', '57', '56', '55', '53', '52', '51', '49', '48', '47', '45', '44', '42', '41', '40']

#sortAlphabeticalOrder()

#print(len(COTDcompIDList))

#COTDcompIDList = COTDcompIDList #Latest to newest

#compID = getLatestFinishedcotdID()
#print(COTDcompIDList[:-6:-1])

#for compID in COTDcompIDList[-50::-1]:
    #print(compID)
    
    #cotdFile = 'json/cotd/cotd-' + compID + '.json'
    
    #if not(path.exists(cotdFile)):
#GATHER INFORMTAIONS FROM TRACKMANIA.IO
       #print("Fetching results of cotd which compID is :",compID)
#totdInfo, results = getCOMPresults("204")

#@uploadCotdJSONoutput(totdInfo,results)

#CREATE ORDERED PLAYER LIST
        #writeCotdJSONoutput(totdInfo, results)


#for compID in COTDcompIDList[1:5:]:
#UPDATE EVERY SINGLE PLAYER PROFILE
    #updatePlayersProfile(compID)

    
#sauvegarder pour l'accout ID, à chaque nouvelle cotd les pseudo correspondant aux account ID est mis à jour









# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 21:19:17 2021

@author: Thomas
"""

import urllib.request, json 
from os import listdir
from os.path import isfile, join

mypath = 'json/cotd/'

onlyfiles = [int(f[:].replace('.json','').replace('cotd-','')) for f in listdir(mypath) if isfile(join(mypath, f))]
   
maxi = max(onlyfiles)

fileName = 'json/cotd/cotd-'+ str(maxi) + '.json'

with open(fileName,'r') as json_file:
    cotdJSON = json.load(json_file)
     
dateMaxi = cotdJSON['date']

print(dateMaxi)
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 18:33:16 2021

@author: Flirno
"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/home")
@app.route("/index")
def hello():
    return ("<!DOCTYPE html><html><head><title>TrackmaniaStats</title></head><body><h1>Welecome to the TrackmaniaStats api</h1><h2>Available endpoint :</h2></body></html>")

if __name__ == "__main__":
    app.run(debug=True)

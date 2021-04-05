from flask import Flask, request, Markup, render_template, flash, Markup
import os
import json

app = Flask(__name__)

@app.route("/")
def render_main():
    return render_template('home.html')

@app.route("/pop")
def render_pop_games():
    return render_template('popGame.html', options=get_years())

@app.route("/popGame")
def render_game_info():
    year_chosen = request.args['games']
    return render_template('popGame.html', options=get_years(), gameData=get_game_data(year_chosen))

def get_years():
    listOfYears = []
    with open('video_games.json') as vG_data:
        videos = json.load(vG_data)
    for video in videos:
        if video["Release"]["Year"] not in listOfYears:
            listOfYears.append(video["Release"]["Year"])
    options = ""
    for year in listOfYears:
        options = options + Markup("<option value=\"" + str(year) + "\">" + str(year) + "</option>")
    return options

def get_game_data(year):
    with open('video_games.json') as vG_data:
        videos = json.load(vG_data)
    high_rate = 0
    name = ""
    for game in videos:
        if game["Release"]["Year"] == year and game["Metrics"]["Review Score"] > high_rate:
            high_rate = game["Metrics"]["Review Score"]
            name = game["Title"]
    game_dat = "The most popular game of " + str(year) + " was " + name + " with a metacritic score of " + str(high_rate) + " out of 100."
    return game_dat

if __name__=="__main__":
    app.run(debug=False, port=54321)

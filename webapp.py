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

def get_game_data(yr):
    with open('video_games.json') as vG_data:
        videos = json.load(vG_data)
    high_rate = 0
    pt = 0
    np = 0
    nm = ""
    nm2 = ""
    for game in videos:
        if (game["Release"]["Year"] == int(yr)) and (game["Metrics"]["Review Score"] > high_rate):
            high_rate = game["Metrics"]["Review Score"]
            nm = game["Title"]
    for game in videos:
        if (game["Release"]["Year"] == int(yr)) and (game["Length"]["All PlayStyles"]["Average"] > pt):
            pt = game["Length"]["All PlayStyles"]["Average"]
            nm2 = game["Title"]
            np = game["Length"]["All PlayStyles"]["Polled"]
    game_dat = ("The most popular game of " + str(yr) + " was " + nm + " with a metacritic score of " + str(high_rate) + " out of 100." \ 
                + " The most played game of " + str(yr) + " was " + nm2 + " with an average playtime of " + str(pt) + " hours between " + str(np) + " users.")
    return game_dat

if __name__=="__main__":
    app.run(debug=False, port=54321)

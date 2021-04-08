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
    return render_template('popGame.html', options=get_years(), gameData=get_pop_game(year_chosen), gamePlay=get_played_game(year_chosen))

@app.route("/pub")
def render_pubs():
    return render_template('publisher.html', options=get_publishers())


@app.route("/pubGame")
def render_pub_info():
    pub_chosen = request.args['pubs']
    return render_template('publisher.html', options=get_publishers(), pubData=get_pub_game(pub_chosen))

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

def get_publishers():
    listOfPublishers = []
    with open('video_games.json') as vG_data:
        videos = json.load(vG_data)
    for video in videos:
        if (video["Metadata"]["Publishers"] not in listOfPublishers) and video["Metadata"]["Publishers"] != "":
            listOfPublishers.append(video["Metadata"]["Publishers"])
    options = ""
    for publish in listOfPublishers:
        options = options + Markup("<option value=\"" + publish + "\">" + publish + "</option>")
    return options

def get_pop_game(yr):
    with open('video_games.json') as vG_data:
        videos = json.load(vG_data)
    high_rate = 0
    nm = ""
    for game in videos:
        if (game["Release"]["Year"] == int(yr)) and (game["Metrics"]["Review Score"] > high_rate):
            high_rate = game["Metrics"]["Review Score"]
            nm = game["Title"]
    
    game_dat = "The most popular game of " + str(yr) + " was " + nm + " with a metacritic score of " + str(high_rate) + " out of 100." 
    return game_dat

def get_played_game(yr):
    with open('video_games.json') as vG_data:
        videos = json.load(vG_data)
    pt = 0
    np = 0
    nm = ""
    gnr = ""
    pub = ""
    cons = ""
    played_dat = ""
    vowels = ['A','E','I','O','U']
    for game in videos:
        if (game["Release"]["Year"] == int(yr)) and (game["Length"]["All PlayStyles"]["Average"] > pt):
            pt = game["Length"]["All PlayStyles"]["Average"]
            nm = game["Title"]
            np = game["Length"]["All PlayStyles"]["Polled"]
            gnr = game["Metadata"]["Genres"]
            pub = game["Metadata"]["Publishers"]
            cons = game["Release"]["Console"]
    if pub != "" and gnr[0] not in vowels:
        played_dat = ("The most played game of " + str(yr) + " was " + nm + " with an average playtime of " + str(pt) + " hours between " + str(np) + " users. " 
                      + nm + " is a " + gnr + " game published by " + pub + " for the " + cons + ".")
    elif pub != "" and gnr[0] in vowels:
        played_dat = ("The most played game of " + str(yr) + " was " + nm + " with an average playtime of " + str(pt) + " hours between " + str(np) + " users. " 
                      + nm + " is an " + gnr + " game published by " + pub + " for the " + cons + ".")
    elif pub == "" and gnr[0] not in vowels:
        played_dat = ("The most played game of " + str(yr) + " was " + nm + " with an average playtime of " + str(pt) + " hours between " + str(np) + " users. " 
                      + nm + " is a " + gnr + " game published for the " + cons + ".")
    elif pub == "" and gnr[0] in vowels:
        played_dat = ("The most played game of " + str(yr) + " was " + nm + " with an average playtime of " + str(pt) + " hours between " + str(np) + " users. " 
                      + nm + " is an " + gnr + " game published for the " + cons + ".")
    print(gnr[0])
    return played_dat

def get_pub_game(pb):
    with open('video_games.json') as vG_data:
        videos = json.load(vG_data)
    meta_review = 0
    count = 0
    for video in videos:
        if video["Metadata"]["Publishers"] == pb:
            meta_review = meta_review + video["Metrics"]["Review Score"]
            count = count + 1
    av_review = meta_review/count
    review_desc = pb + "'s average metacritic review score was " + av_review + " between " + count + " games."
    return review_desc

if __name__=="__main__":
    app.run(debug=False, port=54321)

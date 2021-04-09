from flask import Flask, request, Markup, render_template, flash, Markup
import os
import json

app = Flask(__name__)

@app.route("/")
def render_main():
    return render_template('home.html')

@app.route("/year")
def render_pop_games():
    return render_template('year.html', options=get_years())

@app.route("/popGame")
def render_game_info():
    year_chosen = request.args['games']
    return render_template('year.html', options=get_years(), gameData=get_pop_game(year_chosen), gamePlay=get_played_game(year_chosen))

@app.route("/pub")
def render_pubs():
    return render_template('publisher.html', options=get_publishers())

@app.route("/game")
def render_gms():
    return render_template('game.html', options=get_game())

@app.route("/gmGame")
def render_gm_info():
    gm_chosen = request.args['gms']
    return render_template('game.html', options=get_game(), gmData=get_gm_data(gm_chosen))

@app.route("/pubGame")
def render_pub_info():
    pub_chosen = request.args['pubs']
    return render_template('publisher.html', options=get_publishers(), pubData=get_pub_game(pub_chosen), pubSales=get_pub_sales(pub_chosen))

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

def get_game():
    listOfGames = []
    with open('video_games.json') as vG_data:
        videos = json.load(vG_data)
    for video in videos:
        if video["Title"] not in listOfGames:
            listOfGames.append(video["Title"])
    options = ""
    for gam in listOfGames:
        options = options + Markup("<option value=\"" + gam + "\">" + gam + "</option>")
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
    review_desc = pb + "'s average metacritic review score was " + str(av_review) + " between " + str(count) + " games."
    return review_desc

def get_pub_sales(pb):
    with open('video_games.json') as vG_data:
        videos = json.load(vG_data)
    sales = 0
    count = 0
    for video in videos:
        if video["Metadata"]["Publishers"] == pb:
            sales = sales + video["Metrics"]["Sales"]
            count = count + 1
    av_sales = sales/count
    sale_desc = pb + "'s total sales from 2004 until 2008 was $" + str(sales) + " million. " + pb + " sold $" + str(av_sales) + " million on average for each game it released."
    return sale_desc

def get_gm_data(gam):
    with open('video_games.json') as vG_data:
        videos = json.load(vG_data)
    gm_gnr = ""
    gm_rev = 0
    gm_pub = ""
    gm_cons = ""
    gm_yr = ""
    gm_rtg = ""
    gm_tm = 0
    vowels = ['A','E','I','O','U']
    for video in videos:
        if video["Title"] == gam:
            gm_gnr = video["Metadata"]["Genres"]
            gm_rev = video["Metrics"]["Review Score"]
            gm_pub = video["Metadata"]["Publishers"]
            gm_cons = video["Release"]["Console"]
            gm_yr = video["Release"]["Year"]
            gm_rtg = video["Release"]["Rating"]
            gm_tm = video["Length"]["All PlayStyles"]["Average"]
    if gm_gnr[0] not in vowels and gm_rtg[0] not in vowels:
        gm_desc = (gm + " is a " + gm_gnr + " game published by " + gm_pub + " for the " + gm_cons + ". It was originally released in " + gm_yr + " and is a " 
                   + gm_rtg + " rated game with a " + gm_rev + " review score.")
    elif gm_rtg not in vowels and gnr[0] in vowels:
        gm_desc = (gm + " is an " + gm_gnr + " game published by " + gm_pub + " for the " + gm_cons + ". It was originally released in " + gm_yr + " and is a " 
                   + gm_rtg + " rated game with a " + gm_rev + " review score.")
    elif gm_rtg in vowels and gnr[0] not in vowels:
        gm_desc = (gm + " is a " + gm_gnr + " game published by " + gm_pub + " for the " + gm_cons + ". It was originally released in " + gm_yr + " and is an " 
                   + gm_rtg + " rated game with a " + gm_rev + " review score.")
    elif gm_rtg in vowels and gnr[0] in vowels:
        gm_desc = (gm + " is an " + gm_gnr + " game published by " + gm_pub + " for the " + gm_cons + ". It was originally released in " + gm_yr + " and is an " 
                   + gm_rtg + " rated game with a " + gm_rev + " review score.")
    return gm_desc

if __name__=="__main__":
    app.run(debug=False, port=54321)

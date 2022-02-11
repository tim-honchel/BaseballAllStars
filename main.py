import os
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# create the web application


app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecret"


# each pitcher will be an object with statistical member fields
class Pitcher:

    position = ""
    name = ""
    war = 0
    era = 0
    whip = 0
    wins = 0
    saves = 0
    strikeouts = 0
    innings = 0
    description = ""


# each batter will be an object with statistical member fields
class Batter:

    position = ""
    name = ""
    war = 0
    avg = 0
    obp = 0
    slg = 0
    runs = 0
    hits = 0
    homeruns = 0
    rbi = 0
    steals = 0
    plate_appearances = 0
    owar = 0
    dwar = 0
    description = ""


# form to input time period
class Years_Form(FlaskForm):
    year_a = StringField("Enter the starting year of the time period: ")
    year_b = StringField("Enter the ending year of the time period: ")
    submit = SubmitField("Search this time period")

# scrape each Fangraphs page and create a batter object for each row
def generate_batters(urls):
    batters = []
    for url in urls:
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html5lib')
        table = soup.find(id="LeaderBoard1_dg1_ctl00")
        position = url.split("pos=", 1)[1].split("&", 1)[0].upper()
        num_rows = 4
        for row_num in range(0, num_rows):
            raw_row = str(table.find(id=f"LeaderBoard1_dg1_ctl00__{row_num}"))
            raw_row_split = raw_row.split("</td>")
            col_num = 0
            batter = Batter()
            for raw_column in raw_row_split:
                if col_num == 0 or col_num == 2 or col_num == 15:
                    0
                if col_num == 1:
                    batter.name = raw_column.split(">", 1)[1].split(">", 1)[1].split("<", 1)[0]
                if col_num == 3:
                    batter.war = raw_column.split(">", 1)[1]
                if col_num == 4:
                    batter.avg = raw_column.split(">", 1)[1]
                if col_num == 5:
                    batter.obp = raw_column.split(">", 1)[1]
                if col_num == 6:
                    batter.slg = raw_column.split(">", 1)[1]
                if col_num == 7:
                    batter.hits = raw_column.split(">", 1)[1]
                if col_num == 8:
                    batter.runs = raw_column.split(">", 1)[1]
                if col_num == 9:
                    batter.homeruns = raw_column.split(">", 1)[1]
                if col_num == 10:
                    batter.rbi = raw_column.split(">", 1)[1]
                if col_num == 11:
                    batter.steals = raw_column.split(">", 1)[1]
                if col_num == 12:
                    batter.plate_appearances = raw_column.split(">", 1)[1]
                if col_num == 13:
                    batter.owar = raw_column.split(">", 1)[1]
                if col_num == 14:
                    batter.dwar = raw_column.split(">", 1)[1]
                col_num += 1
            batter.position = position
            batter.description = f"{batter.position} {batter.name} ({batter.war} WAR) - {batter.avg}/{batter.obp}/{batter.slg}, {batter.runs} R, {batter.hits} H, {batter.homeruns} HR, {batter.rbi} RBI, {batter.steals} SB"
            if batter.name != "":
                batters.append(batter)
    return batters


# scrape each Fangraphs page and create a pitcher object for each row
def generate_pitchers(urls):
    pitchers = []
    for url in urls:
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html5lib')
        table = soup.find(id="LeaderBoard1_dg1_ctl00")
        position = url.split("stats=", 1)[1].split("&", 1)[0].upper()
        if position == "PIT":
            position = "SP"
        if position == "REL":
            position = "RP"
        num_rows = 9
        for row_num in range(0, num_rows):
            raw_row = str(table.find(id=f"LeaderBoard1_dg1_ctl00__{row_num}"))
            raw_row_split = raw_row.split("</td>")
            col_num = 0
            pitcher = Pitcher()
            for raw_column in raw_row_split:
                if col_num == 0 or col_num == 2 or col_num == 10:
                    0
                if col_num == 1:
                    pitcher.name = raw_column.split(">", 1)[1].split(">", 1)[1].split("<", 1)[0]
                if col_num == 3:
                    pitcher.war = raw_column.split(">", 1)[1]
                if col_num == 4:
                    pitcher.era = raw_column.split(">", 1)[1]
                if col_num == 5:
                    pitcher.whip = raw_column.split(">", 1)[1]
                if col_num == 6:
                    pitcher.wins = raw_column.split(">", 1)[1]
                if col_num == 7:
                    pitcher.saves = raw_column.split(">", 1)[1]
                if col_num == 8:
                    pitcher.strikeouts = raw_column.split(">", 1)[1]
                if col_num == 9:
                    pitcher.innings = raw_column.split(">", 1)[1]
                col_num += 1
            pitcher.position = position
            pitcher.description = f"{position} {pitcher.name} ({pitcher.war} WAR) - {pitcher.era} ERA, {pitcher.whip} WHIP, {pitcher.wins} W, {pitcher.saves} SV, {pitcher.strikeouts} K"
            if pitcher.name != "":
                pitchers.append(pitcher)
    return pitchers


# display each player's description
def display_players(players):
    for player in players:
        print(player.description)

@app.route("/index", methods=["GET","POST"])
@app.route("/", methods=["GET","POST"])
def index():
    years_form = Years_Form(crsf_enabled=False)
    return(render_template("index.html", template_form=years_form))

@app.route("/loading", methods=["GET","POST"])
def loading():
    years_form = Years_Form(crsf_enabled=False)
    year1 = years_form.year_a.data
    year2 = years_form.year_b.data
    try:
        year1 = int(year1)
        if year1 < 1900 or year1 > 2021:
            return redirect("/")
    except ValueError:
        return redirect("/")
    try:
        year2 = int(year2)
        if year2 < 1900 or year2 > 2021 or year2 < year1:
            return redirect("/")
    except ValueError:
        return redirect("/")
    return (render_template("loading.html", template_form=years_form, year1=year1, year2=year2))


@app.route("/considerations", methods=["GET","POST"])
def considerations():
    years_form = Years_Form(crsf_enabled=False)
    year1 = years_form.year_a.data
    year2 = years_form.year_b.data
    try:
        year1 = int(year1)
        if year1 < 1900 or year1 > 2021:
            return redirect("/")
    except ValueError:
        return redirect("/")
    try:
        year2 = int(year2)
        if year2 < 1900 or year2 > 2021 or year2 < year1:
            return redirect("/")
    except ValueError:
        return redirect("/")
    # Use string interpolation to create the Fangraphs URLs that show the top players at each position
    pitcher_urls = [
        f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=y&type=c,59,6,42,4,11,24,13&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_9&sort=3,d',
        f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=rel&lg=all&qual=y&type=c,59,6,42,4,11,24,13&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_7&sort=3,d'
    ]
    batter_urls = [
        f'https://www.fangraphs.com/leaders.aspx?pos=c&stats=bat&lg=all&qual=y&type=c,58,23,37,38,7,12,11,13,21,6,203,199&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_4&sort=3,d',
        f'https://www.fangraphs.com/leaders.aspx?pos=1b&stats=bat&lg=all&qual=y&type=c,58,23,37,38,7,12,11,13,21,6,203,199&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_4&sort=3,d',
        f'https://www.fangraphs.com/leaders.aspx?pos=2b&stats=bat&lg=all&qual=y&type=c,58,23,37,38,7,12,11,13,21,6,203,199&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_4&sort=3,d',
        f'https://www.fangraphs.com/leaders.aspx?pos=3b&stats=bat&lg=all&qual=y&type=c,58,23,37,38,7,12,11,13,21,6,203,199&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_4&sort=3,d',
        f'https://www.fangraphs.com/leaders.aspx?pos=ss&stats=bat&lg=all&qual=y&type=c,58,23,37,38,7,12,11,13,21,6,203,199&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_4&sort=3,d',
        f'https://www.fangraphs.com/leaders.aspx?pos=lf&stats=bat&lg=all&qual=y&type=c,58,23,37,38,7,12,11,13,21,6,203,199&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_4&sort=3,d',
        f'https://www.fangraphs.com/leaders.aspx?pos=cf&stats=bat&lg=all&qual=y&type=c,58,23,37,38,7,12,11,13,21,6,203,199&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_4&sort=3,d',
        f'https://www.fangraphs.com/leaders.aspx?pos=rf&stats=bat&lg=all&qual=y&type=c,58,23,37,38,7,12,11,13,21,6,203,199&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_4&sort=3,d',
        f'https://www.fangraphs.com/leaders.aspx?pos=dh&stats=bat&lg=all&qual=y&type=c,58,23,37,38,7,12,11,13,21,6,203,199&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_2&sort=3,d'
    ]
    pitchers = generate_pitchers(pitcher_urls)
    batters = generate_batters(batter_urls)
    return(render_template("considerations.html", year_start = year1, year_ending = year2, pitchers=pitchers, batters=batters))


if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    app.run(debug=False, host="0.0.0.0", port=port)
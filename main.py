from flask import Flask, render_template, redirect  # framework
from flask_wtf import FlaskForm  # for inputting years
from wtforms import StringField, SubmitField
import requests  # for getting HTML from websites
import asyncio  # for asynchronous web requests
from bs4 import BeautifulSoup  # for scraping HTML
import os  # required for deployment on Heroku


# creates the web application
app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecret"


# each pitcher will be an object with statistical member fields
class Pitcher:
    position = ""
    name = ""
    war = 0  # wins above replacement - an advanced metric for measuring a player's value
    era = 0  # earned run average
    whip = 0  # walks and hits per innings pitched
    wins = 0
    saves = 0
    strikeouts = 0
    innings = 0
    description = ""  # will be used to display player's information


# each batter will be an object with statistical member fields
class Batter:
    position = ""
    pos = 0  # numerical representation of the position
    pos_sort = 0  # when players have multiple positions, this will determine how they are sorted
    name = ""
    war = 0  # wins above replacement
    avg = 0  # batting average
    obp = 0  # on base percentage
    slg = 0  # slugging percentage
    runs = 0
    hits = 0
    homeruns = 0
    rbi = 0
    steals = 0
    plate_appearances = 0
    owar = 0  # contribution from offense
    dwar = 0  # contribution from defense
    description = ""  # will be used later


# form to input time period
class Years_Form(FlaskForm):
    year_a = StringField("Enter the starting year of the time period: ")
    year_b = StringField("Enter the ending year of the time period: ")
    submit = SubmitField("Search this time period")


# scrapes each Fangraphs page and creates 27 batter objects
def generate_batters(req, position):
    soup = BeautifulSoup(req.content, 'html5lib')  # stores HTML from website in a manipulable form
    table = soup.find(id="LeaderBoard1_dg1_ctl00")  # searches HTML for relevant section
    batters = []
    num_rows = 3  # number of players per position
    for row_num in range(0, num_rows):
        raw_row = str(table.find(id=f"LeaderBoard1_dg1_ctl00__{row_num}"))  # isolates each player's row
        raw_row_split = raw_row.split("</td>")  # splits data into columns
        col_num = 0
        batter = Batter()  # creates new Batter object
        batter.rank = row_num + 1
        for raw_column in raw_row_split:  # iterates through each column
            if col_num == 0 or col_num == 2 or col_num == 15:  # ignores irrelevant columns
                0
            if col_num == 1:
                batter.name = raw_column.split(">", 1)[1].split(">", 1)[1].split("<", 1)[0]  # manipulates HTML into the desired string
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
        positions = {"C":2, "1B":3, "2B":4, "3B":5, "SS":6, "LF":7, "CF":8, "RF":9, "DH":10}
        batter.pos = positions[batter.position]  # assigns numerical position
        batter.pos_sort = batter.pos
        batter.description = f"{batter.position} {batter.name} ({batter.war} WAR) - {batter.avg}/{batter.obp}/{batter.slg}, {batter.runs} R, {batter.hits} H, {batter.homeruns} HR, {batter.rbi} RBI, {batter.steals} SB"
        if batter.name != "":
            batters.append(batter)  # adds current batter to list of batters
    return batters


# scrapes each Fangraphs page and creates 16 pitcher objects (see similar comments in generate_batters function)
def generate_pitchers(req, position):
    pitchers = []
    soup = BeautifulSoup(req.content, 'html5lib')
    table = soup.find(id="LeaderBoard1_dg1_ctl00")
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
        if pitcher.position == "SP":
            pitcher.pos = 1
        if pitcher.position == "RP":
            pitcher.pos = 1.1
        pitcher.description = f"{position} {pitcher.name} ({pitcher.war} WAR) - {pitcher.era} ERA, {pitcher.whip} WHIP, {pitcher.wins} W, {pitcher.saves} SV, {pitcher.strikeouts} K"
        if pitcher.name != "":
            pitchers.append(pitcher)
    return pitchers


# checks to see if a player was in the top 3 at multiple positions
def check_for_duplicates(batters):
    for batter1 in batters:
        for batter2 in batters:
            if batter1.name == batter2.name and batter1.position != batter2.position:
                batter1 = choose_which_duplicate_to_keep(batter1, batter2, batters)
                batters.remove(batter2)  # deletes the duplicate
    return batters


# when there is a duplicate, determines a primary position that will best serve the team
def choose_which_duplicate_to_keep(batter1, batter2, batters):
    batter1.position = f"{batter1.position}/{batter2.position}"  # to indicate they play multiple positions
    batter1.description = f"{batter1.position} {batter1.name} ({batter1.war} WAR) - {batter1.avg}/{batter1.obp}/{batter1.slg}, {batter1.runs} R, {batter1.hits} H, {batter1.homeruns} HR, {batter1.rbi} RBI, {batter1.steals} SB"
    if batter2.rank == 1 and batter1.rank > 1 and batter2.pos != 10:
        batter1.pos = batter2.pos  # if they are the #1 ranked player at a position other than DH, they take that position
        batter1.rank = batter2.rank
    elif batter2.rank == 1 and batter1.rank == 1 and batter2.pos != 10:  # if they are ranked #1 at two positions...
        next_best_position1 = [player.war for player in batters if player.pos == batter1.pos and player.rank == 2]
        next_best_position2 = [player.war for player in batters if player.pos == batter2.pos and player.rank == 2]
        if next_best_position1 >= next_best_position2:  # compare the #2 ranked players at those positions
            batter1.pos = batter2.pos  # whichever #2 is weaker, that will be the player's primary position
            batter1.rank = batter2.rank
    elif batter2.pos == 2 and batter2.rank == 2 and batter1.rank != 1:  # if they are the #2 catcher, that takes priority
        batter1.pos = batter2.pos
        batter1.rank = batter2.rank
    elif batter1.pos == 10:  # if they play DH, their other position takes priority
        batter1.pos = batter2.pos
        batter1.rank = batter2.rank
    elif batter1.pos == 3 and batter2.pos != 10:  # if they play 1B, all other positions except DH take priority
        batter1.pos = batter2.pos
        batter1.rank = batter2.rank
    return batter1


# chooses 13 of the 27 batters to make the All Star team
def select_top_batters(batters):
    final_batters = []
    position_count = {2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}  # number of players selected for each numerical position
    for batter in batters:
        if (batter.rank == 1 and batter.pos != 10):  # selects the #1 ranked player at each position except DH
            final_batters.append(batter)
            position_count[batter.pos] = 1  # adds 1 to the position count
            batters.remove(batter)  # removes the selected player from the pool
    batters.sort(key=lambda x: -float(x.war))  # sorts the remaining batters in descending order by WAR
    while len(final_batters) < 8:  # if a player was the top ranked at multiple positions, it's possible that 8 starters were not selected
        for pos, count in position_count.items():
            if count == 0:
                search_pos = pos  # identifies the position(s) that are missing a starter
        cont = True
        for batter in batters:
            if batter.pos == search_pos and cont is True:  # finds the first (highest WAR) batter at the missing position
                final_batters.append(batter) # selects that player
                position_count[batter.pos] = 1
                batters.remove(batter)
                cont = False  # ends the search for that position
    for batter in batters:
        if batter.rank == 2 and batter.pos == 2:  # selects the #2 ranked catcher
            final_batters.append(batter)
            batters.remove(batter)
    reserves = 0  # the number of reserve spots filled (max 4)
    backup_infielder = False  # whether a backup infielder has been selected (required)
    backup_outfielder = False  # whether a backup outfielder has been selected (required)
    designated_hitter = False  # whether a designated hitter has been selected (not required, max 1)
    flex_reserves = 2  # the number of reserve spots available for any position (2 held for backup infielder and outfielder)
    while reserves < 4:  # iterates until all reserve spots are filled
        player = batters.pop(0)  # grabs the highest WAR remaining player and also removes them from the pool
        if (player.pos == 2 or player.pos == 3) and flex_reserves > 0:  # catchers and 1st basemen are only selected if flex spots are available
            final_batters.append(player)
            flex_reserves -= 1  # flex spots decrease by one
            reserves += 1
        if player.pos == 4 or player.pos == 5 or player.pos == 6:  # 2nd basemen, 3rd basemen, and shortstops
            if backup_infielder is False:  # selected automatically if there isn't already a backup infielder
                final_batters.append(player)
                backup_infielder = True
                reserves += 1
            elif backup_infielder is True and flex_reserves > 0:  # otherwise only if there's a flex spot
                final_batters.append(player)
                flex_reserves -= 1
                reserves += 1
        if player.pos == 7 or player.pos == 8 or player.pos == 9:  # left fielders, center fielders, and rightfielders
            if backup_outfielder is False:  # selected automatically if there isn't already a backup outfielder
                final_batters.append(player)
                backup_outfielder = True
                reserves += 1
            elif backup_outfielder is True and flex_reserves > 0:  # otherwise only if there's a flex spot
                final_batters.append(player)
                flex_reserves -= 1
                reserves += 1
        if player.pos == 10 and designated_hitter is False and flex_reserves > 0:  #designated hitter
            final_batters.append(player)  # only added if there isn't already a DH and a flex spot is open
            designated_hitter = True
            flex_reserves -= 1
            reserves += 1
    final_batters.sort(key=lambda x: (x.pos_sort, -float(x.war)))  # sorts All Stars by WAR, descending
    return final_batters


# chooses 12 of the 16 pitchers to make the All Star team
def select_top_pitchers(pitchers):
    final_pitchers = [pitchers.pop(11),pitchers.pop(10),pitchers.pop(9),pitchers.pop(4),pitchers.pop(3),pitchers.pop(2),pitchers.pop(1),pitchers.pop(0)]  # selects the top 3 relievers and top 5 starters by WAR
    pitchers.sort(key=lambda x: -float(x.war))  # sorts all remaining pitchers by WAR
    final_pitchers.append(pitchers.pop(3))  # selects the next 4 highest WAR pitchers
    final_pitchers.append(pitchers.pop(2))
    final_pitchers.append(pitchers.pop(1))
    final_pitchers.append(pitchers.pop(0))
    final_pitchers.sort(key=lambda x: (x.pos, -float(x.war)))  # sorts All Stars by WAR, descending
    return final_pitchers


# asynchronously request the HTML of 11 Fangraphs web pages, 1 for each position
async def request_pages(year1, year2):
    url_sp = f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=y&type=c,59,6,42,4,11,24,13&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_9&sort=3,d'
    url_rp = f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=rel&lg=all&qual=y&type=c,59,6,42,4,11,24,13&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_7&sort=3,d'
    url_c = f'https://www.fangraphs.com/leaders.aspx?pos=c&stats=bat&lg=all&qual=y&type=c,58,23,37,38,7,12,11,13,21,6,203,199&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_3&sort=3,d'
    url_1b = f'https://www.fangraphs.com/leaders.aspx?pos=1b&stats=bat&lg=all&qual=y&type=c,58,23,37,38,7,12,11,13,21,6,203,199&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_3&sort=3,d'
    url_2b = f'https://www.fangraphs.com/leaders.aspx?pos=2b&stats=bat&lg=all&qual=y&type=c,58,23,37,38,7,12,11,13,21,6,203,199&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_3&sort=3,d'
    url_3b = f'https://www.fangraphs.com/leaders.aspx?pos=3b&stats=bat&lg=all&qual=y&type=c,58,23,37,38,7,12,11,13,21,6,203,199&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_3&sort=3,d'
    url_ss = f'https://www.fangraphs.com/leaders.aspx?pos=ss&stats=bat&lg=all&qual=y&type=c,58,23,37,38,7,12,11,13,21,6,203,199&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_3&sort=3,d'
    url_lf = f'https://www.fangraphs.com/leaders.aspx?pos=lf&stats=bat&lg=all&qual=y&type=c,58,23,37,38,7,12,11,13,21,6,203,199&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_3&sort=3,d'
    url_cf = f'https://www.fangraphs.com/leaders.aspx?pos=cf&stats=bat&lg=all&qual=y&type=c,58,23,37,38,7,12,11,13,21,6,203,199&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_3&sort=3,d'
    url_rf = f'https://www.fangraphs.com/leaders.aspx?pos=rf&stats=bat&lg=all&qual=y&type=c,58,23,37,38,7,12,11,13,21,6,203,199&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_3&sort=3,d'
    url_dh = f'https://www.fangraphs.com/leaders.aspx?pos=dh&stats=bat&lg=all&qual=y&type=c,58,23,37,38,7,12,11,13,21,6,203,199&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_2&sort=3,d'
    loop = asyncio.get_event_loop()  # initiates a loop where tasks can be completed asynchronously
    future_sp = loop.run_in_executor(None, requests.get, url_sp)  # opens one of the Fangraphs pages
    future_rp = loop.run_in_executor(None, requests.get, url_rp)
    future_c = loop.run_in_executor(None, requests.get, url_c)
    future_1b = loop.run_in_executor(None, requests.get, url_1b)
    future_2b = loop.run_in_executor(None, requests.get, url_2b)
    future_3b = loop.run_in_executor(None, requests.get, url_3b)
    future_ss = loop.run_in_executor(None, requests.get, url_ss)
    future_lf = loop.run_in_executor(None, requests.get, url_lf)
    future_cf = loop.run_in_executor(None, requests.get, url_cf)
    future_rf = loop.run_in_executor(None, requests.get, url_rf)
    future_dh = loop.run_in_executor(None, requests.get, url_dh)
    html_sp = await future_sp  # saves the data from the Fangraphs page once it is fully loaded
    html_rp = await future_rp
    html_c = await future_c
    html_1b = await future_1b
    html_2b = await future_2b
    html_3b = await future_3b
    html_ss = await future_ss
    html_lf = await future_lf
    html_cf = await future_cf
    html_rf = await future_rf
    html_dh = await future_dh
    return html_sp, html_rp, html_c, html_1b, html_2b, html_3b, html_ss, html_lf, html_cf, html_rf, html_dh


# assembles the batter list by sending saved HTML through generate_batters function
def prep_batters(html_c, html_1b, html_2b, html_3b, html_ss, html_lf, html_cf, html_rf, html_dh):
    catchers = generate_batters(html_c, "C")
    first_basemen = generate_batters(html_1b, "1B")
    second_basemen = generate_batters(html_2b, "2B")
    third_basemen = generate_batters(html_3b, "3B")
    shortstops = generate_batters(html_ss, "SS")
    left_fielders = generate_batters(html_lf, "LF")
    center_fielders = generate_batters(html_cf, "CF")
    right_fielders = generate_batters(html_rf, "RF")
    designated_hitters = generate_batters(html_dh, "DH")
    batters = catchers + first_basemen + second_basemen + third_basemen + shortstops + left_fielders + center_fielders + right_fielders + designated_hitters
    return batters


# assembles the pitcher list by sending saved HTML through generate_pitchers function
def prep_pitchers(html_sp, html_rp):
    starters = generate_pitchers(html_sp, "SP")
    relievers = generate_pitchers(html_rp, "RP")
    pitchers = starters + relievers
    return pitchers


# the home page that launches initially
@app.route("/index", methods=["GET","POST"])
@app.route("/", methods=["GET","POST"])
def index():
    years_form = Years_Form(crsf_enabled=False)
    return(render_template("index.html", template_form=years_form))


# the page that displays while the data is being scraped
@app.route("/loading", methods=["GET","POST"])
def loading():
    years_form = Years_Form(crsf_enabled=False)
    year1 = years_form.year_a.data
    year2 = years_form.year_b.data
    try:
        year1 = int(year1)
        if year1 < 1900 or year1 > 2021:  # catches if the year entered was before 1900 or after 2021
            return redirect("/")
    except ValueError:  # catches if the year entered was not an integer
        return redirect("/")
    try:
        year2 = int(year2)
        if year2 < 1900 or year2 > 2021 or year2 < year1:
            return redirect("/")
    except ValueError:
        return redirect("/")
    return (render_template("loading.html", template_form=years_form, year1=year1, year2=year2))  # opens the loading page, sends the years


# the final page showing the All-Star team
@app.route("/roster", methods=["GET","POST"])
def roster():
    years_form = Years_Form(crsf_enabled=False)
    year1 = years_form.year_a.data  # gets the years from the form
    year2 = years_form.year_b.data
    outer_loop = asyncio.new_event_loop()  # creates a new loop in order to run tasks asynchronously
    asyncio.set_event_loop(outer_loop)  # sets that loop in motion
    html_sp, html_rp, html_c, html_1b, html_2b, html_3b, html_ss, html_lf, html_cf, html_rf, html_dh = outer_loop.run_until_complete(request_pages(year1, year2))  # calls request_pages function and waits until the loop is complete before returning values
    batters = prep_batters(html_c, html_1b, html_2b, html_3b, html_ss, html_lf, html_cf, html_rf, html_dh)  # parses HTML into batters
    pitchers = prep_pitchers(html_sp, html_rp)  # parses HTML into pitchers
    batters_unduplicated = check_for_duplicates(batters)  # consolidates players who appeared at multiple positions
    final_pitchers = select_top_pitchers(pitchers)  # selects the top 12 pitchers
    final_batters = select_top_batters(batters_unduplicated)  # selects the top 13 batters
    return (render_template("roster.html", year_start = year1, year_ending = year2, pitchers=final_pitchers, batters=final_batters))


# the page that displays if there is a timeout error
@app.route("/timeout", methods=["GET","POST"])
def timeout():
    years_form = Years_Form(crsf_enabled=False)
    return (render_template("timeout.html", template_form=years_form))


if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)  # for Heroku
    app.run(debug=False, host="0.0.0.0", port=port)

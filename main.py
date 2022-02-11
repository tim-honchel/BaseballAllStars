import webbrowser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import html5lib
from flask import Flask, jsonify

# create the web application
# app = Flask(__name__)


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
                match col_num:
                    case 0 | 2 | 15:
                        0
                    case 1:
                        batter.name = raw_column.split(">", 1)[1].split(">", 1)[1].split("<", 1)[0]
                    case 3:
                        batter.war = raw_column.split(">", 1)[1]
                    case 4:
                        batter.avg = raw_column.split(">", 1)[1]
                    case 5:
                        batter.obp = raw_column.split(">", 1)[1]
                    case 6:
                        batter.slg = raw_column.split(">", 1)[1]
                    case 7:
                        batter.hits = raw_column.split(">", 1)[1]
                    case 8:
                        batter.runs = raw_column.split(">", 1)[1]
                    case 9:
                        batter.homeruns = raw_column.split(">", 1)[1]
                    case 10:
                        batter.rbi = raw_column.split(">", 1)[1]
                    case 11:
                        batter.steals = raw_column.split(">", 1)[1]
                    case 12:
                        batter.plate_appearances = raw_column.split(">", 1)[1]
                    case 13:
                        batter.owar = raw_column.split(">", 1)[1]
                    case 14:
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
                match col_num:
                    case 0 | 2 | 10:
                        0
                    case 1:
                        pitcher.name = raw_column.split(">", 1)[1].split(">", 1)[1].split("<", 1)[0]
                    case 3:
                        pitcher.war = raw_column.split(">", 1)[1]
                    case 4:
                        pitcher.era = raw_column.split(">", 1)[1]
                    case 5:
                        pitcher.whip = raw_column.split(">", 1)[1]
                    case 6:
                        pitcher.wins = raw_column.split(">", 1)[1]
                    case 7:
                        pitcher.saves = raw_column.split(">", 1)[1]
                    case 8:
                        pitcher.strikeouts = raw_column.split(">", 1)[1]
                    case 9:
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


# MAIN BEGINS HERE

# Input and validate the historical range
print()
print("Generate a historical MLB all-star team for a select time period.".upper())
print()
year1 = 0
year2 = 0
while year1 < 1900 or year1 > 2021:
    year1 = input("Enter the starting year of the time period: ")
    try:
        year1 = int(year1)
        if year1 < 1900 or year1 > 2021:
            print("Invalid year.")
        break
    except ValueError:
        year1 = 0
        print("Invalid year.")
while year2 < 1900 or year2 > 2021 or year2 < year1:
    year2 = input("Enter the ending year of the time period: ")
    try:
        year2 = int(year2)
        if year2 < 1900 or year2 > 2021 or year2 < year1:
            print("Invalid year.")
        break
    except ValueError:
        print("Invalid year")

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

print()
print("Scraping web data...")
print()

# Scrape the pitcher pages and display the data in a useful format
print("Top pitchers for consideration:".upper())
pitchers = generate_pitchers(pitcher_urls)
display_players(pitchers)
print()

# Scrape the batter pages and display the data in a useful format
print("Top position players for consideration:".upper())
batters = generate_batters(batter_urls)
display_players(batters)
print()

print()
print("Complete!".upper())
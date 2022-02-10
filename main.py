import webbrowser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import html5lib


def generate_batters(urls):
    for url in urls:
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html5lib')
        table = soup.find(id="LeaderBoard1_dg1_ctl00")
        num_rows = 4
        for row_num in range(0, num_rows):
            raw_row = str(table.find(id=f"LeaderBoard1_dg1_ctl00__{row_num}"))
            raw_row_split = raw_row.split("</td>")
            col_num = 0
            for raw_column in raw_row_split:
                match col_num:
                    case 0 | 2 | 15:
                        0
                    case 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14:
                        column_data = raw_column.split(">", 1)[1]
                        #print(col_num, ": ", column_data)
                    case 1:
                        column_data = raw_column.split(">", 1)[1].split(">", 1)[1].split("<", 1)[0]
                        print(column_data)
                col_num += 1


def generate_pitchers(urls):
    for url in urls:
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html5lib')
        table = soup.find(id="LeaderBoard1_dg1_ctl00")
        num_rows = 9
        for row_num in range(0, num_rows):
            raw_row = str(table.find(id=f"LeaderBoard1_dg1_ctl00__{row_num}"))
            raw_row_split = raw_row.split("</td>")
            col_num = 0
            for raw_column in raw_row_split:
                match col_num:
                    case 0 | 2 | 10:
                        0
                    case 3 | 4 | 5 | 6 | 7 | 8 | 9:
                        column_data = raw_column.split(">", 1)[1]
                        #print(col_num, ": ", column_data)
                    case 1:
                        column_data = raw_column.split(">", 1)[1].split(">", 1)[1].split("<", 1)[0]
                        print(column_data)
                col_num += 1


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

# Interpolate the URLs to scrape the top players at each position

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

print("Top pitchers for consideration:".upper())
generate_pitchers(pitcher_urls)
print()

print("Top position players for consideration:".upper())
generate_batters(batter_urls)
print()

print()
print("Complete!".upper())
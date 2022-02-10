import webbrowser

# Input and validate the historical range

print("Generate a historical MLB all-star team for a select time period.")
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

urls = [
f'https://www.fangraphs.com/leaders.aspx?pos=c&stats=bat&lg=all&qual=y&type=8&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_4',
f'https://www.fangraphs.com/leaders.aspx?pos=1b&stats=bat&lg=all&qual=y&type=8&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_4',
f'https://www.fangraphs.com/leaders.aspx?pos=2b&stats=bat&lg=all&qual=y&type=8&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_4',
f'https://www.fangraphs.com/leaders.aspx?pos=3b&stats=bat&lg=all&qual=y&type=8&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_4',
f'https://www.fangraphs.com/leaders.aspx?pos=ss&stats=bat&lg=all&qual=y&type=8&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_4',
f'https://www.fangraphs.com/leaders.aspx?pos=lf&stats=bat&lg=all&qual=y&type=8&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_4',
f'https://www.fangraphs.com/leaders.aspx?pos=cf&stats=bat&lg=all&qual=y&type=8&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_4',
f'https://www.fangraphs.com/leaders.aspx?pos=rf&stats=bat&lg=all&qual=y&type=8&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_4',
f'https://www.fangraphs.com/leaders.aspx?pos=dh&stats=bat&lg=all&qual=y&type=8&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_2',
f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=y&type=8&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_9',
f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=rel&lg=all&qual=y&type=8&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31&page=1_7'
]

# Open each page in the browswer

for page in urls:
    webbrowser.open(page)
import webbrowser

print("Generate a historical MLB all-star team for a select time period.")
year1 = 0
year2 = 0
while year1 < 1900 or year1 > 2021:
    year1 = int(input("Enter the starting year of the time period: "))
while year2 < 1900 or year2 > 2021:
    year2 = int(input("Enter the ending year of the time period: "))
url = f'https://www.fangraphs.com/leaders.aspx?pos=np&stats=bat&lg=all&qual=y&type=8&season={year2}&month=0&season1={year1}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year1}-01-01&enddate={year2}-12-31_100'

webbrowser.open(url)

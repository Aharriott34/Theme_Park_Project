# Project to compare Disney, and Universal Resorts around the world.
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Web scrapping the attendance from the top 25 parks around the world.
disney_website = requests.get("https://www.wdwinfo.com/news-stories/worldwide-theme-park-attendance-grew-4-in-2019-disneys-numbers-dropped-slightly/")
disney_content = disney_website.content
soup = BeautifulSoup(disney_content, "html.parser")
parks_attendance = []
numbers = []
new_park_names = []

# Grabbing park attendance. Europa-Park was causing a problem with the "-", so it had to be split.
for child in soup.ol.children:
    park_names = "{0}".format(child.text)
    park_names = park_names.replace('Europa-Park', 'Europa Park')
    park_names_split = park_names.split("-")
    new_park_names.append(park_names_split[0])
    numbers = park_names_split[1].split(" ")[1]
    new_nums = float(numbers) * 1000000
    parks_attendance.append(new_nums)


park_dict = {}
for key in new_park_names:
    for value in parks_attendance:
        park_dict[key] = value
        parks_attendance.remove(value)
        break


# Combining associated parks from dataframe. Y-axis for bar graph.
df = pd.DataFrame.from_dict(park_dict, orient='index',columns=["Attendance"])
disney_world_parks = df.iloc[[0, 5, 6, 8]]
disneyland_parks = df.iloc[[1, 12]]
disneyland_paris = df.iloc[[13, 22]]
disneyland_tokyo = df.iloc[[2, 3]]
hong_kong_disney = df.iloc[[20]]
shanghai_disney = df.iloc[[9]]
universal_orlando = df.iloc[[10, 11]]
universal_hollywood = df.iloc[[14]]
universal_japan = df.iloc[[4]]

# Getting the total attendance from the associated parks. X-axis for bar graph.
dw_total = disney_world_parks['Attendance'].sum()
dl_total = disneyland_parks['Attendance'].sum()
dlp_total = disneyland_paris['Attendance'].sum()
dlt_total = disneyland_tokyo['Attendance'].sum()
hong_kong_total = hong_kong_disney['Attendance'].sum()
shanghai_total = shanghai_disney['Attendance'].sum()
uo_total = universal_orlando['Attendance'].sum()
uh_total = universal_hollywood['Attendance'].sum()
uj_total = universal_japan['Attendance'].sum()
print(df)

# Disney information.
disney_locations= np.arange(6)
x_disney_parks = ["Walt Disney World", "Tokyo Disneyland", "Disneyland", "Disneyland Paris", "Shanghai Disneyland", "Hong-Kong Disneyland"]
disney_totals = [dw_total , dlt_total, dl_total, dlp_total, shanghai_total, hong_kong_total]
plt.barh(x_disney_parks, disney_totals,label="Disney Resorts", color="mediumblue",zorder=3)

# Universal Information.
x_universal_parks = ["Universal Orlando Resort", "Universal Studios Japan","Universal Studios Hollywood"]
universal_totals = [uo_total, uj_total,uh_total]
plt.barh(x_universal_parks, universal_totals, label="Universal Resorts", color="green", zorder=3)

# Labeling the values.
for index, value in enumerate((*disney_totals, *universal_totals)):
    plt.text(value, index, int(value))

# Matplotlib information to create a graph.
plt.grid(zorder=0)
plt.xlim(0, 70000000)
plt.xticks([0,10000000,20000000,30000000,40000000,50000000,60000000,70000000], ["0", "10M", "20M", "30M", "40M","50M","60M","70M"])
plt.legend()
plt.gcf().subplots_adjust(left=0.20)
plt.xlabel('Attendance')
plt.title("Disney and Universal Resorts Around the World")
plt.savefig('Park_Chart.png', bbox_inches="tight")
plt.show()


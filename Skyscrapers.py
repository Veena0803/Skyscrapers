# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 23:10:34 2021
@author: iyerv
Name: Veena Iyer
CS602: Section SN1
Data: Skyscrapers
URL:
Description: This program demonstrates the skyscrapers of the world and visualizes these buildings in the form of
             various charts like map, bubble graph, bar graph etc based on continents and countries.
"""

# Importing libraries

import pandas as pd
import streamlit as st
import plotly.express as px
from plotly import graph_objects as go
from Functions import *

st.markdown(f'<div id="top"></div>', unsafe_allow_html=True)
# Initializing variables
decade = ['1940', '1950', '1960', '1970', '1980', '1990', '2000', '2010', '2020']
allColumns = ['NAME','CITY','Meters','FLOORS','COMPLETION','Latitude','Longitude']
columns = ['NAME','CITY','Meters','FLOORS','COMPLETION']

# Sets the title
st.title("CS 602 - Final Project: Skyscrapers")
# Sets the image
st.image("https://media.istockphoto.com/photos/aerial-panorama-of-new-york-city-skyline-at-sunset-picture-id1071263666?k=6&m=1071263666&s=612x612&w=0&h=ZNehQFY7r2RR4MXx-JkJiWD8-VCbh9k2vFv9Ng3XLCw=", width=700)
# Sets the index
st.sidebar.markdown(f'<span style="font-weight: bold;color:#EABC11">INDEX</span>', unsafe_allow_html=True)
st.sidebar.markdown(f'<a style="color: #FFFFFF;text-decoration: none;" href="#frame">Skyscraper table</a>', unsafe_allow_html=True)
st.sidebar.markdown(f'<a style="color: #FFFFFF;text-decoration: none;" href="#map">World Map</a>', unsafe_allow_html=True)
st.sidebar.markdown(f'<a style="color: #FFFFFF;text-decoration: none;" href="#bar">Bar Chart</a>', unsafe_allow_html=True)
st.sidebar.markdown(f'<a style="color: #FFFFFF;text-decoration: none;" href="#bubble">Bubble Chart</a>', unsafe_allow_html=True)
st.sidebar.markdown(f'<a style="color: #FFFFFF;text-decoration: none;" href="#top">Top of page</a>', unsafe_allow_html=True)
addMarkdownSeparator(st.sidebar) # Adds a separator - function call

# Creating a new dataframe after reading from the CSV file
sky_df = pd.DataFrame(pd.read_csv("Skyscrapers.csv"))
sky_df["Meters"] = (sky_df["Meters"].str.replace(" m", ""))
df = populateDataframe(sky_df, columns) # Function call

decade_chosen = createSlider(st, decade) # Function call
prev_dec = int(decade_chosen) - 10 # To get the previous 10 years data
st.markdown(f'<div id="frame"></div>', unsafe_allow_html=True)
header(st, "Skyscrapers constructed between " + str(prev_dec) + " and " + decade_chosen) # Function call with styling
updateDataFrame(st, df, decade_chosen)

mapData = {"lat":[], "lon":[]} # Initialize a dictionary for map
mapDf = getMapDataframeSubset(sky_df, decade_chosen) # Function call to check the decade chosen
for i in range(len(mapDf)):
    mapData['lat'].append(mapDf.iloc[i]['Latitude']) # Appends data to lat
    mapData['lon'].append(mapDf.iloc[i]['Longitude']) # Appends data to lon
map_data = pd.DataFrame(data = mapData) # Creates a dataframe from the fetched data

addMarkdownSeparator(st) # Function call to print a separator

st.markdown(f'<div id="map"></div>', unsafe_allow_html=True) # Setting div for click functionality
header(st) # Prints title
st.map(map_data, 1) # World map where 1 depicts the zoom value

year_df = sky_df['COMPLETION'] # Capture the year from the 'completion' column of the DF

addMarkdownSeparator(st.sidebar)

header(st.sidebar, "Skyscrapers by continent")
df_continent_breakup = getAllSkyscrapersUntilDecadeChosen(sky_df, decade_chosen) # Get cumulative skyscrapers count
continent_stats_dict = {}
for continent in df_continent_breakup["CONTINENT"]:
    if continent in continent_stats_dict.keys():
        continent_stats_dict[continent] = continent_stats_dict[continent] + 1
    else:
        continent_stats_dict[continent] = 1
# Print results in sidebar
for key in continent_stats_dict:
    content(str(key) + " : " + str(continent_stats_dict.get(key)), st.sidebar)

addMarkdownSeparator(st)

# Bar chart

st.markdown(f'<div id="bar"></div>', unsafe_allow_html=True)
header(st, "Progressive maximum height of skyscrapers (in meters)")
chart_dict = {"decade" : [], "avgHeight" : []}
for item in decade:
    df_chart = getAllSkyscrapersUntilDecadeChosen(sky_df, item)
    df_chart["Meters"] = df_chart["Meters"].astype(float)
    avg_height = df_chart["Meters"].mean()
    chart_dict["decade"].append(item)
    chart_dict["avgHeight"].append(avg_height)

line_chart = px.bar(chart_dict, x='decade', y='avgHeight',
             hover_data=['decade', 'avgHeight'], color='avgHeight',
             labels={'avgHeight':'Maximum height (in meters)','decade':'Decade'})

st.plotly_chart(line_chart)

addMarkdownSeparator(st)

# Bubble Chart
bubble_chart_dict = {}
bubble_chart_dict_df = {"country" : [], "count" : []}
for item in decade:
    df_chart = getDataframeSubset(sky_df, item)
    for i in df_chart["COUNTRY"]:
        if i in bubble_chart_dict.keys():
            bubble_chart_dict[i] = bubble_chart_dict[i] + 1
        else:
            bubble_chart_dict[i] = 1
# Create another dictionary with a list of countries and corresponding counts
for key in bubble_chart_dict.keys():
    bubble_chart_dict_df["country"].append(key)
    bubble_chart_dict_df["count"].append(bubble_chart_dict.get(key))
df_bb = pd.DataFrame.from_dict(bubble_chart_dict_df)
bubble_chart = px.scatter(df_bb, x="country", y="country", size="count", color="country",
                 hover_name="country", log_x=True, size_max=100)

st.markdown(f'<div id="bubble"></div>', unsafe_allow_html=True)
header(st, "Countries with maximum skyscrapers")
bubble_chart = go.Figure(data=[go.Scatter(
    x=df_bb["country"], y=df_bb["count"],
    mode='markers',
    marker=dict(
        color=["aqua", "beige", "darkolivegreen", "crimson", "darkmagenta", "darkorchid", "gold", "forestgreen", "ghostwhite", "lightcoral", "turquoise"],
        # Scaling smaller values to display better on bubble chart
        size=[count * 3 if count > 10 else count * 5 for count in df_bb["count"]],
    ),
)
])

st.plotly_chart(bubble_chart)

addMarkdownSeparator(st)

'''
References:

https://pythonspot.com/matplotlib-bar-chart/

https://docs.streamlit.io/en/stable/main_concepts.html

https://docs.streamlit.io/en/stable/api.html#display-charts

https://discuss.streamlit.io/t/make-it-more-explicit-for-end-users-what-steps-are-available-in-a-slider/5812

https://plotly.com/python/funnel-charts/

https://plotly.com/python/bubble-charts/

https://media.istockphoto.com/
'''




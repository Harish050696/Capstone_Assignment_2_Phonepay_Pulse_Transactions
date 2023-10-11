
#Importing the necessary libraries

import streamlit as st
import plotly.express as px
import mysql.connector
import pandas as pd  
import json
import locale  

#Data Retrival from the SQL database using the user and password.

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
  password="*****",
  database = "Capstone"
)

df = pd.read_sql_query("SELECT * FROM Capstone.Phonepetransactions",mydb)

#Conversion of the type of the column from str to float.

df = df.astype({'Transaction_Amount':'float'})

#Dashboard Creation

st.set_page_config(page_title="Phonepe_Transactions", page_icon=":bar_chart:",layout="wide")

#Sidebar
#Creating the filter based on the Year, Quarter and State

st.sidebar.header("Please Filter here")
Year = st.sidebar.multiselect("Select Year:",options=df["Year"].unique(),default = df["Year"].unique())
Quarter = st.sidebar.multiselect("Select Quarter:",options=df["Quarter"].unique(),default = df["Quarter"].unique())
State = st.sidebar.multiselect("Select State:",options=df["State"].unique(),default = df["State"].unique())
FS = df.query("Year == @Year & Quarter == @Quarter & State == @State")

#Header Section
#Providing the Total for the transaction Amount and Numbers in the Indian Numerical System using locale library

st.title(":bar_chart: Phonepe Pulse - Transactions")
st.markdown("##")
total_values = int(FS["Transaction_Amount"].sum())
total_count = int(FS["Transaction_Count"].sum())

locale.setlocale(locale.LC_ALL, 'en_IN')
formatted_total_values =  locale.currency(total_values, grouping=True)
formatted_total_numbers =  locale.currency(total_count, grouping=True)

left_column,right_column = st.columns(2)

with left_column:
  st.subheader("Total Transactions Values :")
  st.subheader(formatted_total_values.split(".")[0])

with right_column:
  st.subheader("Total Transactions Numbers :")
  st.subheader(formatted_total_numbers.split(".")[0][1:])
  
st.markdown("---")

#st.dataframe(FS)

# Graphs
# Pie Graph
# Providing the Transaction Values and Numbers based on the Quarter and Year using the Pie Graph with help of the Plotly Library

Amount_by_Quarter =  FS.groupby(by=['Quarter']).sum()[['Transaction_Amount']]
Count_by_Quarter =  FS.groupby(by=['Quarter']).sum()[['Transaction_Count']]
Amount_by_Year =  FS.groupby(by=['Year']).sum()[['Transaction_Amount']]
Count_by_Year =  FS.groupby(by=['Year']).sum()[['Transaction_Count']]


Pie_Quarter1 = px.pie(Amount_by_Quarter, values='Transaction_Amount', names=Amount_by_Quarter.index, title="<b> Transaction Values by Quarter </b>")
Pie1 = Pie_Quarter1.update_traces(textposition='inside', textinfo='percent+label')

Pie_Quarter2 = px.pie(Count_by_Quarter, values='Transaction_Count', names=Count_by_Quarter.index, title="<b> Transaction Numbers by Quarter </b>")
Pie2 = Pie_Quarter2.update_traces(textposition='inside', textinfo='percent+label')

Pie_Year1 = px.pie(Amount_by_Year, values='Transaction_Amount', names=Amount_by_Year.index, title="<b> Transaction Values by Year </b>")
Pie3 = Pie_Year1.update_traces(textposition='inside', textinfo='percent+label')

Pie_Year2 = px.pie(Count_by_Year, values='Transaction_Count', names=Count_by_Year.index, title="<b> Transaction Numbers by Year </b>")
Pie4 = Pie_Year2.update_traces(textposition='inside', textinfo='percent+label')

# Bar Graph
# Providing the Transaction Values and Numbers of the State based on the Quarter and Year using the Bar Graph with help of the Plotly Library

Amount_of_State1 =  FS.groupby(by=['State','Quarter']).sum()[['Transaction_Amount']].reset_index()
Amount_of_State2 =  FS.groupby(by=['State','Year']).sum()[['Transaction_Amount']].reset_index()
Amount_of_State_by_Quarter = Amount_of_State1.set_index(["State"])
Amount_of_State_by_Year = Amount_of_State2.set_index(["State"])

Bar_Quarter1 = px.bar(
 Amount_of_State_by_Quarter,
 x = Amount_of_State_by_Quarter.index,
 y = "Transaction_Amount",
 color = "Quarter",
 orientation = "v",
 title = "<b> Transaction Values of State by Quarter </b>"
)

Bar_Year1 = px.bar(
 Amount_of_State_by_Year,
 x = Amount_of_State_by_Year.index,
 y = "Transaction_Amount",
 color = "Year",
 orientation = "v",
 title = "<b> Transaction Values of State by Year </b>"
)

Count_of_State1 =  FS.groupby(by=['State','Quarter']).sum()[['Transaction_Count']].reset_index()
Count_of_State2 =  FS.groupby(by=['State','Year']).sum()[['Transaction_Count']].reset_index()
Count_of_State_by_Quarter = Count_of_State1.set_index(["State"])
Count_of_State_by_Year = Count_of_State2.set_index(["State"])

Bar_Quarter2 = px.bar(
 Count_of_State_by_Quarter,
 y = Count_of_State_by_Quarter.index,
 x = "Transaction_Count",
 color = "Quarter",
 orientation = "h",
 title = "<b> Transaction Numbers of State by Quarter </b>",
)

Bar_Year2 = px.bar(
 Count_of_State_by_Year,
 y = Count_of_State_by_Year.index,
 x = "Transaction_Count",
 color = "Year",
 orientation = "h",
 title = "<b> Transaction Numbers of State by Year </b>",
)

# Line Graph
# Providing the Transaction Values and Numbers of the District based on the Quarter and Year using the Line Graph with help of the Plotly Library

Amount_of_District1 =  FS.groupby(by=['District','Quarter']).sum()[['Transaction_Amount']].reset_index()
Amount_of_District2 =  FS.groupby(by=['District','Year']).sum()[['Transaction_Amount']].reset_index()

Line_Quarter1 = px.line(Amount_of_District1, x="District", y="Transaction_Amount", color="Quarter", title="<b> Transaction Values of District by Quarter </b>")
Line_Year1 = px.line(Amount_of_District2, x="District", y="Transaction_Amount", color="Year", title="<b> Transaction Values of District by Year </b>")

Count_of_District1 =  FS.groupby(by=['District','Quarter']).sum()[['Transaction_Count']].reset_index()
Count_of_District2 =  FS.groupby(by=['District','Year']).sum()[['Transaction_Count']].reset_index()

Line_Quarter2 = px.line(Count_of_District1, x="District", y="Transaction_Count", color="Quarter", title="<b> Transaction Numbers of District by Quarter </b>")
Line_Year2 = px.line(Count_of_District2, x="District", y="Transaction_Count", color="Year", title="<b> Transaction Numbers of District by Year </b>")

#Map Graph
# Providing the Transaction Values and Numbers of the State based on the Quarter and Year using the Map Graph with help of the Plotly Library
# The Map Graph is made with the help of the GeoJSON file

Mapfig1 = px.choropleth(
    Amount_of_State1,
    geojson= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='State',
    color='Transaction_Amount',
    title= "<b>Geographical Representation of Transaction Values of Indian States by Quarter </b>",
    animation_frame='Quarter',
    color_continuous_scale="Viridis"
)

Mapfig2 = px.choropleth(
    Amount_of_State2,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='State',
    color='Transaction_Amount',
    title= "<b>Geographical Representation of Transaction Values of Indian States by Year </b>",
    animation_frame='Year',
    color_continuous_scale="Plasma"
)

Mapfig3 = px.choropleth(
    Count_of_State1,
    geojson= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='State',
    color='Transaction_Count',
    title= "<b>Geographical Representation of Transaction Numbers of Indian States by Quarter </b>",
    animation_frame='Quarter',
    color_continuous_scale="Inferno"
)

Mapfig4 = px.choropleth(
  Count_of_State2,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='State',
    color='Transaction_Count',
    title= "<b>Geographical Representation of Transaction Numbers of Indian States by Year </b>",
    animation_frame='Year',
    color_continuous_scale="twilight"
)

# Providing the Transaction Values and Numbers of the District based on the Quarter and Year using the Map Graph with help of the Plotly Library
# The Map Graph is made with the help of the GeoJSON file

with open ("E:/Capstone/Project 2/india_district_map.geojson") as ind:
    india = json.load(ind)

Mapfig5 = px.choropleth(
              Amount_of_District1,
              locations="District",
              geojson=india,
              featureidkey="properties.district",
              color='Transaction_Amount',
              projection="mercator" ,
              color_continuous_scale="Reds",
              animation_frame="Quarter",
              title= "<b>Geographical Representation of Transaction Values of Indian Districts by Quarter </b>",
              )

Mapfig6 = px.choropleth(
              Amount_of_District2,
              locations="District",
              geojson=india,
              featureidkey="properties.district",
              color='Transaction_Amount',
              projection="mercator" ,
              color_continuous_scale="blues",
              animation_frame="Year",
              title= "<b>Geographical Representation of Transaction Values of Indian Districts by Year </b>",
              )

Mapfig7 = px.choropleth(
              Count_of_District1,
              locations="District",
              geojson=india,
              featureidkey="properties.district",
              color='Transaction_Count',
              projection="mercator" ,
              color_continuous_scale="greens",
              animation_frame="Quarter",
              title= "<b>Geographical Representation of Transaction Numbers of Indian Districts by Quarter </b>",
              )

Mapfig8 = px.choropleth(
              Count_of_District2,
              locations="District",
              geojson=india,
              featureidkey="properties.district",
              color='Transaction_Count',
              projection="mercator" ,
              color_continuous_scale="oranges",
              animation_frame="Year",
              title= "<b>Geographical Representation of Transaction Numbers of Indian Districts by Year </b>",
              )


map1 = Mapfig1.update_geos(fitbounds="locations", visible=False)
map2 = Mapfig2.update_geos(fitbounds="locations", visible=False)
map3 = Mapfig3.update_geos(fitbounds="locations", visible=False)
map4 = Mapfig4.update_geos(fitbounds="locations", visible=False)
map5 = Mapfig5.update_geos(fitbounds="locations", visible=False)
map6 = Mapfig6.update_geos(fitbounds="locations", visible=False)
map7 = Mapfig7.update_geos(fitbounds="locations", visible=False)
map8 = Mapfig8.update_geos(fitbounds="locations", visible=False)

#Displaying the Graphs in the Dashboards

left_column,right_column = st.columns(2)

left_column.plotly_chart(Pie1,use_container_width=True)
right_column.plotly_chart(Pie2,use_container_width=True)
left_column.plotly_chart(Pie3,use_container_width=True)
right_column.plotly_chart(Pie4,use_container_width=True)

left_column.plotly_chart(Bar_Quarter1,use_container_width=True)
right_column.plotly_chart(Bar_Quarter2,use_container_width=True)
left_column.plotly_chart(Bar_Year1,use_container_width=True)
right_column.plotly_chart(Bar_Year2,use_container_width=True)

left_column.plotly_chart(Line_Quarter1,use_container_width=True)
right_column.plotly_chart(Line_Quarter2,use_container_width=True)
left_column.plotly_chart(Line_Year1,use_container_width=True)
right_column.plotly_chart(Line_Year2,use_container_width=True)

left_column.plotly_chart(map1,use_container_width=True)
right_column.plotly_chart(map3,use_container_width=True)
left_column.plotly_chart(map2,use_container_width=True)
right_column.plotly_chart(map4,use_container_width=True)
left_column.plotly_chart(map5,use_container_width=True)
right_column.plotly_chart(map7,use_container_width=True)
left_column.plotly_chart(map6,use_container_width=True)
right_column.plotly_chart(map8,use_container_width=True)

#Hiding the Main Menu,Header and Footer in the Dashboard

hide_style = """<style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} </style>"""

st.markdown(hide_style,unsafe_allow_html=True)

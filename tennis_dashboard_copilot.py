import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns


df = pd.read_excel("df_merged.xlsx")

sidebar = st.sidebar
last_year = 2022

match_select = sidebar.selectbox("Select match", df["unique_match_num"].unique())
filtered_df = df[df["unique_match_num"] == match_select]

st.sidebar.header("Match details you selected...")
date_select = filtered_df[filtered_df["unique_match_num"] == match_select]["date"].iloc[0]
cup = filtered_df[filtered_df["unique_match_num"] == match_select]["tourney_name"].iloc[0]
court = filtered_df[filtered_df["unique_match_num"] == match_select]["surface"].iloc[0]
winner = filtered_df[filtered_df["winner"] ==1]["player_name"].iloc[0]
runner = filtered_df[filtered_df["winner"] ==0]["player_name"].iloc[0]

sidebar.write("Date of the match you selected:", date_select)
sidebar.write("Cup:", cup)
sidebar.write("Surface of the match:", court)
sidebar.write("Winner:", winner)
sidebar.write("Runner:", runner)

#------------------------------------------------------------
#Create a heading with blue font in streamlit to display match summary
def create_blue_heading(text):
  return st.markdown(f"<h1 style=\"color: blue;\">Match Summary</h1>", unsafe_allow_html=True)

create_blue_heading("Match Summary")

#Create a simple plotly chart to points_won by winner and runner based on points won
fig = px.bar(filtered_df, x="winner", y="points_won", color="winner", title="Points Won by Winner and Runner")
st.plotly_chart(fig)

#Create a plotly grouped bar plot with aces in blue color and double_faults in aqua color as per the unique_match_num selected
fig = go.Figure()
fig.add_traces([
    go.Bar(
      x=filtered_df["player_name"],
      y=filtered_df["aces"],
      name="Aces",
      marker_color="blue"
    ),
    go.Bar(
      x=filtered_df["player_name"],
      y=filtered_df["double_faults"],
      name="Double Faults",
      marker_color="aqua"
    )
])
st.plotly_chart(fig)

#Create two plots next to each other for 1st and 2nd winning serve percentage of two players as per the unique_match_num selected
fig = go.Figure()
fig.add_traces([
    go.Bar(
      x=filtered_df["player_name"],
      y=filtered_df["1stWon"],
      name="1st Winning Serve Percentage",
      marker_color="blue"
    )
])
fig.add_traces([
    go.Bar(
      x=filtered_df["player_name"],
      y=filtered_df["2ndWon"],
      name="2nd Winning Serve Percentage",
      marker_color="aqua"
    )
])
st.plotly_chart(fig)


#Create a sub-heading in blue color to display overall statistics of the matches
def create_blue_heading(text):
  return st.markdown(f"<h1 style=\"color: blue;\">Overall Statistics</h1>", unsafe_allow_html=True)

create_blue_heading("Overall Statistics")

#Create a plotly chart for overall number of wins for each player irrespective of the unique_match_num selected by end user
# Calculate the total number of wins for each player
total_wins = df.groupby("player_name")["winner"].sum()
#Create a new dataframe with only nationality with wins/losses columns
new_df = df.groupby("player_ioc").agg({"winner": "sum"})
new_df["losses"] = new_df["winner"].apply(lambda x: len(df[df["player_ioc"] == x]) - x)
new_df = new_df.reset_index()
#Rename the columns
#PLot a seaborn plot to see overall wins/losses per each nationality
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(data=new_df, x="player_ioc", y="winner", ax=ax)
sns.barplot(data=new_df, x="player_ioc", y="losses", ax=ax)
st.pyplot(fig)


#Create a stacked bar chart in plotly to compare the total number of games won on different surfaces by each player
# Create a new dataframe with only player_name and surface columns
new_df = df.groupby(["player_name", "surface"]).agg({"winner": "sum"})
new_df = new_df.reset_index()
# Create a stacked bar chart
fig = go.Figure()
fig.add_traces([
    go.Bar(
      x=new_df[new_df["player_name"] == "Roger Federer"]["surface"],
      y=new_df[new_df["player_name"] == "Roger Federer"]["winner"],
      name="Roger Federer"
    ),
    go.Bar(
      x=new_df[new_df["player_name"] == "Rafael Nadal"]["surface"],
      y=new_df[new_df["player_name"] == "Rafael Nadal"]["winner"],
      name="Rafael Nadal"
    ),
    go.Bar(
      x=new_df[new_df["player_name"] == "Novak Djokovic"]["surface"],
      y=new_df[new_df["player_name"] == "Novak Djokovic"]["winner"],
      name="Novak Djokovic"
    )
])
# Update the layout
fig.update_layout(
    title="Total Number of Games Won on Different Surfaces by Each Player",
    xaxis_title="Surface",
    yaxis_title="Total Number of Games Won"
)
# Display the bar chart
st.plotly_chart(fig)

#Create a plotly plot to compare players wins on various surfaces
# Create a new dataframe with only player_name and surface columns
new_df = df.groupby(["player_name", "surface"]).agg({"winner": "sum"})
new_df = new_df.reset_index()
# Create a plotly chart
fig = px.bar(new_df, x="player_name", y="winner", color="surface", title="Players Wins on Various Surfaces")
# Display the Plotly chart
st.plotly_chart(fig)



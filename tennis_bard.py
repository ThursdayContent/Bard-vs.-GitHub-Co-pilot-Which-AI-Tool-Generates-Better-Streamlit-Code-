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

#Create a heading with blue font to display match summary
def create_blue_heading(text):
  return st.markdown(f"<h1 style=\"color: blue;\">Match Summary</h1>", unsafe_allow_html=True)

# Create the heading with blue font to display match summary
create_blue_heading("Match Summary")

#Create a plotly grouped bar chart with aces and double_faults as per the unique_match_num selected

#Create a plotly chart for overall number of wins for each player irrespective of the unique_match_num selected by end user 

# Calculate the total number of wins for each player
total_wins = df.groupby("player_name")["winner"].sum()

# Create a bar chart
fig = go.Figure()
fig.add_traces([
    go.Bar(
      x=total_wins.index,
      y=total_wins.values,
      name="Total Wins"
    )
])

# Update the layout
fig.update_layout(
    title="Overall Number of Wins for Each Player",
    xaxis_title="Player Name",
    yaxis_title="Total Wins"
)

# Display the bar chart
st.plotly_chart(fig)

#Create a new dataframe with only player_country and wins/losses columns and plot a plotly chart on the new dataframe to show number of wins/losses per country

# Create a new dataframe with only nationality and wins/losses columns
new_df = df.groupby("player_ioc").agg({"winner": "sum"})
new_df["losses"] = new_df["winner"].apply(lambda x: len(df[df["player_ioc"] == x]) - x)
new_df = new_df.reset_index()

# Rename the columns
new_df = new_df.rename(columns={"player_ioc": "nationality"})

# Plot a Plotly chart to show number of wins/losses per country
fig = px.bar(new_df, x="nationality", y=["winner", "losses"], barmode="group", title="Number of Wins/Losses per Country")

# Display the Plotly chart
st.plotly_chart(fig)


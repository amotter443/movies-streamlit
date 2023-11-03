# To run locally: streamlit run web_movie_viz.py
# Change to dark mode by going to Settings and selecting "Dark" from Choose app theme, colors and fonts

#Load Requisite Libraries
import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st
import altair as alt
from pymongo import MongoClient

#Connect to MongoDB
conn = MongoClient("mongodb+srv://st.secrets.username:st.secrets.password@st.secrets.cluster.ycr5yln.mongodb.net/?retryWrites=true&w=majority")
#Connect to database in cluster
db = conn["letterboxd"]

#Connect to df, drop mongodb ID column
collection = db.get_collection("master_df")
df = pd.DataFrame(list(collection.find()))
df.drop('_id', axis=1, inplace=True)

#Connect to cast, drop mongodb ID column
collection = db.get_collection("cast")
cast = pd.DataFrame(list(collection.find()))
cast.drop('_id', axis=1, inplace=True)

#Connect to crew, drop mongodb ID column
collection = db.get_collection("crew")
crew = pd.DataFrame(list(collection.find()))
crew.drop('_id', axis=1, inplace=True)

#Connect to cast_trended, drop mongodb ID column
collection = db.get_collection("cast_trended")
cast_trended = pd.DataFrame(list(collection.find()))
cast_trended.drop('_id', axis=1, inplace=True)

#Connect to crew_trended, drop mongodb ID column
collection = db.get_collection("crew_trended")
crew_trended = pd.DataFrame(list(collection.find()))
crew_trended.drop('_id', axis=1, inplace=True)

#Create 'normal' view that doesn't included bulk logged entries, in this case from 2017 
normal = df[(df["Logged_Year"]>2017) & (df["Logged_Year"]<2023)]
normal['Enjoyed'] = np.where(normal['Rating']>=4,"Yes","No")

#To Do: Change name to your name
st.title("Alex Motter's Adventures in Moviegoing")
st.markdown("""---""")

######################################  Main View  ###############################################################

#Trended bar graph of release year versus count of films seen
st.subheader('Films Seen by Release Year')
fig_data = df.groupby(['Year']).agg({'Name':'size'})
fig_data.rename(columns = {'Name':'Films'},inplace=True)
fig_data.reset_index(inplace=True)
fig_data['Year'] = fig_data['Year'].astype(str)
chart = alt.Chart(fig_data).mark_bar().encode(
    x='Year',y='Films',color=alt.value("#F3C911"))
st.altair_chart(chart, use_container_width=True)


#Create table with row of stats
st.subheader('Usage Stats at a Glance')
lb_date = datetime.strptime(df.loc[0,'Logged_Date'],"%Y-%m-%d")
lb_date = (datetime.today()-lb_date).days
hours_watched = round((df['runtime'].sum())/60)
mean_rating = round(np.mean(df['Rating']),2)
st.write('Number of Films watched:', len(df))
st.write('Number of Days on Letterboxd:', lb_date)
st.write('Total Hours Watched:', hours_watched)
st.write('Average Star Rating:', mean_rating)
st.text("")
st.text("")


#Progress towards film goal
st.subheader('Progress towards film goal')
progress = [0,250,500,750,1000,1250,1500,1750,2000,2250,2500,2750,3000]
comparison_dict = {value: len(df) > value for value in progress}
fig_data = pd.DataFrame.from_dict(comparison_dict, orient='index')
fig_data.reset_index(inplace=True)
fig_data.columns=['Quantity','Met']
fig_data['Height'] = 1
chart = alt.Chart(fig_data).mark_bar(size=75).encode(
    x=alt.X('Quantity',scale=alt.Scale(domain=[0, 3000])),y=alt.Y('Height', axis=None), color=alt.Color(field="Met", scale=alt.Scale(range=['#b29100','#F3C911']),legend=None),).properties(height=125)
st.altair_chart(chart, use_container_width=True)


#Number of films seen by genre
st.subheader('Quantity of Films Seen by Genre')
genres=['Action', 'Crime', 'War', 'Drama', 'Thriller', 'Mystery', 'Comedy', 'Romance', 'Sci_Fi', 'Animation', 'Documentary', 'Adventure', 'Music', 'Horror', 'Fantasy', 'History', 'Western', 'Rom_Com']
fig_data = df[genres].aggregate("sum")
fig_data=fig_data.to_frame(name='Quantity')
st.table(fig_data)
st.text("")
st.text("")


#Is the film in English?
fig_data = normal.groupby(['english_language']).agg({'Name':'size'})
fig_data.reset_index(inplace=True)
fig_data['english_language'] = np.where(fig_data['english_language']==1,"Yes","No")
fig_data.rename(columns = {'english_language':'In English?','Name':'Quantity'},inplace=True)
chart =alt.Chart(fig_data).mark_arc(innerRadius=100, color="#F3C911").encode(
    theta=alt.Theta(field="Quantity", type="quantitative"),color=alt.Color(field="In English?", type="nominal", scale=alt.Scale(range=['#b29100','#F3C911']),legend=None),
).properties(title=alt.Title(text="Is the film in English?",offset=10),width=100,height=125)

#Enjoyed the film?
fig_data = normal.groupby(['Enjoyed']).agg({'Name':'size'})
fig_data.reset_index(inplace=True)
fig_data.rename(columns = {'Enjoyed':'Enjoyed?','Name':'Quantity'},inplace=True)
chart2 =alt.Chart(fig_data).mark_arc(innerRadius=100, color="#F3C911").encode(
    theta=alt.Theta(field="Quantity", type="quantitative"),color=alt.Color(field="Enjoyed?", type="nominal", scale=alt.Scale(range=['#b29100','#F3C911']),legend=None),
).properties(title=alt.Title(text="Enjoyed the film?",offset=10),width=100,height=125)

#Wrote a review?
fig_data = normal.groupby(['Review']).agg({'Name':'size'})
fig_data.reset_index(inplace=True)
fig_data['Review'] = np.where(fig_data['Review']==1,"Yes","No")
fig_data.rename(columns = {'Review':'Review?','Name':'Quantity'},inplace=True)
chart3 =alt.Chart(fig_data).mark_arc(innerRadius=100, color="#F3C911").encode(
    theta=alt.Theta(field="Quantity", type="quantitative"),color=alt.Color(field="Review?", type="nominal", scale=alt.Scale(range=['#b29100','#F3C911']),legend=None),
).properties(title=alt.Title(text="Wrote a Review?",offset=10),width=100,height=125)

st.altair_chart(chart | chart2 | chart3, use_container_width=True)

st.markdown("""---""")

######################################  Usage View  ###############################################################

st.subheader('Letterboxd Usage')

#High-level stats
fig_data = normal.groupby(['Logged_Year','Logged_Week']).agg({'Name':'size'})
weekly_watch = round(np.mean(fig_data['Name']),1)
fig_data = normal.groupby(['Logged_Year','Logged_Month']).agg({'Name':'size'})
monthly_watch = round(np.mean(fig_data['Name']),1)
st.write('Average per Month:', monthly_watch)
st.write('Average per Week:', weekly_watch)
st.text("")
st.text("")

#Trended line graph of each film logged minus outliers like backfilling/partial years
st.subheader('Quantity of New Films Logged per Year')
fig_data = normal.groupby(['Logged_Year']).agg({'Name':'size'})
fig_data.reset_index(inplace=True)
fig_data.rename(columns = {'Name':'Films','Logged_Year':'Year'},inplace=True)
fig_data['Year'] = fig_data['Year'].astype(str)
chart = alt.Chart(fig_data).mark_line().encode(
    x='Year',y='Films',color=alt.value("#F3C911"))
st.altair_chart(chart, use_container_width=True)

#Average star rating by decade
st.subheader('Average Rating per Decade')
# Function to calculate the decade
def calculate_decade(year):
    return (year // 10) * 10

# Create the "Decade" column
df['Decade'] = df['Year'].apply(calculate_decade)
fig_data = df[df['Rating']>0]
fig_data = fig_data.groupby(['Decade']).agg({'Rating':'mean'})
fig_data['Rating'] = round(fig_data['Rating'],2)
st.table(fig_data)
st.text("")
st.text("")


#Breakdown of movies watched per month
fig_data = normal.groupby(['Logged_Month']).agg({'Name':'size'})
fig_data.reset_index(inplace=True)
fig_data.rename(columns = {'Name':'Quantity','Logged_Month':'Month'},inplace=True)
chart = alt.Chart(fig_data).mark_bar(size=20).encode(
    x=alt.X('Month',scale=alt.Scale(domain=[1,12])),y='Quantity',color=alt.value("#F3C911")).properties(title=alt.Title(text="Movies Logged by Month",offset=10),width=300,height=250)

#Breakdown of movies watched per day of week
fig_data = normal.groupby(['Logged_DOW']).agg({'Name':'size'})
fig_data.reset_index(inplace=True)
fig_data.rename(columns = {'Name':'Quantity','Logged_DOW':'Day of Week'},inplace=True)
chart2 = alt.Chart(fig_data).mark_bar(size=20).encode(
    x=alt.X('Day of Week',scale=alt.Scale(domain=[1,7])),y='Quantity',color=alt.value("#F3C911")).properties(title=alt.Title(text="Movies Logged by Day of Week",offset=10),width=250,height=250)

#Visualize both graphs
st.altair_chart(chart | chart2,use_container_width=True)

st.markdown("""---""")

######################################  Cast/Crew View  ###############################################################

st.subheader('Most Watched Cast & Crew')
st.text("")
st.text("")

#Generate top actor
actor = cast.loc[cast['order']==0,'profile_path'].values[0]
#Generate top crew stats
fig_data = crew.groupby(['job']).agg({'order':'min'})
fig_data = fig_data.merge(crew, on=['job','order'],  how='left')
director = fig_data.loc[fig_data['job']=='Director','profile_path'].values[0]
costume = fig_data.loc[fig_data['job']=='Costume Design','profile_path'].values[0]
screenplay = fig_data.loc[fig_data['job']=='Screenplay','profile_path'].values[0]
editor = fig_data.loc[fig_data['job']=='Editor','profile_path'].values[0]
dp = fig_data.loc[fig_data['job']=='Director of Photography','profile_path'].values[0]

st.image([actor,director,costume],width=200, caption=['Actor','Director','Costume Designer']) 
st.image([screenplay,editor,dp],width=200, caption=['Screenplay','Editor','Director of Photography']) 
st.text("")
st.text("")


#Stats on Female Representation
st.subheader('Female Representation in Film Watching')
female_roles = round(np.mean(df['female_roles']),2)
st.write('Average Credited Female Roles:', female_roles)
fig_data = df.groupby(['female_directed']).agg({'Rating':'mean'})
fig_data.reset_index(inplace=True)
st.write('Average Star Rating (Female Directed)', round(fig_data.loc[1,'Rating'],2))
st.write('Average Star Rating (Non-Female Directed)', round(fig_data.loc[0,'Rating'],2))
st.text("")
st.text("")


#What percentage of films were female driven
fig_data = df.groupby(['female_driven']).agg({'Name':'size'})
fig_data.reset_index(inplace=True)
fig_data['female_driven'] = np.where(fig_data['female_driven']==1,"Yes","No")
fig_data.rename(columns = {'female_driven':'Female Driven?','Name':'Quantity'},inplace=True)
chart =alt.Chart(fig_data).mark_arc(innerRadius=100, color="#F3C911").encode(
    theta=alt.Theta(field="Quantity", type="quantitative"),color=alt.Color(field="Female Driven?", type="nominal", scale=alt.Scale(range=['#b29100','#F3C911']),legend=None),
).properties(title=alt.Title(text="Female Driven?",offset=10))

st.altair_chart(chart,use_container_width=True)


#Trend most seen actors by year
st.subheader('Top Actors by Year')
fig_data = cast_trended.groupby(['Logged_Year','gender']).agg({'order':'min', 'display':'max'})
fig_data.reset_index(inplace=True)
fig_data = fig_data.merge(cast_trended, on=['Logged_Year','gender','order','display'],  how='left')
fig_data = fig_data[['Logged_Year','name']]
fig_data.columns = ['Year','Name']
fig_data = fig_data.sort_values('Year',ascending=False)
st.table(fig_data)


#Trend most seen directors by year
st.subheader('Top Directors by Year')
fig_data = crew_trended.groupby(['Logged_Year','job']).agg({'order':'min', 'display':'max'})
fig_data.reset_index(inplace=True)
fig_data = fig_data[fig_data['job']=='Director']
fig_data = fig_data.merge(crew_trended, on=['Logged_Year','job','order','display'],  how='left')
fig_data = fig_data[['Logged_Year','name']]
fig_data.columns = ['Year','Name']
fig_data = fig_data.sort_values('Year',ascending=False)
st.table(fig_data)

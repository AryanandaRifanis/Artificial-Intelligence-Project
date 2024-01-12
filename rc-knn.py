# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 23:53:16 2024

@author: ARYA
"""

#importing all the neccesary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile
import warnings
warnings.filterwarnings('ignore')

#Reading The dataset

#consisit of 25M ratings
rating_df = pd.read_csv('C:/Folder Arya/Study/BAU Doc/Fall SMT/Recommender Systems/RS PROJEK/ratings.csv')
#consist of tags/comments from user
tags_df = pd.read_csv('C:/Folder Arya/Study/BAU Doc/Fall SMT/Recommender Systems/RS PROJEK/tags.csv')
#consist of movie titles
title_df = pd.read_csv('C:/Folder Arya/Study/BAU Doc/Fall SMT/Recommender Systems/RS PROJEK/movies.csv')

#looking for some initial statistics of data
print('No of Users who rated movies:', rating_df.userId.nunique())
print('No of Movies:', rating_df.movieId.nunique())
print('No of ratings:', rating_df.rating.count())
print('No of user comments:', tags_df.tag.nunique())
print('No of Movies commented by user:', tags_df.movieId.nunique())
print('Percentage of user commented:', (tags_df.tag.nunique()/rating_df.userId.nunique())*100, '%')
print('No of movies commented by user:', (tags_df.movieId.nunique()/rating_df.movieId.nunique())*100, '%')

#Data Manipulation
df1 = rating_df.copy()
df2 = tags_df.copy()
df3 = title_df.copy()
del df1['timestamp']
del df2['timestamp']

#seperate year from title
#seperate genre in each colum
#add year from title feature
ss = df3['title'].str.findall('\((\d{4})\)').str.get(0)
df3['Year'] = ss
#seperate genre for each movie and count genres
sss = df3['genres'].str.split(pat='|', expand=True).fillna(0)
sss.columns = ['genre1', 'genre2', 'genre3', 'genre4', 'genre5', 'genre6', 'genre7', 'genre8', 'genre9', 'genre10']
cols = sss.columns
sss[cols] = sss[cols].astype('category')
ss1 = sss.copy()
cat_columns = ss1.select_dtypes(['category']).columns
#count genres (non zeros)
ss1[cat_columns] = ss1[cat_columns].apply(lambda x: x.cat.codes)
ss1['genre_count'] = ss1[cols].gt(0).sum(axis=1) #count greater than 0 values for less than: df[cols].lt(0).sum(axis=1), for equal==0: df[cols].eq(0).sum(axis=1)
#assigning everything to same dataframe
df3['genre_count'] = ss1['genre_count']
df3[cols] = sss[cols]
#Show dataframe
df3.head(10)

#avg movie ratings by movied id and count
rating_avg = df1.groupby('movieId')['rating'].mean().reset_index()
rating_avg = pd.DataFrame(rating_avg)
rating_count = df1.groupby('movieId')['rating'].count().reset_index()
rating_count = pd.DataFrame(rating_count)
rating_count.rename({'rating': 'rating_count'}, axis=1, inplace=True)

#avg movie ratings by user id and count
user_rating = df1.groupby('userId')['rating'].mean().reset_index()
user_rating = pd.DataFrame(user_rating)
user_count = df1.groupby('userId')['rating'].count().reset_index()
user_count = pd.DataFrame(user_count)
user_count.rename({'rating': 'rating_count'}, axis=1, inplace=True)

#dataframe movie 
df_movie = rating_avg.merge(rating_count, on = 'movieId', how='inner')
#dataframe users
df_user = user_rating.merge(user_count, on = 'userId', how='inner')

#avg rating given by a user and its count
df_user.head(10)

#avg rating on a movie and count
df_movie.head(10)

#add genre to tags_df --> for word cloud
cols = ['movieId','genre1']
dfk = df3[cols]
df2 = df2.merge(dfk, on = 'movieId', how='inner')
df2.head(10)

#user movie tags (just for checking spaming)
user_tags = df2.groupby(['userId', 'movieId'])['tag'].count().reset_index()
user_tags = pd.DataFrame(user_tags)
user_tags[user_tags['tag']==user_tags.tag.max()]

#user tag count  --> add
user_tagcount = df2.groupby('userId')['tag'].count().reset_index()
user_tagcount = pd.DataFrame(user_tagcount)
user_tagcount.rename({'tag': 'tag_count'}, axis=1, inplace=True)
user_tagcount.head(10)

#movie tag count --> movie year & genres
movie_tagcount = df2.groupby('movieId')['tag'].count().reset_index()
movie_tagcount = pd.DataFrame(movie_tagcount)
movie_tagcount.rename({'tag': 'tag_count'}, axis=1, inplace=True)
movie_tagcount.head(10)

cols = ['movieId','genre_count', 'genre1']
dfs = df3[cols]
movie_tagcount = movie_tagcount.merge(dfs, on = 'movieId', how='inner')
movie_tagcount.head(10)

df3 = df3.merge(df_movie, on = 'movieId', how='inner')
df3.rename({'rating': 'avg_rating'}, axis=1, inplace=True)
df3.head(10)

#descriptive statistics
#df3 title, year, genres, genre_count --> avg rating and count can be added
#df_user: avg_rating and count by user
#df_movie: avg_rating and count on movie
#df2: userid, movieid, tags, genre
#user_tags: tags by user on each movie
#user_tagcount: user activity
#movie_tagcount: tags & genre count by movie and genre 1

#Summary statistics to have some more insights
df3.describe()
#Summary statistics for df3
df3.describe(include=[object, 'category'])
#describe dataframe for user 
df_user.describe()
#Summary statistics for df2
df2.describe(include=[object, 'category'])
#summary statistics for usertags
user_tags.describe()
#summary statistics for usertagcount
user_tagcount.describe(include='all')
#summary statistics for movietagcount
movie_tagcount.describe(include='all')

#--> Visualization
df3.head(10)

#Using graphs
sns.set(rc={'figure.figsize':(14, 6)})
sns.set_context("talk")
sns.set_style("darkgrid", {"axes.facecolor": ".9"}) #sns.axes_style("whitegrid")
sns.distplot(df3.Year)

#zooming in:
sns.distplot(df3.Year)
plt.xlim(1940, 2020)

#Describe the genres per count
genre = df3.genre1.value_counts()
genre = pd.DataFrame(genre)
genre = genre.reset_index()
genre.rename({'index': 'genre', 'genre1':'Count'}, axis=1, inplace=True)
sns.barplot(x = genre.genre, y=genre.Count)
plt.xticks(rotation=90)
plt.show()

#Describe the average of genres per count
genre1 = df3.groupby('genre1')['rating_count'].mean()
genre1 = pd.DataFrame(genre1)
genre1 = genre1.reset_index()
genre1.rename({'rating_count':'avg_count_per_genre'}, axis=1, inplace=True)
sns.set(rc={'figure.figsize':(14, 8)})
sns.set_context("talk")
sns.set_style("darkgrid", {"axes.facecolor": ".9"})
sns.barplot(x = genre1.avg_count_per_genre, y=genre1.genre1)
plt.ylabel("")

#show the rating for each genre of films
cols = ['movieId', 'genre1']
b1 = df3[cols]
box_genre = df1.merge(b1, on='movieId', how='inner')
sns.set(rc={'figure.figsize':(16, 6)})
sns.set_context("talk")
sns.set_style("darkgrid", {"axes.facecolor": ".9"})
sns.boxenplot(x=box_genre.genre1, y=box_genre.rating, data=box_genre)
plt.xticks(rotation=90)
plt.ylim(-2, 7)

#movie produced each year for each genre (stacked bar)
genre_by_year = df3.groupby(['Year', 'genre1'])['title'].count().reset_index()
genre_by_year  = pd.DataFrame(genre_by_year)
genre_by_year.tail()

#shaping by genre per year
genre_by_year.shape

#since we already seen that move of the movies were after 1940s - 1950's, so we filter out every thing before it
genre_by_year1 = genre_by_year[genre_by_year['Year']>='1945']
genre_by_year1.shape

#Stackable rating averages per pivots
sns.set(rc={'figure.figsize':(24, 8)})
sns.set_context("talk")
sns.set_style("darkgrid", {"axes.facecolor": ".9"})
df_pivot = pd.pivot_table(genre_by_year1, index='Year', columns='genre1', values='title')
df_pivot.plot.bar(stacked=True, colormap='plasma')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

#genre popularity each year
genre_pop = df3.groupby(['genre1', 'Year' ])['avg_rating'].mean().reset_index()
genre_pop  = pd.DataFrame(genre_pop)
genre_pop.tail()

#top 10 movies with rating count via swarmplot
top10_mov = df3.sort_values(by=['rating_count'], ascending=False)
top10_mov = top10_mov.head(10)
cols = ['movieId', 'title']
top10mov = top10_mov[cols]
top10mov.head(10)

#shaping with top 10 movies
top10mov = top10mov.merge(df1, on = 'movieId', how='inner')
top10mov.shape

top10mov.head(10)

kkk = top10mov[top10mov['movieId']==356]
sns.displot(kkk.rating)

sns.kdeplot(data=top10mov, x='rating', hue='title', fill=True, common_norm=False, palette="plasma", alpha=.5, linewidth=0,)
plt.tight_layout()

#verify if top rates are also top commentors
top100tag_usr = user_tagcount.sort_values(by=['tag_count'], ascending=False).reset_index()
del top100tag_usr['index']
top100tag_usr.head(10)

avg_rating_perc = ((3.405-3.056)/3.056) *100
avg_rating_count = ((3429.190-75.776)/3429.190) *100
tag_avg_count = ((138.80 - 6.284)/138.80) *100
print('Movies with greater than average tags count have ', avg_rating_perc, '% better avg rating')
print('Movies with greater than average tags count have ', avg_rating_count, '% better rating count')
print('Movies with greater than average tags count have ', tag_avg_count, '% better tag count')

#genre popularity each year
genre_pop = df3.groupby(['genre1', 'Year' ])['avg_rating'].mean().reset_index()
genre_pop  = pd.DataFrame(genre_pop)
genre_pop.tail()

genre_pop1 = genre_pop.copy()

dfgen2 = genre_pop1[genre_pop1['genre1']=='Comedy']
dfgen3 = genre_pop1[genre_pop1['genre1']=='Documentary']
dfgen4 = genre_pop1[genre_pop1['genre1']=='Horror']
dfgen = genre_pop1[genre_pop1['genre1']=='Action']
dfgen1 = genre_pop1[genre_pop1['genre1']=='Drama']

#hence proved that movies with more than average tag count are more popular and so do popular movies have more rating counts and tags counts aswell.

genre1 = df3.groupby('genre1')['rating_count'].mean()
genre1 = pd.DataFrame(genre1)
genre1 = genre1.reset_index()
genre1.rename({'rating_count':'avg_count_per_genre'}, axis=1, inplace=True)
genre1.head()

cols = ['movieId', 'genre1', 'Year']
b1 = df3[cols]
box_genre = b1.merge(df_movie, on='movieId', how='inner')
box_genre.head(10)

cols = ['Year', 'genre1', 'rating']
box_genre1 = box_genre[cols]
box_genre1.head()

d1 = box_genre1[box_genre1['Year']>'2009']

para = d1.pivot_table(index='genre1', columns='Year', values='rating', fill_value=0)

para.head(10)

para1 = para.reset_index()
#del para1['Year']
para1.head()

para1['genre2'] = para1.genre1.cat.codes

para1.head(10)


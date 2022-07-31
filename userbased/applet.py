import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests

l = []
# l_dict = {}


def movies_csv2dict(string):
    # f = open(string, "r+")
    l_dict = {}
    # f.readline()
    movies = pd.read_csv(string)
    # for l in f.readlines():
    for i in range(movies.shape[0]):
        l_dict[movies.iloc[i,1]] = movies.iloc[i,0]
    return l_dict


# recmovi = set({})
mapped_movies = movies_csv2dict("userbased\movies.csv")  # name : id
# st.write(mapped_movies)
# with pickle
# with open("users.csv", "r+") as f:
#     file = f.readlines()
#     recmovi = set(file)
#     pass


def csv2dict(string):
    f = open(string, "r+")
    l_dict = {}
    f.readline()
    df = pd.read_csv(string)
    
    rows = df.shape[0]
    # print(mapped_movies)
    for i in range(rows):
        user_id, movie_id, rating = df.iloc[i,0], df.iloc[i,1],df.iloc[i,1]
    # for l in f.readlines():
    #     user_id, movie_id, rating, _ = l.split(",")
    #     # movie_id = mapped_movies[movie]
        if int(user_id) not in l_dict:
            l_dict[int(user_id)] = {}
            l_dict[int(user_id)][int(movie_id)] = float(rating)
        else:
            l_dict[int(user_id)][int(movie_id)] = float(rating)
    return l_dict

def dict2csv(string,dict):
    u,m,r=[], [], []
    for user_id in dict:
        for movie_id in dict[user_id]:
            u.append(user_id); m.append(movie_id); r.append(dict[user_id][movie_id])
    dict= {
        'user_id':u, 'movie_id':m, 'ratings':r
    }
    df = pd.DataFrame(dict)
    df.to_csv(string, index=False, header=False)
try:

    # recmovi = pickle.load(open('pick.pkl', 'rb'))
    watched_movies = pickle.load(open('userbased\watched1.pkl', 'rb'))
    dict2csv("ratings_modified.csv",watched_movies)
    # watched_movies = csv2dict('userbased/ratings.csv')
except Exception as e:
    st.write("No pickle file found",e)
    # watched_movies = {672 : {'Jumanji (1995)': 4}}
    # watched_movies = csv2dict('/home/dhruvil/MR_Project/userbased/ratings.csv')

    print("hello")

try:
    movies = pd.read_csv('userbased\movies.csv')
except Exception as e:
    print("hello sorry i found an exrror", e)
st.title("Provide your watched movies")
user_id = st.text_input("Enter user id")
option = st.selectbox('Enter Movie Name', (movies['title']))
rating = st.slider('Enter Rating', 1, 5)
emoji = "⭐"
st.markdown("<p style='text-align: center;'>" + emoji*rating + "</p>", unsafe_allow_html=True)
result = st.button("Add to watched")
if result:
    # print(type(watched_movies))
    user_id = int(user_id)
    if user_id not in watched_movies:
        watched_movies[int(user_id)] = {option: rating}
        st.write("You have rated {} {} stars".format(option, rating))
    # print("watched movies is here", watched_movies)
    else:
        if int(mapped_movies[option]) in watched_movies[user_id]:
            st.write("Rating is updated. You have earlier rated {} {} stars".format(
                option, watched_movies[user_id][int(mapped_movies[option])]))
        else:

            st.write("Movie added")
        watched_movies[user_id][int(mapped_movies[option])] = rating
        # pickle.dump(recmovi, open('pick.pkl', 'wb'))
    pickle.dump(watched_movies, open('userbased\watched1.pkl', 'wb'))

# {user_id : {movie_id : rating}}

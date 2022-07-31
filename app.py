import streamlit as st
import pandas as pd
import pickle
import requests

# css
#not found
# ['The Company', 'Star Wars: Clone Wars: Volume 1', 'Restless', 'Wuthering Heights', 'Emma', 'The Secret', 'Creature']
st.set_page_config(layout="wide")
styl = f"""
    <style>
        img{{
            height : 240px;
            margin : 8px;   
            border-radius: 5%;
        }}
        
    </style>
    """
st.markdown(styl, unsafe_allow_html=True)


l = []
l_dict = {}
watched_movies = []
sim_score = {}
recmovi = set({})
# with pickle
# with open("users.csv", "r+") as f:
#     file = f.readlines()
#     recmovi = set(file)
#     pass
try:

    recmovi = pickle.load(open('pick.pkl', 'rb'))
    watched_movies = pickle.load(open('watched.pkl', 'rb'))
except Exception:
    print("hello")


def fetch_posterpath(recomended_movies_set):
    for i in recomended_movies_set:
        dict = pickle.load(open('posterpaths.pkl', 'rb'))
        if i not in dict:
            st.write("Movie name is here", i)

            index = movies[movies['title'] == i].index[0]
            movie_id = movies.loc[index, 'movie_id']
            # st.write(movie_id)

            response = requests.get(
                f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=5f22100b0a8f34d1ea15eb5605bc2d87&language=en-US")
            response = response.json()

            data = response["poster_path"]
            poster = f"https://image.tmdb.org/t/p/w500/{data}"
            name = movies.loc[index, 'title']

            dict[name] = poster
            pickle.dump(dict, open('posterpaths.pkl', 'wb'))
    return dict

def fetch_posterpath_from_pkl(recomended_movies_set):
    dict = {}
    poster_dict_from_pkl = pickle.load(open('posterpaths.pkl', 'rb'))
    for i in recomended_movies_set:
        poster = poster_dict_from_pkl[i]
        dict[i] = poster
    return dict
    

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),
                        reverse=True, key=lambda x: x[1])
    movie_list = movie_list[1:7 + 1]
    # st.write(movie_list)
    # st.write(movie_list)
    list1 = []
    for i in movie_list:
        movie_id = movies.loc[i[0], 'movie_id']

        # response = requests.get(
        #     f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=5f22100b0a8f34d1ea15eb5605bc2d87&language=en-US")
        # response = response.json()

        # data = response["poster_path"]
        # poster = f"https://image.tmdb.org/t/p/w500/{data}"
        name = movies.loc[i[0], 'title']
        list1.append(name)
        # print(name)
        # print(type(name))
        # l.append(poster)
        # poster = 
        # l_dict[name] = [poster[name],i[1]]
        # l.append([poster[name], name])
    l_dict = fetch_posterpath_from_pkl(list1)
    l = dict2dlist(l_dict)
    return l, l_dict


# movi.append()
movies = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies)
similarity = pickle.load(open('similarity.pkl', 'rb'))
similarity = pd.DataFrame(similarity)

# # TO BE removed 
# try:
#     poster_path_dict = fetch_posterpath(movies['title'])
# except Exception as e:
#     st.write("No movies found")
# finally:
#     pickle.dump(poster_path_dict, open('posterpaths.pkl', 'wb'))

st.title('Movie Recommendation System')
option = st.selectbox('Enter Movie Name', (movies['title']))
result = st.button("Recommend")
var = 0
f = open('recommended.csv', 'w+')


def dict2dlist(dict):
    l = []
    for x, y in dict.items():
        temp = [y, x]
        l.append(temp)
    return l


def display_from_dict(dict, message):
    l = dict2dlist(dict)
    img = []
    caption = []
    for i in range(len(l)):

        img.append(l[i][0])
        caption.append(l[i][1])
    # st.columns here since it is out of beta at the time I'm writing this
    # cols = cycle(st.columns(4))
    # for idx, filteredImage in enumerate(img):
    #     next(cols).image(filteredImage, width=150,
    #                      caption=caption[idx], use_column_width=False)
    st.write(message)
    st.image(img, width=155, caption=caption, use_column_width= False)


if result:
    output, output_dict = recommend(option)
    watched_movies.append(option)
    img, caption = [], []
    st.write("Based on your provided movie, we recommend the following movies")
    for i in range(8):
        recmovi.add(output[i][1])
        img.append(output[i][0])
        caption.append(output[i][1])
    st.image(img, width=155, caption=caption, use_column_width= False)



    
        
    
# api key - 5f22100b0a8f34d1ea15eb5605bc2d87
# api - application programme interface (data pipeline)(software intersection)
# eg - irctc,mmt
# database calling - return data(json format string)
# dict ={
#     "devasy": {mo}
# }
    
# st.write(fetch_posterpath(watched_movies))
final_rec = recmovi.difference(set(watched_movies))
message = "Based on your previous watchlist, we recommend you the following movies"
display_from_dict(fetch_posterpath_from_pkl(final_rec), message)
# display_from_dict(fetch_posterpath(final_rec), message)
message = "Do you want to watch it again ??"
# display_from_dict(fetch_posterpath(watched_movies), message)
display_from_dict(fetch_posterpath_from_pkl(watched_movies), message)
# st.write(final_rec)
f.write(str(final_rec))
pickle.dump(final_rec, open('pick.pkl', 'wb'))
pickle.dump(watched_movies, open('watched.pkl', 'wb'))
f.close()


# without pickle
# st.title('Movie recommendation System')
# movies = pd.DataFrame(pd.read_csv('movies.csv'))
# option = st.selectbox('Enter Movie Name', (movies['title']))
# result = st.button("Recommend")
# similarity = pd.DataFrame(pd.read_csv('simdf.csv'))
#
# if result:
#     st.write(option)

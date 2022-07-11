import http.client
import json
import time
import sys
import collections

conn = http.client.HTTPSConnection("api.themoviedb.org")
#API_key = "6b3c013514029dfa94497c46ff814cd0"
API_key = sys.argv[1]

######### Q1.b #########
# Search for movies in the "Drama" category released in 2004 or later and retrieve the 350 most popular
movie_ID_name = {}

for i in range(1, 19):
    request_string = "/3/discover/movie?with_genres=18&primary_release_date.gte=2004-01-01&page=" + str(
        i) + "&include_video=false&include_adult=false&sort_by=popularity.desc&language=en-US&api_key="+API_key
    #print(request_string)

    payload = "{}"
    conn.request("GET", request_string, payload)
    res = conn.getresponse()
    data = res.read()
    dat = json.loads(data)
    res_i = dat['results']

    for result in res_i:
        if "," in result['title']:
             movie_ID_name[result['id']] = '"'+result['title']+'"'
        else:
            movie_ID_name[result['id']] = result['title']

# Remove the last 10 movies, so the list is only 350 movies long
for j in range(10,20):
    del movie_ID_name[res_i[j]['id']]

with open('movie_ID_name.csv', 'w') as f:
    for key in movie_ID_name.keys():
        f.write("%s,%s\n" % (key, movie_ID_name[key]))

######### Q1.c #########
# 1. For each movie retrieved in part b, find it's 5 similar movies.
request_count = 0
movie_ID_sim_movie_ID = []

for movie_ID in movie_ID_name.keys():
    if request_count in [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]:
        print('at request '+str(request_count)+' ,sleeping for 10 seconds')
        time.sleep(10)

        payload = "{}"
        conn = http.client.HTTPSConnection("api.themoviedb.org")
        request_string = "/3/movie/" + str(movie_ID) + "/similar?page=" + str(1) + "&language=en-US&api_key=" + API_key
        conn.request("GET", request_string, payload)
        res2 = conn.getresponse()
        data2 = res2.read()
        dat2 = json.loads(data2)
        try:
            res_j = dat2['results']
        except:
            print('Error')
        else:
            for index, item in enumerate(res_j):
                if index >= 5:
                    break
                else:
                    movie_ID_sim_movie_ID.append((movie_ID,item['id']))
        finally:
            request_count += 1

    else:
        print("Request count: "+str(request_count))
        payload = "{}"
        conn = http.client.HTTPSConnection("api.themoviedb.org")
        request_string = "/3/movie/" + str(movie_ID) + "/similar?page=" + str(1) + "&language=en-US&api_key=" + API_key
        conn.request("GET", request_string, payload)
        res2 = conn.getresponse()
        data2 = res2.read()
        dat2 = json.loads(data2)
        try:
            res_j = dat2['results']
        except:
            print('Error_2')
        else:
            for index, item in enumerate(res_j):
                if index >= 5:
                    break
                else:
                    movie_ID_sim_movie_ID.append((movie_ID,item['id']))
        finally:
            request_count += 1

# Remove all duplicates
for (a,b) in movie_ID_sim_movie_ID:
    if (b,a) in movie_ID_sim_movie_ID:
        movie_ID_sim_movie_ID.remove((b,a))


with open('movie_ID_sim_movie_ID.csv', 'w') as f:
    for pair in movie_ID_sim_movie_ID:
        f.write("%s,%s\n" % (pair[0], pair[1]))


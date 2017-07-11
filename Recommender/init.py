from os.path import isfile

from models.Movie import Movie
from random import randint
from models.User import User
import numpy as np
import math
from imdb import IMDb
import os
import operator
from scipy import spatial
from scipy.stats.stats import pearsonr

users = []
movies = []
userIndexMap = {}
indexUserMap = {}
movieIndexMap = {}
indexMovieMap = {}
movieLink = {}

matrix = np.zeros((1,1))

def init_data():
    fill_movies()
    fill_users()

    # set_matrix(np.random.randint(6, size=(len(users), len(movies))))
    set_matrix()

    print matrix.shape
    # setMoviesHTML()

    # pearson_similarity(users[3].username)
    # print pearson_def([0,0,1], [1,5,7])
    # init_IMDBb()

    # centered_cosine_similarity(users[1].username)

    # jaccard_similarity(users[4].username)

def setMoviesHTML():
    table = "<table class='table table-striped table-bordered' style='width: 100%; background: white; table-layout: fixed;' id='notRatedTable'>\n"
    table = table + "\t<thead>\n\t\t<tr><td>Title</td></tr>\n\t</thead>\n\t<tbody>\n"
    for asd, movie in enumerate(movies):
        print str(asd) + " " + movie
        table = table + "\t\t<tr style='cursor: pointer;' onclick='movieDetails(\"" + movie + "\")'>\n\t\t<td>" + movie + "</td>\n\t</tr>\n"
    table = table + "\n\t</tbody>\n</table>"

    f = open(os.path.dirname(__file__) + "/static/all_movies_table.html", 'w')
    f.write(table.encode("ascii", "ignore"))  # python will convert \n to os.linesep
    f.close()

def init_IMDBb():

    ia = IMDb()

    movie = ia.get_movie('0094878')
    # for movie in indiana:
    #     print str(movie)+'\n'
    # print movie['cover url']
    # for name in movie.keys():
    #     print(name)
    # for person in ia.search_person('Mel Gibson'):
    #     print person.personID, person['name']


def fill_users():
    global users
    if os.path.isfile(os.path.dirname(__file__) + "/data/users.npy"):
        users = np.load(os.path.dirname(__file__) + "/data/users.npy")
        for i, user in enumerate(users):
            userIndexMap[user.username] = i
            indexUserMap[i] = user.username
    else:
        users = []
        for i in range(10):
            username = "username"+str(i)
            password = "password"+str(i)
            full_name = "fullName"+str(i)

            users.append(User(username, password, full_name))
            userIndexMap[username] = i
            indexUserMap[i] = username

        np.save(os.path.dirname(__file__) + "/data/users", users)


def register_new_user(username, password, full_name):
    global matrix
    for user in users:
        if user.username == username:
            return False

    users.append(User(username, password, full_name))
    userIndexMap[username] = len(users)-1
    indexUserMap[len(users)-1] = username

    matrix = np.concatenate((matrix, np.zeros((1, len(movies)))), axis=0)
    print matrix.shape

    np.save(os.path.dirname(__file__) + "/data/users", users)
    return True

def fill_movies():
    f = open(os.path.dirname(__file__) + "/movies/links.txt")

    i = 0
    for movie in f.readlines():
        movie_link = movie.strip().decode("utf8")
        movie_link = movie_link.rsplit(',',1)
        movieIndexMap[movie_link[0]] = i
        indexMovieMap[i] = movie_link[0]
        movieLink[movie_link[0]] = movie_link[1]
        movies.append(movie_link[0])
        i = i+1

    f.close()


def get_all_movies():
    return movies


def get_not_rated_movies(username):
    retMovies = []
    my_movies = get_movies_for_username(username)
    for idx, rate in enumerate(my_movies):
        if rate == 0:
            movie = indexMovieMap[idx]
            retMovies.append(movie)

    return retMovies


def rate_movie(username, title, rate):
    try :
        print username
        usernameIndex = userIndexMap.get(username)
        movieIndex = movieIndexMap.get(title)
        matrix[usernameIndex,movieIndex] = rate
        np.save(os.path.dirname(__file__) + "/data/matrix", matrix)
        return True
    except Exception:
        return False

def read_users():
    users_str = ""
    for user in users:
        users_str = users_str + "\n"+user.to_string()

    return users_str


def set_matrix():
    global matrix
    matrix = np.zeros((len(users), len(movies)))
    if os.path.isfile(os.path.dirname(__file__) + "/data/matrix.npy"):
        matrix = np.load(os.path.dirname(__file__) + "/data/matrix.npy")
    else:
        np.save(os.path.dirname(__file__) + "/data/matrix", matrix)


def loginUser(username, password):
    for user in users:
        if np.logical_and(user.username == username, user.password == password):
            return user
    return None


def get_user(username):
    for user in users:
        if user.username == username:
            return user

    return None


def get_movies_for_username(username):
    index = userIndexMap.get(username)
    return matrix[index, :]


def get_movie_name_rating(username):
    movieMap = {}
    ratings = get_movies_for_username(username)
    for id, rate in enumerate(ratings):
        mn = indexMovieMap.get(id).decode("utf8")
        movieMap[mn] = rate

    movieMap = sorted(movieMap.items(), key=operator.itemgetter(1), reverse=True)
    return movieMap


def movies_i_watched(username):
    movieMap = {}
    ratings = get_movies_for_username(username)
    for id, rate in enumerate(ratings):
        if rate != 0:
            mn = indexMovieMap.get(id)
            movieMap[mn] = rate

    movieMap = sorted(movieMap.items(), key=operator.itemgetter(1), reverse=True)
    return movieMap


def get_movies():
    return indexMovieMap


def get_plot(title):
    id = movieLink.get(title)
    movie = IMDb().get_movie(id)
    return movie['plot']


def get_movie_from_imdb(title):
    id = movieLink.get(title)
    return IMDb().get_movie(id)


def get_cover(title):
    id = movieLink.get(title)
    movie = IMDb().get_movie(id)
    return movie['cover url']


def get_genres(title):
    id = movieLink.get(title)
    movie = IMDb().get_movie(id)
    return movie['genres']


def get_year(title):
    id = movieLink.get(title)
    movie = IMDb().get_movie(id)
    return movie['year']


def get_movies_for_similar(myUsername, similar_users):
    topMovies = []
    retTopMovies = []
    myMovies = get_movies_for_username(myUsername)
    newUser = True
    for username, value in similar_users:
        if np.logical_and(abs(value) >= 0.0001, not np.isnan(value)):
            newUser = False
            break

    if newUser:
        return new_user()

    for username, value in similar_users:
        if np.logical_and(abs(value) >= 0.0001, not np.isnan(value)):
            hisMovies = get_movies_for_username(username)
            hisMovies = np.array(hisMovies, dtype=np.int)
            for myIndex, tempValue in enumerate(hisMovies):  # his movies are set to 0 if i watched them
                if np.logical_and(myMovies[myIndex] != 0, hisMovies[myIndex] != 0):
                    hisMovies[myIndex] = 0
            for num, hisRate in enumerate(hisMovies):
                if hisRate != 0:
                    if indexMovieMap.get(num) not in topMovies:
                        topMovies.append(indexMovieMap.get(num))
                        retTopMovies.append([indexMovieMap.get(num), float("{0:.3f}".format(value))])
                    elif indexMovieMap.get(num) in topMovies:
                        index = topMovies.index(indexMovieMap.get(num))
                        retMovieValue = retTopMovies[index]
                        if value > retMovieValue[1]:
                            retTopMovies.pop(index)
                            retTopMovies.insert(index, [indexMovieMap.get(num), float("{0:.3f}".format(value))])


    print len(retTopMovies)
    return retTopMovies


def jaccard_similarity(username):
    print "Username: "+str(username)
    global matrix
    similar_users = {}
    my_movies = get_movies_for_username(username)
    my_movies = np.array(my_movies)
    my_movies_zero = np.where(my_movies != 0)[0]
    print matrix
    for idx, row in enumerate(matrix):
        print str(idx)+' row: '+str(row)
        union = 0
        intersection = 0
        # for i, value in enumerate(row):
        #     if np.logical_and(value != 0, my_movies[i] != 0):
        #         union = union+1
        #         intersection = intersection+1
        #     elif np.logical_and(value != 0, my_movies[i] == 0):
        #         union = union+1
        #     elif np.logical_and(value == 0, my_movies[i] != 0):
        #         union = union+1

        rowArray = np.array(row)
        row_non_zero = np.where(rowArray != 0)[0]
        print "Row: "+str(row_non_zero)
        print "My zero:" +str(my_movies_zero)
        intersection = len(np.intersect1d(row_non_zero, my_movies_zero))
        union =  len(np.unique(np.concatenate((row_non_zero, my_movies_zero), axis=0)))

        if union != 0:
            similarity = float(intersection)/union
            similar_users[indexUserMap.get(idx)] = similarity
        else:
            similar_users[indexUserMap.get(idx)] = 0.0


    similar_users.pop(username)

    similar_users = sorted(similar_users.items(), key=operator.itemgetter(1), reverse=True)
    print 'SimilarUsers: ' + str(similar_users)

    movieList = get_movies_for_similar(username, similar_users)
    # print "JaccardMovieList:" + str(movieList)
    return movieList


def cosine_similarity(username):
    print "Username: "+str(username)
    global matrix
    similar_users = {}
    print matrix.shape
    my_movies = get_movies_for_username(username)
    for idx, row in enumerate(matrix):
        # print str(idx) + ' row: ' + str(row)
        similarity = 1 - spatial.distance.cosine(my_movies, row)
        similar_users[indexUserMap.get(idx)] = similarity

    similar_users.pop(username)

    similar_users = sorted(similar_users.items(), key=operator.itemgetter(1), reverse=True)
    print 'SimilarUsers: '+ str(similar_users)

    movieList = get_movies_for_similar(username, similar_users)
    # print 'CosineMovieList: '+ str(movieList)
    return movieList

def centered_cosine_similarity(username):
    print "Username: "+str(username)
    global matrix
    similar_users = {}
    print matrix.shape
    my_movies = center_row(get_movies_for_username(username))
    print my_movies
    for idx, row in enumerate(matrix):
        # print str(idx) + ' row: ' + str(row)

        rowArray = center_row(row)

        similarity = 1 - spatial.distance.cosine(my_movies, rowArray)
        similar_users[indexUserMap.get(idx)] = similarity

    similar_users.pop(username)

    similar_users = sorted(similar_users.items(), key=operator.itemgetter(1), reverse=True)
    print 'SimilarUsers: '+ str(similar_users)

    movieList = get_movies_for_similar(username, similar_users)
    # print 'CosineMovieList: '+ str(movieList)
    return movieList

def center_row(row):
    rowArray = np.array(row)
    row_mean = rowArray[rowArray.nonzero()].mean()
    for rowId, val in enumerate(rowArray):
        if val != 0:
            rowArray[rowId] = val - row_mean
    return rowArray

def pearson_similarity(username):
    my_movies = get_movies_for_username(username)
    similar_users = {}
    for idx, row in enumerate(matrix):
        similarity = pearson_def(my_movies, row)
        similar_users[indexUserMap.get(idx)] = similarity

    similar_users.pop(username)

    similar_users = sorted(similar_users.items(), key=operator.itemgetter(1), reverse=True)
    print 'SimilarUsers: ' + str(similar_users)

    movieList = get_movies_for_similar(username, similar_users)
    print 'PearsonMovieList: '+ str(movieList)
    return movieList

def average(x):
    assert len(x) > 0
    return float(sum(x)) / len(x)


def pearson_def(x, y):
    assert len(x) == len(y)
    n = len(x)
    assert n > 0
    avg_x = average(x)
    avg_y = average(y)
    diffprod = 0
    xdiff2 = 0
    ydiff2 = 0
    for idx in range(n):
        xdiff = x[idx] - avg_x
        ydiff = y[idx] - avg_y
        diffprod += xdiff * ydiff
        xdiff2 += xdiff * xdiff
        ydiff2 += ydiff * ydiff
    # print math.sqrt(xdiff2 * ydiff2)
    if math.sqrt(xdiff2 * ydiff2) != 0:
        return diffprod / math.sqrt(xdiff2 * ydiff2)
    else:
        return 0


def new_user():
    tempMatrix = np.matrix(matrix)
    if not tempMatrix.any():
        return random_movies()
    ret = []
    n = 250
    for i in range(n):
        if not tempMatrix.any():
            break
        maxcol = tempMatrix.sum(axis=0).argmax()
        ret.append([indexMovieMap.get(maxcol), n-i])
        x = np.zeros((len(users), 1))
        tempMatrix[:, maxcol] = x

    return ret


def random_movies():
    ret = []
    for i in range(250):
        randNum = randint(0, len(movies))
        ret.append([indexMovieMap.get(randNum), randNum])

    return ret

from imdb import IMDb
import os.path

from flask import Flask, json, render_template, request, Response
import numpy as np

from init import init_data, loginUser, get_user, jaccard_similarity, get_movies_for_username, get_movie_name_rating, \
    movies_i_watched, get_plot, get_cover, get_year, get_genres, get_movie_from_imdb, cosine_similarity, get_all_movies, \
    get_not_rated_movies, rate_movie, pearson_similarity, centered_cosine_similarity, register_new_user

app = Flask(__name__)

# reload(sys)
# sys.setdefaultencoding('utf8')

init_data()


@app.route('/')
def hello_world():


    return render_template("home.html", login="initial")


@app.route('/profile/<username>/<password>')
def get_user_route(username, password):
    user = loginUser(username, password)
    if user != None:
        return render_template("profile.html", username=user.username, fullName=user.fullName)
    return render_template("home.html", login="unsuccessful")

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username'].encode("ascii", "ignore")
    password = request.form['password']
    full_name = request.form['full_name']
    register_new_user(username, password, full_name)
    return render_template("home.html", login="unsuccessful", register="unsuccessfull")



@app.route('/profile', methods=['POST'])
def profile():
    username = request.form['username'].encode("ascii", "ignore")
    password = request.form['password']
    user = loginUser(username, password)
    if user is not None:
        return render_template("profile.html", username=user.username, full_name=user.fullName)
    return render_template("home.html", login="unsuccessful")


@app.route('/my_movies', methods=['POST'])
def ratedMovies():
    username = request.form['username'].encode("ascii", "ignore")
    my_movies = movies_i_watched(username)
    # print my_movies
    # retMovies = []
    # for i, movie in enumerate(my_movies):
    #     if i > (number * 10 + 10):
    #         break
    #     elif np.logical_and(i > (number * 10), i < (number * 10 + 10)):
    #         retMovies.append(movie)
    print my_movies
    # pages = len(my_movies)/10 + 1
    return render_template("rated.html", username=username, my_movies=my_movies)


@app.route('/not_rated', methods=['POST'])
def notRatedMovies():
    username = request.form['username']
    all_movies = get_all_movies()
    return render_template('all_movies.html', username=username, all_movies=all_movies)


@app.route('/rate', methods=['POST'])
def rateMovie():
    username = request.form['username'].encode("ascii", "ignore")
    title = request.form['title']
    rate = request.form['rate']
    print "Username: "+username+", Title: "+title+" Rate: "+rate
    if rate_movie(username, title, rate):
        return render_template("toast.html", message = ""+title+" is rated successfully")
    else:
        return render_template("toast.html", message="" + title + " is rated unsuccessfully")



@app.route('/movie_details', methods=['POST'])
def movieDetails():
    print "movieDetails"
    try:
        username = request.form['username'].encode("ascii", "ignore")
        title = request.form['title']
        print "Username: "+username
        print "Title: "+title
        movie = get_movie_from_imdb(title)
        cover = movie['cover url']
        plot = movie['plot']
        genres = movie['genres']
        return render_template("details.html", username=username, title=title, plot=plot, cover=cover, genres=genres)
    except Exception:
        return render_template("details.html", title=title, plot='Not available', cover='', genres=[])


@app.route('/jaccard_method', methods=['POST'])
def jaccard_method():
    username = request.form['username'].encode("ascii", "ignore")
    # number = int(request.form['number'])
    # retMovies = []
    # for i, movie in enumerate(jaccard_similarity(username)):
    #     if i > (number * 10 + 10):
    #         break
    #     elif np.logical_and(i >= (number * 10), i < (number * 10 + 10)):
    #         retMovies.append(movie)
    # pages = len(retMovies)/10 + 1
    return render_template("recommended.html", method= 'Jaccard', username=username, movies=jaccard_similarity(username))


@app.route('/cosine_method', methods=['POST'])
def cosine_method():
    username = request.form['username'].encode("ascii", "ignore")
    print username
    # number = int(request.form['number'])
    # retMovies = []
    # for i, movie in enumerate(cosine_similarity(username)):
    #     if i > (number * 10 + 10):
    #         break
    #     elif np.logical_and(i >= (number * 10), i < (number * 10 + 10)):
    #         retMovies.append(movie)
    return render_template("recommended.html", method= 'Cosine', username=username, movies=cosine_similarity(username))


@app.route('/centered_cosine_method', methods=['POST'])
def centered_cosine_method():
    username = request.form['username'].encode("ascii", "ignore")
    print username
    # number = int(request.form['number'])
    # retMovies = []
    # for i, movie in enumerate(cosine_similarity(username)):
    #     if i > (number * 10 + 10):
    #         break
    #     elif np.logical_and(i >= (number * 10), i < (number * 10 + 10)):
    #         retMovies.append(movie)
    return render_template("recommended.html", method= 'Centered cosine', username=username, movies=centered_cosine_similarity(username))


@app.route('/pearson_method', methods=['POST'])
def pearson_method():
    username = request.form['username'].encode("ascii", "ignore")
    print username
    # number = int(request.form['number'])
    # retMovies = []
    # for i, movie in enumerate(cosine_similarity(username)):
    #     if i > (number * 10 + 10):
    #         break
    #     elif np.logical_and(i >= (number * 10), i < (number * 10 + 10)):
    #         retMovies.append(movie)
    return render_template("recommended.html", method= 'Pearson', username=username, movies=pearson_similarity(username))


if __name__ == '__main__':
    app.run()

class Movie(object):
    name = ""
    id = ""
    poster = ""
    plot = ""
    genres = []
    rating = 0.0

    def __init__(self, name, id, poster, plot, genres, rating):
        self.name = name
        self.id = id
        self.poster = poster
        self.plot = plot
        self.genres = genres
        self.rating = rating

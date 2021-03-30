# functions to paw through a movie directory recursively go fetch the 
# ratings for all the movies and then recommend movies to cull based 
# on that rating.

import re
import urllib3
import urllib.parse
import json
import os, sys

def getMovieList(moviedir_path, movielist_path) -> list:
    print ('INFO: Creating Movie list.')
    os.system('find ' + moviesdir_path + ' -type f >> '+ movielist_path)
    print ('INFO: Finished creating movie list.')
    movies_file = open(movielist_path, 'r')
    retVal = movies_file.readlines()
    movies_file.close()

    return retVal

# Given a filename for maybe a movie, return the title if it's got a movie extension,
# else return ''
# expect filenames to be in Title (Year).mp4 (or some other video extension)
def getMovieName(path_to_file: str) -> str:
    allowedfileformats = [".m4v", ".mov",".mp4",".mpg", ".wmv"]
    path_to_file = path_to_file.lower().strip()
    if len(path_to_file) <= 0:
        return ''

    split_name = os.path.splitext(os.path.basename(path_to_file.strip()))
    if split_name[1] not in allowedfileformats:
        return ''
    
    return split_name[0]

# This works using omdb API which queries for the title and if we have a year
# it uses that to. If you get the year wrong by even 1 year it will return movie
# not found.
# If you are pulling this from github, you'll need to get an API key from omdbapi.com
# they allow 1000 queries a day without paying. If you want to use this seriously, consider
# throwing the dev a bone.
# key - filename
# value - rating
def getRatings(movie_list: list, API_key: str) -> dict:
    print ('INFO: Fetching ratings.')
    url = 'http://www.omdbapi.com/?apikey=' + API_key + '&t='
    http = urllib3.PoolManager()
    ratings = {}
    count = 0

    for movie in movie_list:
        # check this is an actual movie, not '.' or something
        movie = movie.strip()
        title = getMovieName(movie)
        if title == '':
            continue
        
        count += 1
        movie_info = title.split('(')
        query_url = url + urllib.parse.quote(movie_info[0].strip())
        if (len(movie_info) == 2):
            movie_info[1] = movie_info[1].strip()[0:-1]
            query_url = query_url + '&y=' + movie_info[1]
        r = http.request('GET', query_url)
        if r.status != 200:
            print("Error calling API with URL " + url)
        else:
            data = json.loads(r.data.decode('utf-8'))
            if data['Response'] == 'False':
                print('WARNING: Couldn''t find ' + movie + ' in the database.')
            else:
                if 'imdbRating' in data and data['imdbRating'] != 'N/A':
                    # consider having try catch block here to stop erroring while processing
                    ratings[movie] = float(data['imdbRating'].strip())
                else:
                    print ('WARNING: No rating returned for ' + movie)

    return ratings
    
def findBadMovies(movierating_path, bad_movie_path, rating_threshold):
    print ('INFO: Finding the bad movies.')
    infile = open(movierating_path, 'r')
    movies = infile.readlines()
    infile.close()
    outfile = open(bad_movie_path, 'a')

    for movie in movies:
        movie_info = movie.split('***')
        rating = float(movie_info[1].strip())
        if rating < rating_threshold:
            outfile.write(movie)
    
    outfile.close()

# This works using omdb API which queries for the title and if we have a year
# it uses that to. If you get the year wrong by even 1 year it will return movie
# not found.
# If you are pulling this from github, you'll need to get an API key from omdbapi.com
# they allow 1000 queries a day without paying. If you want to use this seriously, consider
# throwing the dev a bone.
# key - filename
# value - rating
def simpleGetRatings(movie_list: list, API_key: str) -> dict:
    print ('INFO: Fetching ratings.')
    url = 'http://www.omdbapi.com/?apikey=' + API_key + '&t='
    infile = open(cleanmovielist_path, 'r')
    movies = infile.readlines()
    infile.close()
    http = urllib3.PoolManager()
    outfile = open(movierating_path,"a")
    count = 0

    for movie in movies:
        count += 1
        if count > 5:
            break
        movie_info = movie.split('(')
        query_url = url + urllib.parse.quote(movie_info[0].strip())
        if (len(movie_info) == 2):
            movie_info[1] = movie_info[1].strip()[0:-1]
            query_url = query_url + '&y=' + movie_info[1]
        r = http.request('GET', query_url)
        if r.status != 200:
            print("Error calling API with URL " + url)
        else:
            data = json.loads(r.data.decode('utf-8'))
            if data['Response'] == 'False':
                print('WARNING: Couldn''t find ' + movie.strip() + ' in the database.')
            else:
                outline = movie.strip() + ' *** ' + data['imdbRating'].strip()
                outfile.write(outline + '\n')

    outfile.close()
    
def findBadMovies(ratings: dict, bad_movie_path: str, rating_threshold: float) -> None:
    print ('INFO: Finding the bad movies.')
    outfile = open(bad_movie_path, 'a')

    for movie, rating in ratings.items():
        if rating < rating_threshold:
            outfile.write('# ' + movie + ' *** Rating: ' + str(rating) + '\n')
            outfile.write('rm ' + movie + '\n')
            outfile.flush()
    
    outfile.close()


def deletefiles(files):
    print ('INFO: Removing temp files.')
    for filename in files:
        os.path.exists(filename) and os.remove(filename)

# Change the variables below to suit your scanning needs.
# moviesdir_path - where you keep your movies
# movielist_path - temp file of all movies found
# API_key - get yours and put it there.
# rating_threshold - what is the minimum rating to not be on report
# bad_movie_path - where you want the report to show up    
if __name__=='__main__':
    moviesdir_path = '/Volumes/media/Movies'
    movielist_path = '/Users/dave.heberer/Documents/Movie_List.txt'
    bad_movie_path = '/Users/dave.heberer/Documents/BadMovies.txt'
    API_key = 'NOT_A_KEY' # you need to go get an API key of your own.
    rating_threshold = 7.0

    if API_key == 'NOT_A_KEY':
        print("Need an API key from OMDB, exiting..")
        exit()

    deletefiles([movielist_path, bad_movie_path])
    movies = getMovieList(moviesdir_path, movielist_path)
    ratings = getRatings(movies, API_key)
    findBadMovies(ratings, bad_movie_path, rating_threshold)
    # deletefiles([movielist_path, cleanmovielist_path, movierating_path])
    print ('Processing Complete')

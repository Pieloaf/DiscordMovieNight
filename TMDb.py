import requests
import os
from const import SEARCHURL, MOVIEURL, IMAGEURL, GETIMAGE
from urllib.parse import quote as encode

with open('./TMDbToken') as file:
    TMDbToken = file.readlines()[0]


def search(query, year=''):
    result = requests.get(SEARCHURL.format(
        TMDbToken, encode(query), year)).json()
    if result['total_results'] == 0:
        return('Error: Movie Not Found')

    movies = result['results']
    for movie in movies:
        if movie['title'].lower() == query.lower():
            return movieData(movie)
    return movieData(movies[0])


def movieData(movie):
    return {
        'url': MOVIEURL.format(movie['id']),
        'name': movie['title'],
        'year': movie['release_date'][:4],
        'score': int(float(movie['vote_average'])*10)
    }


def getThumb(id):
    try:
        image = requests.get(GETIMAGE.format(id, TMDbToken, 'en')).json()[
            'posters'][0]['file_path']
    except IndexError:
        image = requests.get(GETIMAGE.format(id, TMDbToken, '')).json()[
            'posters'][0]['file_path']
    return(IMAGEURL.format(image))

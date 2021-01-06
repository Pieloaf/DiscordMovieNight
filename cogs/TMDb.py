import requests
import os
from const import URL

with open('./TMDbToken') as file:
    TMDbToken = file.readlines()


def search(TMDbToken, query):
    result = requests.get(URL.format(TMDbToken, query))
    result.json()['results'][0]

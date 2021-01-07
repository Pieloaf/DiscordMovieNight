voteEmotes = [
    '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣'
]
usefulEmotes = {'yes': '✅', 'no': '❌'}

voteEmbed = {
    "title": "Movie Vote",
    "description": "Vote for which movie you want to watch",
    "color": 3385832,
    "thumbnail": {
        "url": "https://image.flaticon.com/icons/png/512/195/195158.png"
    }
}

# Discord Messages
REMOVEMOVIE = "React to remove a movie"
LISTFULL = "Movie Vote List is Full"
MOVIEEXISTS = "There is already a movie vote, use `+addMovie [Title]` to add to the list"
NOVOTE = "There is currently no movie vote. Use `+movievote` to start the vote"

# TMDb URLs
SEARCHURL = 'https://api.themoviedb.org/3/search/movie?api_key={}&query={}&primary_release_year={}'
MOVIEURL = 'https://www.themoviedb.org/movie/{}'
IMAGEURL = 'https://www.themoviedb.org/t/p/w600_and_h900_bestv2{}'

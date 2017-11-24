#
# This program gets the movies we are interested in
#

import json
import sys

targets = ["Tarantino, Quentin", "Anderson, Wes", "Thurman, Uma", "McDormand, Frances", "Keitel, Harvey", "Murray, Bill"]

def main():
    flag = ""
    movies_cast = {}
    if len(sys.argv) == 2 and sys.argv[1] == "-m":
        flag = "-m"
    with open(f"movies-cast{flag}.json", "r", encoding="ISO-8859-1") as f:
        movies = json.load(f)
    for movie, v in movies.items():
        for targ in targets:
            if not movies_cast.get(movie) and ((targ in v["actors"]) or (targ in v["directors"])):
                movies_cast[movie] = v
    actors = []
    directors = []
    movies = {}
    actors_movies = {}
    directors_movies = {}
    for name, v in movies_cast.items():
        movies[name] = v["year"]
        for director in v["directors"]:
            if not directors_movies.get(director):
                directors.append(director)
                directors_movies[director] = {}
            directors_movies[director][name] = v["year"]
        for actor in v["actors"]:
            if not actors_movies.get(actor):
                actors.append(actor)
                actors_movies[actor] = {}
            actors_movies[actor][name] = v["year"]
    with open(f"target-actors{flag}.json", "wb+") as f:
        f.write(json.dumps(actors, indent=1, ensure_ascii=False).encode("utf8"))
    with open(f"target-directors{flag}.json", "wb+") as f:
        f.write(json.dumps(directors, indent=1, ensure_ascii=False).encode("utf8"))
    with open(f"target-actors-movies{flag}.json", "wb+") as f:
        f.write(json.dumps(actors_movies, indent=1, ensure_ascii=False).encode("utf8"))
    with open(f"target-directors-movies{flag}.json", "wb+") as f:
        f.write(json.dumps(directors_movies, indent=1, ensure_ascii=False).encode("utf8"))
    with open(f"target-movies{flag}.json", "wb+") as f:
        f.write(json.dumps(movies, indent=1, ensure_ascii=False).encode("utf8"))
    with open(f"target-movies-cast{flag}.json", "wb+") as f:
        f.write(json.dumps(movies_cast, indent=1, ensure_ascii=False).encode("utf8"))

if __name__ == '__main__':
    main()

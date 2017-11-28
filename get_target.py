#
# This program gets the lists we are interested in
#

import json
import sys
import re

targets = ["Tarantino, Quentin", "Anderson, Wes", "Thurman, Uma", "McDormand, Frances", "Keitel, Harvey", "Murray, Bill"]

def main():
    flag = ""
    movies_cast = {}
    repeated = {}
    if len(sys.argv) == 2 and sys.argv[1] == "-m":
        flag = "-m"
    with open(f"movies-cast{flag}.json", "r", encoding="ISO-8859-1") as f:
        movies = json.load(f)
    for full_title, v in movies.items():
        for targ in targets:
            if (targ in v["actors"]) or (targ in v["directors"]):
                m = re.match("(?P<title>.+?) \((?P<year>[0-9\?]+?)([\/IVXLCD]+)*\)$", full_title)
                movie = m.group("title")
                year = m.group("year")
                #print(full_title)
                #print(movie)
                if movies_cast.get(movie):
                    if not repeated.get(movie):
                        tmp = movies_cast[movie]
                        movies_cast[movie + " " + tmp["year"]] = tmp
                        movies_cast.pop(movie)
                        repeated[movie] = True
                    movie = movie + " " + year
                movies_cast[movie] = v
                movies_cast[movie]["year"] = year
                break
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

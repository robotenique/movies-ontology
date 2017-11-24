#
# This program gets the movies we are interested in
#

import json

targets = ["Tarantino, Quentin", "Anderson, Wes", "Thurman, Uma", "McDormand, Frances", "Keitel, Harvey", "Murray, Bill"]

def main():
    d = {}
    with open("movies-cast.json", "r", encoding="ISO-8859-1") as f:
        movies = json.load(f)
    for movie, v in movies.items():
        for targ in targets:
            if not d.get(movie) and ((targ in v["actors"]) or (targ in v["directors"])):
                d[movie] = v
    with open("target-movies.json", "wb+") as f:
        f.write(json.dumps(d, indent=1, ensure_ascii=False).encode("utf8"))

if __name__ == '__main__':
    main()

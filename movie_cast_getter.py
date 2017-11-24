#
# This program puts together the three lists to build the cast of the movies
#

import json
import re

def main():
    d = {}
    print("WARNING: Make sure to have at least 4GB of free RAM while running this!!!")
    print("Importing actors...")
    with open("actors.json", "r", encoding="ISO-8859-1") as f:
        actors = json.load(f)
    for name, v in actors.items():
        name = re.sub("\([IVXLDCM]+\)", "", name).strip()
        for movie, year in v.items():
            if not d.get(movie):
                d[movie] = {"year": year, "directors": [], "actors": []}
            d[movie]["actors"].append(name)
    print("Done")
    print("Importing actresses...")
    with open("actresses.json", "r", encoding="ISO-8859-1") as f:
        actresses = json.load(f)
    for name, v in actresses.items():
        name = re.sub("\([IVXLDCM]+\)", "", name).strip()
        for movie, year in v.items():
            if not d.get(movie):
                d[movie] = {"year": year, "directors": [], "actors": []}
            d[movie]["actors"].append(name)
    print("Done")
    print("Importing directors...")
    with open("directors.json", "r", encoding="ISO-8859-1") as f:
        directors = json.load(f)
    for name, v in directors.items():
        name = re.sub("\([IVXLDCM]+\)", "", name).strip()
        for movie, year in v.items():
            if not d.get(movie):
                d[movie] = {"year": year, "directors": [], "actors": []}
            d[movie]["directors"].append(name)
    print("Done")
    f = open("movies-cast.json", "wb+")
    f.write(json.dumps(d, indent=1, ensure_ascii=False).encode("utf8"))
    f.close()

if __name__ == '__main__':
    main()

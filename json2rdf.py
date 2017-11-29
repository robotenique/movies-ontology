import json
import string
import datetime
import pytz
import re

def init_movie(movie_name, date):
    redux = "".join(list(filter(lambda c: str.isalnum(c) or c == ' ', string.capwords(movie_name).replace(" ", ""))))
    comm = movie_name.replace("&", "and")
    date = datetime.datetime(year=date, month=1, day=1, tzinfo=pytz.utc).isoformat()

    rdf = f"""<!-- http://www.ime.usp.br/~renata/FOAF-modified#{redux} -->

    <owl:NamedIndividual rdf:about="http://www.ime.usp.br/~renata/FOAF-modified#{redux}">
        <rdf:type rdf:resource="http://www.ime.usp.br/~renata/FOAF-modifiedMovie"/>
        <renata:FOAF-modifiedlaunchDate rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">{date}</renata:FOAF-modifiedlaunchDate>
        <renata:FOAF-modifiedtitle rdf:datatype="http://www.w3.org/2001/XMLSchema#string">{comm}</renata:FOAF-modifiedtitle>
    </owl:NamedIndividual>"""

    return rdf

def prepare_movie_rdf(file):
    movie_rdf = {}
    with open(file, "r") as f:
        d = json.loads(f.read())
        for mov in d.keys():
            if d[mov].isnumeric():
                movie_rdf[mov] = init_movie(mov, int(d[mov]))

    return movie_rdf

def main():
    t = prepare_movie_rdf("target-movies-m.json")

    for k in t.keys():
        print(t[k])
        print("")


if __name__ == '__main__':
    main()

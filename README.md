# movies-ontology

In this project, we create an [ontology](https://en.wikipedia.org/wiki/Ontology_(information_science)) of movies, by parsing iMDb datasets and adding them into our ontology. The modelling of the ontology was made with [Protégé](https://protege.stanford.edu), an open-source ontology editor.

We can express the concepts and relations between them concepts/properties of the ontology by using DL ([Description Logic](https://en.wikipedia.org/wiki/Description_logic)). This is very useful because the Reasoner can use the properties and relations expressed in our ontology to "reason", i.e. infer rules and relationships implied by our core logic, without the need for the user to explicitly describe it in the ontology creation. The queries to our ontology can be made using [SPARQL](https://en.wikipedia.org/wiki/SPARQL).

![protege](https://i.stack.imgur.com/X6x1q.png)

**OBS:** The iMDb raw files aren't in this repo (too big to put here), only our ontology (in different formats for convenience).

## Contributors

* **Juliano Garcia** - [@robotenique](https://github.com/robotenique)
* **João Gabriel** - [@icemage144](https://github.com/IceMage144)
* **Pedro Pereira** - [@pedro823](https://github.com/pedro823)

## 1. **imdbAnalyzer**
Parser for the imdb *.list* files, in python 3.6, and the parsed dictionaries are saved using the **pickle** library in *.pkl* format in the *obj/* folder. In this parser, we used a lot of Regexpr to filter valid movies to our ontology, so the code can be a little hard to read.

## 2. **get_target**
Since the iMDb files are too big, we can first filter the rows which relate to actors/actresses, director, movie title, etc. that we specifically want, and then build the ontollogy on top of that. This program open the full json files, filter them, and outputs the filtered json.

## 3. **json2rdf**
This program converts our .json files to entrances in our ontology. This automate the process of adding new information to our ontology. Our ontology can them be opened on Protégé, and be converted to different formats other than RDF.

## 4. **sparql_queries.txt**
In this TXT file, we have 10 sample queries written in *SPARQL*, to our ontology. This is used to exemplify how someone can query the ontology (and also as an introduction to SPARQL). The results of each query are in the *screenshots/* folder. You can run the queries directly in Protégé, but the recommended way of doing so is by using a standalone SPARQL processor. In this project, we used [ARQ - A SPARQL Processor for Jena](https://jena.apache.org/documentation/query/)

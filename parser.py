#
# This program parses the .list files from imdb
#

import re
import json
import sys

valid = ["actors", "actresses", "directors"]

def main():
    if len(sys.argv) < 2:
        print("You have to pass the name of the list you wanna parse as argument (e.g.: python parser.py actors)")
        exit()
    if sys.argv[1] not in valid:
        print("The argument passed is not valid, you can only parse actors, actresses or directors")
        exit()
    listName = sys.argv[1]
    f = open(f"{listName}.list", "r", encoding="ISO-8859-1")
    line = f.readline()
    initLine = f"THE {listName.swapcase()} LIST"
    while initLine not in line:
        line = f.readline()
    for i in range(4):
        f.readline()
    actual = False
    d = {}
    for i, line in enumerate(f):
        if i%50000 == 0:
            print(f"Line {i}")
        if "-------------------------------" in line:
            break
        if line[0] == "\n" or re.search("\(VG\)", line) or re.search("\(TV\)", line):
            continue
        if line[0] == "\t":
            m = re.match("\t*\"?(?P<title>.+?)\"? *(\(.*?\))? *(\((?P<year>[0-9\?]+?)([\/IVXLCD]+)*\))[^\{\}]*$", line)
        else:
            m = re.match("(?P<name>.*)\t+\"?(?P<title>.+?)\"? *(\(.*?\))? *(\((?P<year>[0-9\?]+?)([\/IVXLCD]+)*\))[^\{\}]*$", line)
        if not m:
            m2 = re.search("\{|\}", line)
            if not m2:
                raise NameError(f"Cannot parse line {i}: {line.strip()}")
            continue
        if not m.group("title"):
            raise NameError(f"Cannot find title at line {i}: {line.strip()}")
        if not m.group("year"):
            raise NameError(f"Cannot find year at line {i}: {line.strip()}")
        if line[0] != "\t":
            actual = re.sub("\([IVXLDCM]+\)", "", m.group("name")).strip()
            d[actual] = {}
        d[actual][m.group("title")] = m.group("year")
    g = open(f"{listName}.json", "wb+")
    g.write(json.dumps(d, indent=1, ensure_ascii=False).encode("utf8"))
    g.close()
    f.close()


if __name__ == '__main__':
    main()

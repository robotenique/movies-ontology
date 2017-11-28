#
# This program parses the .list files from imdb
#

import re
import json
import sys

valid = ["actors", "actresses", "directors"]

def main():
    flag = ""
    add = ""
    if len(sys.argv) < 2:
        print("You have to pass the name of the list you wanna parse as argument (e.g.: python parser.py actors)")
        exit()
    if len(sys.argv) == 3 and sys.argv[2] == "-m":
        flag = "-m"
        add = "[^\{\}]*$"
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
    m1 = f"\t+\"?(?P<title>.+?)\"? *(\(.*?\))? *(?P<year>\([0-9\?]+?([\/IVXLCD]+)*\)){add}"
    m2 = "(?P<name>.*)" + m1
    for i, line in enumerate(f):
        if i%50000 == 0:
            print(f"Line {i}")
        if "-------------------------------" in line:
            break
        if line[0] == "\n":
            continue
        if line[0] == "\t":
            m = re.match(m1, line)
        else:
            m = re.match(m2, line)
        if not m:
            m3 = re.search("\{|\}", line) if flag else None
            if not m3:
                raise NameError(f"Cannot parse line {i}: {line.strip()}")
            continue
        if not m.group("title"):
            raise NameError(f"Cannot find title at line {i}: {line.strip()}")
        if not m.group("year"):
            raise NameError(f"Cannot find year at line {i}: {line.strip()}")
        if line[0] != "\t":
            if d and not d[actual]:
                d.pop(actual)
            actual = re.sub("\([IVXLDCM]+\)", "", m.group("name")).strip()
            if not d.get(actual):
                d[actual] = {}
        if not flag or (flag and not re.search("(\(VG\)|\(TV\))", line)):
            d[actual][m.group("title") + " " + m.group("year")] = True
    g = open(f"{listName}{flag}.json", "wb+")
    g.write(json.dumps(d, indent=1, ensure_ascii=False).encode("utf8"))
    g.close()
    f.close()


if __name__ == '__main__':
    main()

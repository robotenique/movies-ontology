import re
import json
import pickle

# Save python objects in binary format
def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

class Act(object):
    def wsearch(w):
        return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

    def __init__(self, first, last):
        self.f = first
        self.l = last

    def regexp(self):
        return (Act.wsearch(self.f), Act.wsearch(self.l))

    def __repr__(self):
        return f"f: {self.f} l: {self.l}"

## Finding Actors Information!
#act_n = ["Uma Thurman", "Harvey Keitel", "Bill Murray", "Frances McDormand"]
#gen_st = "acts"
#act_n = ["Quentin Tarantino", "Wes Anderson"]
#gen_st = "directs"
act_man_f = "actors.list"
act_woman_f = "actresses.list"
#act_man_f = "directors.list"
#act_woman_f = "t"
#act_l = [(lambda n: Act(n[0], n[1]))([t.lower() for t in s.split()]) for s in act_n]
act_d = {}
mov_d = {}

def st_op(t):
    s = t
    p = s.find("(")
    count = 0
    while p < len(s) and p + 1 < len(s) and not s[p+1].isdigit() and not s[p+1] == '?':
        tlist = list(s)
        tlist[p] = '_'
        s = "".join(tlist)
        p = s.find("(")
        count += 1
        if count > 20:
            return len(t)
    return p


def find_person_movie(l, f):
    if l and l[0] != '\t':
        for i, a in enumerate(act_l):
            if all(x(l[:l.find('\t')].replace(",","")) for x in a.regexp()) and not act_d.get(act_n[i], None):
                cs = [l[l.find('\t'):st_op(l)].strip().replace("\t","").replace("\n","")]
                l = f.readline()
                while l and l[0] == '\t':
                    mv = l.strip().replace("\t", "").replace("\n","")
                    cs.append(mv[:st_op(mv)].strip())
                    l = f.readline()
                act_d[act_n[i]] = cs
    return l

def act_d_builder(l, f):
        if l and l[0] != '\t':
            print(l[:l.find('\t')].strip())
            if not act_d.get(l[:l.find('\t')].strip(), None):
                idx = l[:l.find('\t')].strip()
                if not list(filter(None, idx)):
                    return
                cs = [l[l.find('\t'):st_op(l)].strip().replace("\t","").replace("\n","")]
                l = f.readline()
                while l and l[0] == '\t':
                    mv = l.strip().replace("\t", "").replace("\n","")
                    cs.append(mv[:st_op(mv)])
                    l = f.readline()
                act_d[idx] = cs
        return l

def mov_actors_builder(l, f, movd):
    if l and l[0] != '\t':
        idx = l[:l.find('\t')].strip()
        if not list(filter(None, idx)):
            return
        cs = [l[l.find('\t'):st_op(l)].strip().replace("\t","").replace("\n","")]
        l = f.readline()
        while l and l[0] == '\t':
            mv = l.strip().replace("\t", "").replace("\n","")
            mv = mv[:st_op(mv)].strip()
            if mv in movd:
                if not mov_d.get(mv, None):
                    mov_d[mv] = set(idx)
                else:
                    mov_d[mv].add(idx)
                print(f"Adicionado em {mv} = {idx}")
            l = f.readline()
    return l



def build_movieDict():
    actd = load_obj("acts")
    drcd = load_obj("directs")
    movd = set()
    for block in list(actd.values()) + list(drcd.values()):
        for mov in block:
            movd.add(mov)
    return movd

def main():
    #print(load_obj("movies_actors"))
    #movd = build_movieDict()
    #print("Taxi Driver" in movd)
    #exit()
    with open(act_man_f, "r", encoding='latin-1') as m, open(act_woman_f, "r", encoding='latin-1') as w:
        c = 0
        lm = m.readline()
        lw = w.readline()
        while lm or lw:
            lm, lw = mov_actors_builder(lm, m, movd), mov_actors_builder(lw, w, movd)
            lm, lw = m.readline(),  w.readline()
            if c%50 == 0:
                print(f"{c}º iteration...")
                input("continua...")
            c+=1

    #print(json.dumps(mov_d, indent=5))
    save_obj(mov_d,"movies_actors")
if __name__ == '__main__':
    main()

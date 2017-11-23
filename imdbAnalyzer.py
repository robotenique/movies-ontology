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
act_n = ["Uma Thurman", "Harvey Keitel", "Bill Murray", "Frances McDormand"]
#act_man_f = "actors.list"
#act_woman_f = "actresses.list"
act_man_f = "t"
act_woman_f = "teste"
act_l = [(lambda n: Act(n[0], n[1]))([t.lower() for t in s.split()]) for s in act_n]
act_d = {}


def find_actor_line(l, f):
    if l and l[0] != '\t':
        for i, a in enumerate(act_l):
            if all(x(l.lower().replace(",","")) for x in a.regexp()) and not act_d.get(act_n[i], None):
                cs = [l[l.find('\t'):].replace("\t","").replace("\n","")]
                l = f.readline()
                while l and l[0] == '\t':
                    cs.append(l.replace("\t", "").replace("\n",""))
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
                cs = [l[l.find('\t'):].replace("\t","").replace("\n","")]
                l = f.readline()
                while l and l[0] == '\t':
                    cs.append(l.replace("\t", "").replace("\n",""))
                    l = f.readline()
                act_d[idx] = cs
        return l



with open(act_man_f, "r", encoding='latin-1') as m, open(act_woman_f, "r", encoding='latin-1') as w:
    c = 0
    lm = m.readline()
    lw = w.readline()
    while lm or lw:
        lm, lw = act_d_builder(lm, m), act_d_builder(lw, w)
        lm, lw = m.readline(),  w.readline()
        if c%50000 == 0:
            print(f"{c}º iteration...")
        c+=1

save_obj(act_d, "actors_actresses")

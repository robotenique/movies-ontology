import re
class Act(object):
    def __init__(self, f, l):
        self.f = f
        self.l = l
    def nlist(self):
        return [self.f, self.l]
    def __repr__(self):
        return f"f: {self.f} l: {self.l}"

## Finding Actors Information!
act_l = ["Uma Thurman", "Harvey Keitel", "Bill Murray", "Frances McDormand"]
act_man_f = "actors.list"
act_woman_f = "t"
act_l = [(lambda n: Act(n[0], n[1]))([t.lower() for t in s.split()]) for s in act_l]
act_d = {}


def find_actor_line(l, f):
    if l and l[0] != '\t':
        for i, a in enumerate(act_l):
            if all(x in l.lower().replace(",","") for x in (a.f, a.l)) and not act_d.get(i, None):
                act_d[i] = []
                cs = [l[l.find('\t'):].replace("\t","")]
                l = f.readline()
                while l and l[0] == '\t':
                    cs.append(l.replace("\t", ""))
                    l = f.readline()
                act_d[i].append("".join(cs))
    return l


with open(act_man_f, "r", encoding='latin-1') as m, open(act_woman_f, "r", encoding='latin-1') as w:
    c = 0
    lm = m.readline()
    lw = w.readline()
    while lm or lw:
        lm, lw = find_actor_line(lm, m), find_actor_line(lw, w)
        lm = m.readline(),  w.readline()
        if c%10000 == 0:
            print(f"Lendo {c+1}º linha...")
        c+=1

print(act_d)

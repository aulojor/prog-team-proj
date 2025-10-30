from collections import defaultdict
from datetime import datetime

def is_blank(l: str) -> bool:
    return len(l.strip(" ")) == 0


def parse():
    fp = open("dados.txt")
    data = [l for l in fp.read().split("\n")]
    chunks = boundaries(data)

    for c in chunks:
        parse_chunk(data[c[0]:c[1]])

    fp.close()


def boundaries(data: list[str]):
    boundaries = []
    s = None
    for (idx,l) in enumerate(data):
        if s is None:
            if not is_blank(l):
                s = idx
        else:
            if is_blank(l):
                boundaries.append((s,idx))
                s = None
    return boundaries


def parse_chunk(chunk_lines: list[str]):
    header = None
    for (idx, l) in enumerate(chunk_lines):
        if l[-1] == " ":
            header = idx-1
            break
    parse_header(chunk_lines[:header])


def parse_header(headers: list[str]):
    h = defaultdict(list)

    for line in headers:
        match line[-1]:
            case "1":
                h[1].append(line)
                break
            case "2":
                h[2].append(line)
                break
            case "3":
                h[3].append(line)
                break
            case "5":
                h[5].append(line)
                break
            case "6":
                h[6].append(line)
                break
            case "E":
                h["E"].append(line)
                break
            case "I":
                h["I"].append(line)
                break
            case _:
                raise NotImplemented
    for (k,v) in h.items():
        if len(v) != 0:
            FUNCS[k](v)


def parse_type_1(data: list[str]):
    aux = data[0]
    y = int(aux[1:5])
    mo = int(aux[6:8])
    d = int(aux[8:10])
    h = int(aux[11:13])
    m = int(aux[13:15])
    s = int(aux[16:18])
    mil = int(aux[19]) * 10**5
    dt = datetime(y,mo,d,h,m,s,mil)

    dist_ind = aux[21]
    eId = aux[22]
    lat = float(aux[23:30])
    long = float(aux[30:38])
    depth = float(aux[38:43])
    rep_ag = aux[45:48]

    hypo = {"dt": dt.isoformat(), "Distance Indicator": dist_ind, "Event ID": eId, "Lat": lat, "Long": long, "Depth": depth, "Agency": rep_ag, "magnitudes": list()}

    for (idx, l) in enumerate(data):
        hypo["magnitudes"] = hypo["magnitudes"] + parse_mag(l, idx)
    
    print(hypo)
    return hypo


def parse_mag(line: str, idx: int) -> list:
    magnitudes = []
    base = 55
    while base < 80:
        m = line[base:base+4]
        mt = line[base+4]
        if is_blank(m):
            break
        magnitudes.append({"M": m, "T": mt})
        base += 8
    return magnitudes

    
def parse_type_2(data: list[str]):
    pass

def parse_type_3(data: list[str]):
    pass

def parse_type_5(data: list[str]):
    pass

def parse_type_6(data: list[str]):
    pass

def parse_type_e(data: list[str]):
    pass

def parse_type_f(data: list[str]):
    pass

FUNCS = {1: parse_type_1, 2: parse_type_2, 3: parse_type_3, 5: parse_type_5, 6: parse_type_6, "E": parse_type_e, "F": parse_type_f}
parse()

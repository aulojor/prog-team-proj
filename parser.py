from collections import defaultdict
from datetime import datetime, time
import warnings

def is_blank(l: str) -> bool:
    return len(l.strip(" ")) == 0

def parse_flt(v:str) -> float | None:
    try:
        t = float(v)
        return t
    except ValueError:
        return None

def parse_int(v:str) -> int | None:
    try:
        t = int(v)
        return t
    except ValueError:
        return None


def parse():
    fp = open("dados.txt")
    data = [l for l in fp.read().split("\n")]
    chunks = boundaries(data)

    for c in chunks:
        yield parse_chunk(data[c[0]:c[1]])

    fp.close()


def boundaries(data: list[str]):
    boundaries = []
    start = None
    for (idx,l) in enumerate(data):
        if start is None:
            if not is_blank(l):
                start = idx
        else:
            if is_blank(l):
                boundaries.append((start,idx))
                start = None
    return boundaries


def parse_chunk(chunk_lines: list[str]):
    hIdx = None
    for (idx, l) in enumerate(chunk_lines):
        if l[-1] == "7":
            hIdx = idx
            break
    if hIdx is None:
        raise ValueError("Expected a '7' phase header in chunk_lines")
    else:
        headersRet = parse_header(chunk_lines[:hIdx])
        phaseRet = parse_type_7(chunk_lines[hIdx+1:])
    eventData = headersRet | phaseRet

    return eventData
    

def parse_header(hLines: list[str]):
    aux = defaultdict(list)

    for line in hLines:
        match line[-1]:
            case "1":
                aux[1].append(line)
            case "3":
                aux[3].append(line)
            case "6":
                aux[6].append(line)
            case "E":
                aux["E"].append(line)
            case "I":
                aux["I"].append(line)
            case "F":
                aux["F"].append(line)
            case unknown:
                warnings.warn(f"header type not implemented: {unknown}")

    headerDict = dict()
    for (k,v) in aux.items():
        if len(v) != 0:
            headerDict.update(FUNCS[k](v))
    return headerDict


def parse_mag(line: str):
    magnitudes = []
    base = 55
    while base < 79:
        m = line[base:base+4]
        mt = line[base+4]
        if not is_blank(m):
            magnitudes.append({"M": m, "T": mt})
        base += 8
    return magnitudes


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

    hypo = {"DateTime": dt.isoformat(), "Distance Indicator": dist_ind, "Event ID": eId, "Lat": lat, "Long": long, "Depth": depth, "Agency": rep_ag, "Magnitudes": list()}

    for l in data:
        hypo["Magnitudes"] = hypo["Magnitudes"] + parse_mag(l)

    return hypo

def parse_type_3(data: list[str]):
    comments = []
    for line in data:
        comments.append(line[:-2].strip())
    return {"Comments": comments}


def parse_type_6(data: list[str]):
    waves = []
    for l in data:
        waves.append(l.strip().split(" ")[0])
    return {"Wave": waves}


def parse_type_7(data: list[str]):
    phases = []
    # nordic format
    for l in data:
        h = int(l[18:20])
        m = int(l[20:22])
        sec = int(l[23:25])
        mil = int(l[26:28]) * 10**4
        t = time(h,m,sec,mil)
        phases.append({"Stat:":l[1:5], "Com": l[6:10], "I": l[9].strip(), "Phase": l[10:15].strip(), "Polarity": l[16].strip(), "Time": t.isoformat(), "Duration": parse_flt(l[29:33]), "Amplitude": parse_flt(l[34:40]), "Period": parse_flt(l[41:45]), "Azimuth": parse_flt(l[46:51]), "Velocity":parse_int(l[52:56]), "AIN": parse_int(l[57:60]), "AR": l[61:63], "Travel Time": parse_flt(l[63:67]), "Weigth": parse_int(l[67:70]), "Distance": float(l[71:75]), "CAZ": int(l[76:79])})

    return {"Phases": phases}

def parse_type_e(data: list[str]):
    aux = data[0]
    error = {"Gap": int(aux[5:8]), "Origin": float(aux[14:20]), "Error_lat": float(aux[24:30]), "Error_long": float(aux[32:38]), "Error_depth": float(aux[38:43]), "Cov_xy": float(aux[43:55]), "Cov_xz": float(aux[55:67]), "Cov_yz": float(aux[67:79])}
    return error


def parse_type_f(data: list[str]):
    return {}


def parse_type_i(data: list[str]):
    aux = data[0]
    dt = datetime.strptime(aux[12:26], "%y-%m-%d %H:%M")
    return {"Action": aux[8:11], "Action Extra": {"Date": dt.isoformat(), "OP": aux[30:35].strip(), "Status": aux[42:57].strip(), "ID":int(aux[60:74])}}


FUNCS = {1: parse_type_1, 3: parse_type_3, 6: parse_type_6, "E": parse_type_e, "F": parse_type_f, "I": parse_type_i}


print(next(parse()))

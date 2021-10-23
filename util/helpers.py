from datetime import datetime

def split_list(a, n):
    b = []
    for i in range(0, len(a)+1, n):
        b.append(a[i:i+n])
    return b


def difference(d1, d2 = datetime.now()):
    d1 = datetime.strptime(d1, '%m/%d/%y')
    #d2 = datetime.strptime(d2, '%m/%w/%y')
    return round(abs((d1 - d2).days) / 365)


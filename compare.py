import re
from Levenshtein import distance as levenshtein_distance
from dateutil.parser import parse
import util

def totalPrice(p1, p2):
    if not p1 or not p2:
        return False
    try:
        p1 = float(p1)
        p2 = float(p2)
        return p1 == p2
    except:
        return False

def currency(c1, c2):
    if not c1 or not c2:
        return False
    return c1 == c2

def date(d1, d2, raw):
    if not d1 or not d2:
        return False
    if d1 == d2:
        return True
   
    for b1 in [True, False]:
        for b2 in [True, False]:
            try:
                date1 = parse(d1,yearfirst=b1, dayfirst=b1)
                date2 = parse(d2,yearfirst=b2, dayfirst=b2)
                if date1 == date2:
                    return True
            except:
                continue
    d1 = re.sub(r'[-|.|\s|\\]', '', d1)
    d2 = re.sub(r'[-|.|\s|\\]', '', d2)
    return d1 == d2

def vendor(v1, v2):
    if not v1 or not v2:
        return False
    v1 = v1.lower()
    v2 = v2.lower()
    return levenshtein_distance(v1,v2) <= 3

def taxRate(r1, r2):
    if not r1 or not r2:
        return False
    r1 = re.sub(r'%', '', r1)
    r2 = re.sub(r'%', '', r2)
    r1 = re.sub(r',', '.', r1)
    r2 = re.sub(r',', '.', r2)
    try:
        r1 = float(r1)
        r2 = float(r2)
        return r1 == r2
    except:
        return False

def address(a1, a2):
    if not a1 or not a2:
        return False
    a1 = a1.lower()
    a2 = a2.lower()
    return levenshtein_distance(a1,a2) <= 3

def products(p1,p2):
    return p1 == p2
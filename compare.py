import re
from Levenshtein import distance as levenshtein_distance

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

def date(d1, d2):
    if not d1 or not d2:
        return False
    if d1 == d2:
        return True
    d1 = re.sub(r'[-|.|\s|\\]', '', d1)
    d2 = re.sub(r'[-|.|\s|\\]', '', d2)
    return d1 == d2

def vendor(v1, v2):
    if not v1 or not v2:
        return False
    #v1 = re.sub(r'[\s]', '', v1)
    #v2 = re.sub(r'[\s]', '', v2)
    v1 = v1.lower()
    v2 = v2.lower()
    if levenshtein_distance(v1,v2) > 3:
        #print(v1, '---', v2)
        x= 1

    return levenshtein_distance(v1,v2) <= 3

def taxRate(r1, r2):
    if not r1 or not r2:
        return False
    r1 = re.sub(r'%', '', r1)
    r2 = re.sub(r'%', '', r2)
    try:
        r1 = float(r1)
        r2 = float(r2)
        if r1 != r2:
            x = 1
            #print(r1, r2)
        return r1 == r2
    except:
        return False

def address(a1, a2):
    if not a1 or not a2:
        return False
    return levenshtein_distance(a1,a2) <= 3

def products(p1,p2):
    return p1 == p2
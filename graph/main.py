import json
from bpemb import BPEmb
#multibpemb = BPEmb(lang="multi", vs=1000000, dim=300)


def createGraph(json):
    #Create lines
    lines = []
    for element in json:
        print(element["bottomLeft"])
    return jsons

def feature_creation(word):
    return multibpemb.embed(word)

with open('test.txt') as json_file:
    data = json.load(json_file)
    createGraph(data)

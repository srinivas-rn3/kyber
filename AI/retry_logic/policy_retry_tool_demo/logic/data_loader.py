import json,os

def load_json(name):
    base = os.path.join(os.path.dirname(os.path.dirname(__file__)),"data",name)
    return json.load(open(base,'r'))
    
import json

def load(file = 'defaults.json'):
    obj = json.load(open(file, 'r'))
    obj.is_valid = verify(obj)
    return obj
    
def verify(obj):
    return True
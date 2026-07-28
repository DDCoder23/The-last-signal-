import json
def log(level,module,message):
    payload = json.dumps({
    "level": level,
    "module": module,
    "message": message
}).encode("utf-8")
    

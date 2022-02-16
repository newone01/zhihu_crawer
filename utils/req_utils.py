from flask import request

def get_params(key):
    if request.json:
        return request.json.get(key)
    return None
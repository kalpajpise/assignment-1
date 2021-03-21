import json
import requests

FLASK_ENDPOINTS = {
    "SEARCH": 'http://localhost:8000/api/query/search',
    "BANKLEAD": "http://localhost:8000/api/query/banklead",
    "STATS": "http://localhost:8000/api/query/stats"
}

DJANGO_ENDPOINTS = {
    "SEARCH": 'http://localhost:80/api/client/search',
    "BANKLEAD": "http://localhost:80/api/client/banklead",
    "STATS": "http://localhost:80/api/client/stats"
}


def redis_update_hit_count(dict_name, dict_key, r):
    r_data = r.get(dict_name)
    if not r_data:
        r.set(dict_name, json.dumps({
            dict_key : 1
        }))
    elif not dict_key in json.loads(r_data).keys():
        data = json.loads(r_data)
        data[dict_key] = 1
        r.set(dict_name, json.dumps(data))
    else :
        data = json.loads(r_data)
        data[dict_key] += 1
        r.set(dict_name, json.dumps(data))



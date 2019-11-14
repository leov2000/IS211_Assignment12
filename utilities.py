import json

def get_credentials():
    with open('app_keys.json') as credentials:
        keys = json.load(credentials)
    
    return keys 
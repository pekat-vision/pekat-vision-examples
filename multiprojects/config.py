import json

config = None

with open('config.json') as f:
    config = json.load(f)

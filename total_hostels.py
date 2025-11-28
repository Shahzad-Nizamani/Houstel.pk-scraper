import json

with open("hostels.json", 'r') as f:
    h = json.load(f)

length = len(h["hostels"])
print(length)
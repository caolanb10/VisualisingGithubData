import requests
import json

f = open("githubjson", "w")
r = requests.get('https://api.github.com/repos/caolanb10/Compilers')
if(r.ok):
    repoItem = json.loads(r.text or r.content)
    print(json.dumps(repoItem, sort_keys=True, indent = 3))

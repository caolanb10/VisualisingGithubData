import requests
import json
import sqlite3




def URLchopper(url):
    newurl = url.split('{')
    newurl = newurl[0]
    return newurl

r = requests.get('https://api.github.com/repos/caolanb10/Compilers')
if(r.ok):
    repoItem = json.loads(r.text or r.content)
    print(json.dumps(repoItem, indent=4))
    jsonstr = repoItem['owner']['following_url']
    print(URLchopper(jsonstr))

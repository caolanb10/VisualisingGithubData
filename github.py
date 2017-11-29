import requests
import json
import sqlite3

class user:
    id = 'NULL'
    name = 'NULL'
    location = 'NULL'
    repos = 'NULL'
    userSince = 'NULL'
    company = 'NULL'
    followers = 'NULL'
    following = 'NULL'
    trackedUser = 'NULL'
    insertStatement = 'NULL'

    def __init__(self, userJSON, tracked):
        self.id = userJSON['id']
        self.name = userJSON['name']
        self.location = userJSON['location']
        self.repos = userJSON['public_repos']
        self.userSince = userJSON['created_at']
        self.company = userJSON['company']
        self.followers = userJSON['followers']
        self.following = userJSON['following']
        self.trackedUser = tracked

    def URLchopper(self, url):
        newurl = url.split('{')
        newurl = newurl[0]
        return newurl

    def createInsertStatement(self):
        self.insertStatement = "INSERT INTO TABLE userTable VALUES(" + str(self.id) + ",'" + self.name + "','" + self.location + "',"+ str(self.repos) + ",'"+ self.userSince + "',"+ str(self.followers) + ","+ str(self.following) + "," + ")";
        return self.insertStatement                                              #+ str(self.trackedUser) + ");"

#conn = sqlite3.connect('githubDb.db')

#c = conn.cursor()

#c.execute("create table =(id int, string text)")

r = requests.get('https://api.github.com/users/WhelanB')
userJSON = json.loads(r.text or r.content)
#print(json.dumps(userJSON, indent=4))
firstUser = user(userJSON, 1)
print(str(firstUser.trackedUser))
print(firstUser.createInsertStatement())



#userFollowers = requests.get(userJSON['followers_url'])
#userFollowing = requests.get(URLchopper(userJSON['following_url']))
#followersJSON = json.loads(userFollowers.text or userFollowers.content)
#followingJSON = json.loads(userFollowing.text or userFollowing.content)
#print(json.dumps(followingJSON, indent = 4))
#print(json.dumps(followersJSON, indent = 4))
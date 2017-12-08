import requests
import json
import _random
import random
import sqlite3

def newURLchopper(url):
    newurl = url.split('{')
    newurl = newurl[0]
    return newurl

def followerInsertStatement(firstUser, follower):
    insertStatement = "INSERT INTO UserFollowing VALUES(" + str(firstUser.id) + "," + str(follower.id) + ")"
    return insertStatement

def followingInsertStatement(firstUser, follower):
    insertStatement = "INSERT INTO UserFollowers VALUES(" + str(firstUser.id) + "," + str(follower.id) + ")"
    return insertStatement

class user:
    login = 'NULL'
    id = 'NULL'
    name = 'NULL'
    location = 'NULL'
    repos = 'NULL'
    userSince = 'NULL'
    followers = 'NULL'
    following = 'NULL'
    trackedUser = 'NULL'
    insertStatement = 'NULL'

    def __init__(self, userJSON, tracked):
        self.login = userJSON['login']
        self.id = userJSON['id']
        self.name = userJSON['name']
        self.location = userJSON['location']
        self.repos = userJSON['public_repos']
        self.userSince = userJSON['created_at']
        self.followers = userJSON['followers']
        self.following = userJSON['following']
        self.trackedUser = tracked
        if self.name is None:
            self.name = self.login
        if self.location is None:
            self.location = "No location"
        self.insertStatement = self.createInsertStatement()
        print(self.name)
        print(self.id)

    def createInsertStatement(self):
        insertStatement = 'INSERT INTO User VALUES(' + str(self.id) + ',"' + \
                               self.name + '","' + \
                               self.location + '",'+ \
                               str(self.repos) + ',"'+ \
                               self.userSince + '",'+ \
                               str(self.followers) + ','+ \
                               str(self.following) + ',' + str(self.trackedUser) + ')'
        return insertStatement
auth = ('caolanb10', 'itzzCaolan10')
r = requests.get('https://api.github.com/users/WhelanB', auth=auth)
userJSON = json.loads(r.text or r.content)
print(json.dumps(userJSON, indent = 4))
firstUser = user(userJSON, 1)
conn = sqlite3.connect('githubDb.db', isolation_level=None)
c = conn.cursor()
c.execute("create table User(id int PRIMARY KEY, name text, location text, repos int, userSince text, followers int, following int, trackedUser int);")
c.execute("create table UserFollowing(userid int, followingid int, PRIMARY KEY(userid, followingid) , FOREIGN KEY (userid) REFERENCES User(id), FOREIGN KEY (followingid) REFERENCES User(id))")
c.execute("create table UserFollowers(userid int, followerid int, PRIMARY KEY(userid, followerid), FOREIGN KEY (userid) REFERENCES User(id), FOREIGN KEY (followerid) REFERENCES User(id))")
print(firstUser.insertStatement)
c.execute(firstUser.insertStatement)

counter = 0
idList = []

while(counter<100):
    userFollowing = requests.get(newURLchopper(userJSON['following_url']), auth=auth)
    userFollowers = requests.get(userJSON['followers_url'], auth=auth)
    followersJSON = json.loads(userFollowers.text or userFollowers.content)
    followingJSON = json.loads(userFollowing.text or userFollowing.text)
    for x in range(0, len(followersJSON)):
        followers = []
        afollower = requests.get(followersJSON[x]['url'], auth=auth)
        afollower1 = json.loads(afollower.text or afollower.content)
        followedUser = user(afollower1, 0)
        counter+=1
        followers.append(followedUser)
        idList.append(followedUser.id)
        for xx in range(0, len(followers)):
            userInput = followers[xx]
            c.execute(userInput.insertStatement)
            c.execute(followerInsertStatement(firstUser, followers[xx]))
    print("------------done------------")
    print(json.dumps(followingJSON, indent=4))
    for y in range(0, len(followingJSON)):
        following = []
        afollowing = requests.get(followingJSON[y]['url'], auth =auth)
        afollowing1=json.loads(afollowing.text or afollowing.content)
        followingUser = user(afollowing1, 0)
        counter+=1
        following.append(followingUser)
        if followingUser.id not in idList:
            idList.append(followingUser.id)
        for yy in range(0, len(following)):
            userInput = following[yy]
            c.execute(userInput.insertStatement)
            c.execute(followingInsertStatement(firstUser, following[yy]))
    nextUser = requests.get(followingJSON[random.randrange(len(followingJSON))]['url'], auth=auth)
    userJSON = json.loads(nextUser.text or nextUser.content)
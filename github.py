import requests
import json
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
        self.insertStatement = self.createInsertStatement()

    def createInsertStatement(self):
        insertStatement = 'INSERT INTO User VALUES(' + str(self.id) + ',"' + \
                               self.name + '","' + \
                               self.location + '",'+ \
                               str(self.repos) + ',"'+ \
                               self.userSince + '",'+ \
                               str(self.followers) + ','+ \
                               str(self.following) + ',' + str(self.trackedUser) + ')'
        return insertStatement
request = requests.get('https://api.github.com/user', auth=('user', 'pass'))
print(request.content or request.text)
r = requests.get('https://api.github.com/users/WhelanB')
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
while(counter<100):
    userFollowers = requests.get(userJSON['followers_url'])
    followersJSON = json.loads(userFollowers.text or userFollowers.content)
    print(json.dumps(followersJSON, indent = 4))
    userFollowing = requests.get(newURLchopper(userJSON['following_url']))
    followingJSON = json.loads(userFollowing.text or userFollowing.text)
    for x in range(0, len(followersJSON)):
        followers = []
        afollower = requests.get(followersJSON[x]['url'])
        afollower1 = json.loads(afollower.text or afollower.content)
        followedUser = user(json.loads(afollower.text or afollower.content), 0)
        counter+=1
        followers.append(afollower1)
        for xx in range(0, len(followers)):
            c.execute(followers[xx].insertStatement)
            c.execute(followerInsertStatement(firstUser, followers[xx]))
    for x in range(0, len(followers)):
        print(followers[x].insertStatement)
    for y in range(0, len(followingJSON)):
        following = []
        afollowing = requests.get(followingJSON[y]['url'])
        followingUser = user(json.loads(afollowing.text or afollowing.content), 0)
        counter+=1
        following.append(followingUser)
        for yy in range(0, len(following)):
            c.execute(following[yy].insertStatement)
            c.execute(followingInsertStatement(firstUser, following[yy]))
    userJSON = requests.get(followingJSON[0]['url'])
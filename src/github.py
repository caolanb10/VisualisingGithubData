import requests
import json
import random
import sqlite3
# function for taking parentheses from end of URL
def newURLchopper(url):
    newurl = url.split('{')
    newurl = newurl[0]
    return newurl
# function generates insert statement for userFollower table
def followerInsertStatement(firstUser, follower):
    insertStatement = "INSERT INTO UserFollowing VALUES(" + str(firstUser.id) + "," + str(follower.id) + ")"
    return insertStatement
# function generates insert statement for userFollowing table
def followingInsertStatement(firstUser, follower):
    insertStatement = "INSERT INTO UserFollowers VALUES(" + str(firstUser.id) + "," + str(follower.id) + ")"
    return insertStatement

# class for storing user info from parsing JSON
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

#authorisation with auth token
auth = ("caolanb10" ,"itzzCaolan10")
r = requests.get('https://api.github.com/users/WhelanB', auth=auth)     #an account with followers and is following people
userJSON = json.loads(r.text or r.content)
firstUser = user(userJSON, 1)
conn = sqlite3.connect('githubDb.db', isolation_level=None)
c = conn.cursor()
c.execute("create table User(id int PRIMARY KEY, "      #creating tables in database
          "name text, location text, repos int, "
          "userSince text, followers int, "
          "following int, trackedUser int);")
c.execute("create table UserFollowing(userid int, followingid int, "
          "PRIMARY KEY(userid, followingid) , FOREIGN KEY (userid) REFERENCES User(id), "
          "FOREIGN KEY (followingid) REFERENCES User(id))")
c.execute("create table UserFollowers(userid int, followerid int, PRIMARY KEY(userid, followerid), "
          "FOREIGN KEY (userid) REFERENCES User(id), "
          "FOREIGN KEY (followerid) REFERENCES User(id))")

c.execute(firstUser.insertStatement)
#Github crawl loop

counter = 0
idList = []
idList.append(firstUser.id)
while(counter<50):
    userFollowing = requests.get(newURLchopper(userJSON['following_url']), auth=auth)
    userFollowers = requests.get(userJSON['followers_url'], auth=auth)
    followersJSON = json.loads(userFollowers.text or userFollowers.content)                     #creates list of followeres
    followingJSON = json.loads(userFollowing.text or userFollowing.text)                        #creates list of following
    for x in range(0, 6 if len(followersJSON)> 6 else len(followersJSON)):                                                      #loops through each follower and generates statement for tables
        afollower = requests.get(followersJSON[x]['url'], auth=auth)
        afollower1 = json.loads(afollower.text or afollower.content)                            #loads user and checks if user has been passed before
        userId = afollower1['id']
        if userId not in idList:
            idList.append(userId)
            followedUser = user(afollower1, 0)
            counter+=1                                                                          #If they havent they are entered into the database
            c.execute(followedUser.insertStatement)
            c.execute(followerInsertStatement(firstUser, followedUser))

    for y in range(0, 6 if len(followingJSON)>6 else len(followingJSON)):                                                      #loops through each user their following                                                                        #and generates statement for tables
        afollowing = requests.get(followingJSON[y]['url'], auth =auth)
        afollowing1=json.loads(afollowing.text or afollowing.content)
        userId = afollowing1['id']
        if userId not in idList:
            idList.append(userId)
            followingUser = user(afollowing1, 0)
            counter+=1                                                                          #loads user and checks if user has been passed before
            idList.append(followingUser.id)                                                #If they havent they are entered into the database
            c.execute(followingUser.insertStatement)
            c.execute(followingInsertStatement(followingUser, firstUser))

    nextUser = requests.get(followersJSON[random.randrange(10 if len(followersJSON) > 10 else len(followersJSON))]['url'], auth=auth)
    userJSON = json.loads(nextUser.text or nextUser.content)
    firstUser = user(userJSON, 0)           # 0 here indicates this is not the very first user just the next one were crawling to
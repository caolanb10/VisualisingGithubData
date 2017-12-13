import matplotlib.pyplot as plot
import sqlite3
import networkx as nx

G = nx.DiGraph()                                                #new directed graph
conn = sqlite3.connect('githubDb.db', isolation_level=None)
c=conn.cursor()
c.execute("SELECT name FROM user WHERE trackeduser = 1;")
name = c.fetchone()[0]                                         #get name of the first tracked user
c.execute("SELECT name, followers FROM user INNER JOIN userfollowing on user.id = userfollowing.userid;")
l = [row[0] for row in c.fetchall()]
c.execute("SELECT name, followers FROM user INNER JOIN userfollowing on user.id = userfollowing.followingid;")
s = [row[0] for row in c.fetchall()]
ls = list(zip(l,s))                                             #zip together the tuples from the userfollowing table
G.add_edges_from(ls)
c.execute("SELECT name, followers FROM user INNER JOIN userfollowers on user.id = userfollowers.userid;")
l = [row[0] for row in c.fetchall()]
c.execute("SELECT name, followers FROM user INNER JOIN userfollowers on user.id = userfollowers.followerid;")
s = [row[0] for row in c.fetchall()]
ls = list(zip(l,s))                                             #zip together the tuples from the userfollowers table
G.add_edges_from(ls)
color_list = []
color_list.append('g')

var = (list(G.nodes.items()))
var2 = ([x[0] for x in var])

followersList = []
for y in range(0, len(var2)):
    user = var2[y]
    c.execute('SELECT followers FROM user WHERE name = '+'"'+ user+'"' + ';')
    followers = c.fetchone()[0]
    followersList.append(500 if followers>500 else followers)

for x in G.edges:
    color_list.append('r')          #colour all nodes except for the base node red, base node is blue.

pos = nx.random_layout(G)
nx.draw_networkx_nodes(G, pos, node_color=color_list, node_size=followersList)
nx.draw_networkx_labels(G, pos, font_color='k', font_size='10')
nx.draw_networkx_edges(G, pos, line_width=0.5, alpha=0.5)
plot.show()

## Introduction
This project is about retrieving data from Github's API, processing and storing it and creating a visualisation of this data.
The data that I hope to create visualisations of is the data of a user's followers and who the user is following. I hope to make some type of directed graph
visualisaiton with vertices that will have differing radii depending on the amount of followers that user has. I then hope to access the followers and those following the user's who the initial user has as followers and who they are following. I aim to do this to 3 degree's of seperation.

## Technology Used
For this project I am using the python programming language in conjunction with SQLite for the database management system. I am using NetworkX as well as matplotlib for the visualisations

## Steps Involved
I have subdivided this project into two distinct steps which will be represented as two distinct scripts. The first one will access github's API and extract the necessary user data and the user data of that user's followers and those they are following. Then this data will be processed and then inserted into a relational database.
For the second half of the assignment I used networkx and matplotlib to create the graph of the connected users on github.

## Progress
I have managed to complete my web crawl on the user data, I have altered my implication by limiting the number of followers or users that the user is following to 10
as my crawl allowed for one users data to fully complete the crawl which didnt very much crawl very far.

My crawl now allows for 6 followers and 6 users theyre following to be added to the graph, i did this to get greater disparity from the visualisation.
I decided against using d3.js as none of the templates really satisfied my idea of a directed graph.
I decided to use matplotlib and networkX for the graphs instead.
The crawl collects ~100 users and each user where follower information was collected has degree 12 (6 in degree, 6 out degree)

## Customising the graph size
The counter in the github script counts how many users we are putting on our graph, by customising this number we can define how many users we want our graph to span.

## Libraries Used
NetworkX
SQLite3
Requests
JSON
Random
Matplotlib
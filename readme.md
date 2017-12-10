
## Introduction
This project is about retrieving data from Github's API, processing and storing it and creating a visualisation of this data.
The data that I hope to create visualisations of is the data of a user's followers and who the user is following. I hope to make some type of directed graph
visualisaiton with vertices that will have differing radii depending on the amount of followers that user has. I then hope to access the followers and those following the user's who the initial user has as followers and who they are following. I aim to do this to 3 degree's of seperation.

## Technology Used
For this project I am using the python programming language in conjunction with SQLite for the database management system. I will be using d3.js libraries for the data visualisations

## Steps Involved
I have subdivided this project into two distinct steps which will be represented as two distinct scripts. The first one will access github's API and extract the necessary user data and the user data of that user's followers and those they are following. Then this data will be processed and then inserted into a relational database.
The second step is creating a webserver that interacts with this database and creates visualisations from the data stored in the database, the language used for the scripts used on the webpage will be javascript.

## Progress
I have managed to complete my web crawl on the user data, I have altered my implication by limiting the number of followers or users that the user is following to 10
as my crawl allowed for one users data to fully complete the crawl which didnt very much crawl very far.

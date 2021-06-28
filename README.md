# MuseumsAssignment

This repository was originally created as an assignment for an interview process. I make this repo public as a showcase for other interviews. 

The theme of this repo is museums. The goal is to make a linear regression model to predict the attendance of major museums based on their city's population. This project extracts the list of most visited museums in the world (2M+ yearly attendance) from Wikipedia, extracts data about the population of their respective cities from Wikidata and creates a custom linear regression model to predict the attendance.

The project is separated in three executable sections:
1) Extracting the list of museums and storing that in a database. Extracting population data from cities and storing that in a database.
2) Train a custom linear regression
3) Collect additional information about museums from Wikidata

The code was deliberately split into three sections to simulate that these processes can happen at different moments in the life of the software.
Thus, they all interact with a local sqlite DB to persist information between runs.
For instance, the table that contains museums is used many times and additional data is added to it. 
This sqlite DB contains two tables: Cities and Museums

## How to run

To run this repo, you can use Main.py, which will call the respective mains of the subsections needed to complete the task. You can refer to the requirements.txt file for the necessary packages.

A Dockerfile has also been created to deploy the whole project easily. Thus, one only needs to build the dockerfile and run the image to see the project in action.

## Notable features

I coded an entire Linear Regression Model from scratch to showcase my ability to understand custom ML models and reproduce them.

In order to interface the code with an SQL database, I extended the pandas DataFrame class.
This means that the pandas DataFrame can be used as if it was a normal DataFrame with all its convenient features.
In addition, it can be created from an SQL query to a DB and save to that DB as well.

I made sure that my data was up to date by looking for the most recent population data available for each city from Wikidata.
Also, I made sure that even though some museums did not exist in English Wikipedia, I could still get the relevant data from them by looking at data from elsewhere in Wikipedia and Wikidata.

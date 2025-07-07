# Script to fetch and store cat facts

import requests
import sqlite3
import re
from db import connectToDB, createDB, limitFiveFacts, fetchDB, insertDB

con = connectToDB() #Connect to cat_facts database
createDB(con) #Create cat_facts dabatase

def getCatFactsFromSite(): #Connect to catfact website 
    response = requests.get('https://catfact.ninja/fact')
    
    if response.status_code == 200: #Connection Succesful
        data = response.json()
        return data
    else: #Connection Unsuccessful
        print("Failed to get data. Status Code: {r.status_code}")


def saveFactsToDB(): #Saving facts from catfact website to the cat_fact database
    inserts = 0
    duplicates = 0

    while inserts < 5: #Only insert 5 facts into the database
        catFact = getCatFactsFromSite()
        if catFact:
            cur = insertDB(con, catFact["fact"]) #Extracting and inserting the facts

            if cur.rowcount == 1: #Checking for fact duplicates
                inserts += 1
            else:
                print("Skipped Duplicate.") 

    limitFiveFacts(con) #Keep only the lastest 5 facts in the cat_fact database
    
    #Fetching and printing all facts in the cat_fact database
    cur = fetchDB(con)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    

saveFactsToDB()





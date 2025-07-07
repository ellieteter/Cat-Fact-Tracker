# FastAPI backend

import import_cat_facts
from db import fetchDB, fetchDB_random, insertDB
from fastapi.middleware.cors import CORSMiddleware

from typing import Union
from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(  #CORS support to allow requests from your frontend
    CORSMiddleware,
    allow_origins="http://localhost:3000",  # You can limit this to http://localhost:3000 if preferred
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_DB_connetion(): #Connect to cat_facts database
    con = sqlite3.connect('cat_facts.db')
    con.row_factory = sqlite3.Row
    return con

@app.get("/catfacts") #Returns all cat facts in the database
def getCatFacts():
    con = get_DB_connetion()
    cursor = fetchDB(con).fetchall()
    con.close()
    return cursor


@app.get("/catfacts/random") #Returns a random cat fact
def getRandomCatFacts():
    con = get_DB_connetion()
    cursor = fetchDB_random(con).fetchone()
    con.close()
    return cursor
    
class CatFact(BaseModel):
    fact: str

@app.post("/catfacts") #Accepts a new cat fact and inserts it in cat_facts database
def postCatFacts(cat_fact:CatFact):
    con = get_DB_connetion()
    cur = insertDB(con, (cat_fact.fact))
    con.commit()
    if cur.rowcount == 0: #Checks for duplicate cat facts
        message = "Skipped Duplicate."
    else:
        message = "Cat fact added!"
    con.close()
    return {"message": message}
    
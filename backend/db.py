# DB logic (create, insert, fetch)

import sqlite3 

def connectToDB(): #Function to connect to the SQLite3 cat_facts database
    return sqlite3.connect('cat_facts.db')


def createDB(con): #Function to create the cat_facts database
    con.execute('''CREATE TABLE IF NOT EXISTS cat_facts (id INTEGER PRIMARY KEY AUTOINCREMENT,fact TEXT UNIQUE, created_at DATE DEFAULT (DATE('now')));''')
    con.commit()

def insertDB(con, fact): #Function to insert facts into the cat_facts database
    cursor = con.execute("INSERT OR IGNORE INTO cat_facts (fact) VALUES (?)", (fact,)) #Insert facts as single element tuples
    con.commit()
    return cursor

def fetchDB(con): #Function to fetch facts from the cat_facts database
    cursor = con.execute("SELECT id, fact, created_at FROM cat_facts")
    return cursor

def fetchDB_random(con):
    cursor = con.execute('SELECT fact FROM cat_facts ORDER BY RANDOM()')
    return cursor

def limitFiveFacts(con): #Function to have only 5 cat facts in the database
    con.execute("""DELETE FROM cat_facts WHERE id NOT IN (SELECT id FROM cat_facts ORDER BY id DESC LIMIT 5)""")
    con.commit()

import sqlite3

DB_NAME = "odds.db"

# create the database
def init_db():
    con = sqlite3.connect("odds.db")
    cur = con.cursor()
    
    # create the table
    cur.execute(
        """ CREATE TABLE IF NOT EXISTS odds_histroy (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id TEXT,
            bookmaker TEXT,
            team TEXT,
            price REAL,
            prob, REAL
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)"""
    )
     
    con.commit()
    con.close()

# add odds to data base
def save_odds(game_id, bookmaker, team, price, prob):
    con = sqlite3.connect("odds.db")
    cur = con.cursor()
    
    cur.execute(
        """ INSERT INTO odds_history VALUES(?,?,?,?,?)""", (game_id, bookmaker, team, price, prob)
    )
    
    con.commit()
    con.close()

init_db()
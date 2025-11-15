import sqlite3

def test():
    
    con = sqlite3.connect("odds.db")
    cur = con.cursor()
    
    sql = "SELECT * FROM odds_history"
    
    cur.execute(sql)
    
    print(cur.fetchall)
    
test()
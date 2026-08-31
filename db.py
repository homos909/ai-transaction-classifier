import sqlite3

def tao_bang(ten_db):
    conn = sqlite3.connect(ten_db)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            account TEXT
        )
    ''')
    conn.commit()
    conn.close()

def luu_giao_dich(ten_db, date, description, amount, account):
    conn = sqlite3.connect(ten_db)
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO transactions (date, description, amount, account)
        VALUES (?, ?, ?, ?)
    ''', (date, description, amount, account))
    conn.commit()
    conn.close()

def xoa_du_lieu_cu(ten_db):
    conn = sqlite3.connect(ten_db)
    cur = conn.cursor()
    cur.execute("DELETE FROM transactions")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    tao_bang("classifier.db")
    luu_giao_dich("classifier.db", "2026-09-01", "Thu tiền bán hàng", 15000000, "Doanh thu")

    conn = sqlite3.connect("classifier.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions")
    print(cur.fetchall())
    conn.close()
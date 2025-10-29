import sqlite3, time, os
DB = os.path.join(os.getcwd(), 'review_queue.db')

def _conn():
    c = sqlite3.connect(DB, check_same_thread=False)
    return c

def init_db():
    c = _conn()
    c.execute("""CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prompt TEXT,
        label TEXT,
        score REAL,
        status TEXT,
        metadata TEXT,
        created_at REAL
    )""")
    c.commit()

def enqueue(prompt: str, label: str, score: float, metadata: str = ""):
    c = _conn()
    c.execute("INSERT INTO reviews (prompt, label, score, status, metadata, created_at) VALUES (?,?,?,?,?,?)", 
              (prompt, label, score, "PENDING", metadata, time.time()))
    c.commit()
    return c.execute("SELECT last_insert_rowid()").fetchone()[0]

def list_pending(limit=50):
    c = _conn()
    rows = c.execute("SELECT id, prompt, label, score, metadata, created_at FROM reviews WHERE status='PENDING' ORDER BY created_at ASC LIMIT ?", (limit,)).fetchall()
    return rows

def update_status(review_id:int, status:str, resolution:str=""):
    c = _conn()
    c.execute("UPDATE reviews SET status=?, metadata=metadata||? WHERE id=?", (status, f" | resolution:{resolution}", review_id))
    c.commit()

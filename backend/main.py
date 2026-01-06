from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from datetime import datetime

app = FastAPI()

DB_PATH = "health.db"

def init_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,
        name TEXT NOT NULL,
        total_score REAL NOT NULL,
        smoking REAL NOT NULL,
        steps REAL NOT NULL,
        ldl REAL NOT NULL,
        bp REAL NOT NULL,
        bmi REAL NOT NULL,
        day TEXT NOT NULL
    )
    """)
    con.commit()
    con.close()

init_db()

class ScoreIn(BaseModel):
    name: str
    totalScore: float
    smoking: float
    steps: float
    ldl: float
    bp: float
    bmi: float

@app.post("/score")
def save_score(body: ScoreIn):
    now = datetime.now()
    day_str = now.date().isoformat()

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        INSERT INTO scores (ts, name, total_score, smoking, steps, ldl, bp, bmi, day)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        now.isoformat(timespec="seconds"),
        body.name,
        body.totalScore,
        body.smoking,
        body.steps,
        body.ldl,
        body.bp,
        body.bmi,
        day_str
    ))
    con.commit()
    con.close()

    return {"status": "ok"}

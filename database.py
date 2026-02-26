import sqlite3

DB_NAME = "analysis.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            job_id TEXT PRIMARY KEY,
            filename TEXT,
            status TEXT,
            result TEXT
        )
    """)

    conn.commit()
    conn.close()


def create_job(job_id, filename):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO analyses (job_id, filename, status, result) VALUES (?, ?, ?, ?)",
        (job_id, filename, "processing", "")
    )

    conn.commit()
    conn.close()


def update_job(job_id, result):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE analyses SET status=?, result=? WHERE job_id=?",
        ("completed", result, job_id)
    )

    conn.commit()
    conn.close()


def get_job(job_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT job_id, filename, status, result FROM analyses WHERE job_id=?", (job_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "job_id": row[0],
        "filename": row[1],
        "status": row[2],
        "result": row[3]
    }
import csv
import datetime
import sqlite3
from .nlp_processor import get_keywords


def get_db_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def create_knowledge_table(db_path):
    conn = get_db_connection(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            keywords TEXT,
            answer TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def create_pending_knowledge_table(db_path):
    conn = get_db_connection(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS pending_knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            keywords TEXT,
            answer TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def load_csv_file(csv_path, db_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = []
        for row in reader:
            category = row.get('category', '').strip()
            keywords = row.get('keywords', '').strip()
            answer = row.get('answer', '').strip()
            if category and keywords and answer:
                rows.append((category, keywords, answer))

    if rows:
        conn = get_db_connection(db_path)
        conn.executemany(
            'INSERT INTO knowledge (category, keywords, answer) VALUES (?, ?, ?)',
            rows
        )
        conn.commit()
        conn.close()


def save_pending_knowledge(question, answer, db_path):
    answer_text = answer.strip()
    if len(answer_text) < 4:
        return False

    keywords = get_keywords(question)
    if not keywords:
        return False

    keyword_string = ','.join(keywords)
    conn = get_db_connection(db_path)
    
    existing_pending = conn.execute(
        'SELECT 1 FROM pending_knowledge WHERE question = ? AND answer = ? AND status = ?',
        (question.strip(), answer_text, 'pending')
    ).fetchone()
    if existing_pending:
        conn.close()
        return False

    existing_known = conn.execute(
        'SELECT 1 FROM knowledge WHERE keywords = ? AND answer = ?',
        (keyword_string, answer_text)
    ).fetchone()
    if existing_known:
        conn.close()
        return False

    created_at = datetime.datetime.utcnow().isoformat()
    conn.execute(
        'INSERT INTO pending_knowledge (question, keywords, answer, status, created_at) VALUES (?, ?, ?, ?, ?)',
        (question.strip(), keyword_string, answer_text, 'pending', created_at)
    )
    conn.commit()
    conn.close()
    return True


def save_knowledge(question, answer, db_path):
    answer_text = answer.strip()
    if len(answer_text) < 4:
        return False

    keywords = get_keywords(question)
    if not keywords:
        return False

    keyword_string = ','.join(keywords)
    conn = get_db_connection(db_path)
    
    existing = conn.execute(
        'SELECT 1 FROM knowledge WHERE keywords = ? AND answer = ?',
        (keyword_string, answer_text)
    ).fetchone()
    if existing:
        conn.close()
        return False

    conn.execute(
        'INSERT INTO knowledge (category, keywords, answer) VALUES (?, ?, ?)',
        ('learned', keyword_string, answer_text)
    )
    conn.commit()
    conn.close()
    return True

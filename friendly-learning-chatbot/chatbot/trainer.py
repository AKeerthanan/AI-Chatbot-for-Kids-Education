import sqlite3
from .nlp_processor import get_keywords


def get_db_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def save_knowledge(question, answer, db_path):
    answer_text = answer.strip()
    if not answer_text:
        return False

    blocked_answers = {'skip', 'cancel', 'never mind', 'nevermind'}
    if answer_text.lower() in blocked_answers:
        return False

    keywords = get_keywords(question)
    if not keywords:
        return False

    keyword_string = ','.join(keywords)
    conn = get_db_connection(db_path)
    conn.execute(
        'INSERT INTO knowledge (category, keywords, answer) VALUES (?, ?, ?)',
        ('learned', keyword_string, answer_text)
    )
    conn.commit()
    conn.close()
    return True

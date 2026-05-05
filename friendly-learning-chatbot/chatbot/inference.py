import sqlite3
from .nlp_processor import get_keywords

UNKNOWN_PROMPT = 'I don’t know that yet. If you want to teach me, type: teach: your answer. Or type skip.'


def get_db_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def find_best_answer(user_input, db_path):
    user_keywords = get_keywords(user_input)
    if not user_keywords:
        return UNKNOWN_PROMPT

    conn = get_db_connection(db_path)
    rows = conn.execute('SELECT keywords, answer FROM knowledge').fetchall()
    conn.close()

    best_match = None
    best_score = 0
    keyword_set = set(user_keywords)

    for row in rows:
        stored_keywords = {keyword.strip() for keyword in row['keywords'].split(',') if keyword.strip()}
        match_score = len(keyword_set & stored_keywords)
        if match_score > best_score:
            best_score = match_score
            best_match = row['answer']

    if best_match and best_score > 0:
        return best_match
    return UNKNOWN_PROMPT

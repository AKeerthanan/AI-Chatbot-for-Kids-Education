import csv
import glob
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_PATH = os.path.join(os.path.dirname(BASE_DIR), 'database', 'chatbot.db')
DEFAULT_DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), 'dataset')


def get_db_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def create_knowledge_table(db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = get_db_connection(db_path)
    conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            keywords TEXT,
            answer TEXT
        )
        '''
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


def build_database(db_path=None, data_dir=None):
    if db_path is None:
        db_path = DEFAULT_DB_PATH
    if data_dir is None:
        data_dir = DEFAULT_DATA_DIR

    create_knowledge_table(db_path)

    if not os.path.isdir(data_dir):
        raise FileNotFoundError(f'Dataset directory not found: {data_dir}')

    csv_files = sorted(glob.glob(os.path.join(data_dir, '*.csv')))
    if not csv_files:
        raise FileNotFoundError('No CSV dataset files found in dataset directory.')

    for csv_file in csv_files:
        print(f'Loading {os.path.basename(csv_file)}...')
        load_csv_file(csv_file, db_path)

    print('Training complete. Data inserted into', db_path)


def reset_database(db_path=None, data_dir=None):
    if db_path is None:
        db_path = DEFAULT_DB_PATH
    if data_dir is None:
        data_dir = DEFAULT_DATA_DIR

    if os.path.exists(db_path):
        os.remove(db_path)
    build_database(db_path, data_dir)


def save_knowledge(question, answer, db_path):
    answer_text = answer.strip()
    if not answer_text:
        return False

    blocked_answers = {'skip', 'cancel', 'never mind', 'nevermind'}
    if answer_text.lower() in blocked_answers:
        return False

    from .nlp_processor import get_keywords

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

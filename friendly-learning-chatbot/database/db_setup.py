import os
import sqlite3


def get_db_connection(db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path):
    first_time = not os.path.exists(db_path)
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

    if first_time:
        sample_data = [
            ('math', 'addition,add,plus,sum,total', 'Addition means putting numbers together to find the total.'),
            ('math', 'subtraction,subtract,minus,less,difference', 'Subtraction means taking one number away from another.'),
            ('english', 'noun,nouns,person,place,thing,idea', 'A noun is a word for a person, place, thing, or idea.'),
            ('english', 'verb,verbs,action,doing', 'A verb is a word that shows action or being.'),
            ('science', 'water,boil,boils,celsius,heat', 'Water boils at 100 degrees Celsius at normal pressure.'),
            ('science', 'plant,plants,sun,water,air,soil,grow', 'Plants need sunlight, water, air, and soil to grow.'),
            ('greeting', 'hello,hi,hey,good morning,good afternoon', 'Hello! I am a friendly learning chatbot for kids.'),
            ('farewell', 'bye,goodbye,see you,see ya', 'Goodbye! Come back anytime to learn more.')
        ]
        conn.executemany(
            'INSERT INTO knowledge (category, keywords, answer) VALUES (?, ?, ?)',
            sample_data
        )
        conn.commit()

    conn.close()

import os
import sqlite3
from chatbot.trainer import load_csv_file, create_knowledge_table

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database', 'chatbot.db')
DATA_DIR = os.path.join(BASE_DIR, 'dataset')


def delete_learned_rows(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute("DELETE FROM knowledge WHERE category = 'learned'")
    conn.commit()
    conn.close()


def main():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print('Deleted existing database:', DB_PATH)

    create_knowledge_table(DB_PATH)
    print('Created fresh knowledge table')

    csv_files = [
        os.path.join(DATA_DIR, 'math.csv'),
        os.path.join(DATA_DIR, 'science.csv'),
        os.path.join(DATA_DIR, 'english.csv'),
        os.path.join(DATA_DIR, 'smalltalk.csv')
    ]

    for csv_file in csv_files:
        if os.path.exists(csv_file):
            print(f'Loading {os.path.basename(csv_file)}...')
            load_csv_file(csv_file, DB_PATH)
        else:
            print(f'Warning: {csv_file} not found')

    print('Database reset complete:', DB_PATH)
    print('All learned data has been removed.')
    print('Fresh dataset has been loaded from CSV files.')


if __name__ == '__main__':
    main()

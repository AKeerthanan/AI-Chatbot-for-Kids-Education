import os
from trainer import reset_database

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database', 'chatbot.db')


def main():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    reset_database(DB_PATH)
    print('Database reset complete:', DB_PATH)


if __name__ == '__main__':
    main()

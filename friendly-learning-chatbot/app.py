import os
import re
from flask import Flask, request, jsonify, render_template, session
from chatbot.chatbot_engine import get_response, save_knowledge
from database.db_setup import init_db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'chatbot.db')

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')

SKIP_KEYWORDS = {'skip', 'cancel', 'no', 'never mind', 'nevermind'}
TEACH_PREFIX = 'teach:'
UNKNOWN_PROMPT = 'I don’t know that yet. If you want to teach me, type: teach: your answer. Or type skip.'


def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s:]', '', text)
    return ' '.join(text.split())


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(force=True)
    if not data or 'message' not in data:
        return jsonify({'response': 'Please send a message in JSON format.'}), 400

    message = data['message'].strip()
    if not message:
        return jsonify({'response': 'Please type a message.'}), 400

    normalized = normalize_text(message)
    pending_question = session.get('pending_question')

    if pending_question:
        if normalized in SKIP_KEYWORDS:
            session.pop('pending_question', None)
            return jsonify({'response': 'Okay, no problem 😊'})

        if normalized.startswith(TEACH_PREFIX):
            answer_text = message[len(TEACH_PREFIX):].strip()
            if not answer_text or answer_text.lower() in SKIP_KEYWORDS:
                session.pop('pending_question', None)
                return jsonify({'response': 'Okay, no problem 😊'})

            saved = save_knowledge(pending_question, answer_text, DATABASE_PATH)
            session.pop('pending_question', None)
            if saved:
                return jsonify({'response': 'Thanks! I learned something new.'})
            return jsonify({'response': 'I could not save that right now. Try again.'}), 500

        session.pop('pending_question', None)
        response_text = get_response(message, DATABASE_PATH)
        if response_text == UNKNOWN_PROMPT:
            session['pending_question'] = message
        return jsonify({'response': response_text})

    if normalized.startswith(TEACH_PREFIX):
        return jsonify({'response': 'I do not have a question to learn yet. Ask a question first.'})

    response_text = get_response(message, DATABASE_PATH)
    if response_text == UNKNOWN_PROMPT:
        session['pending_question'] = message
    return jsonify({'response': response_text})


if __name__ == '__main__':
    init_db(DATABASE_PATH)
    app.run(debug=True)

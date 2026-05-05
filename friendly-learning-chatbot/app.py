import os
import re
from flask import Flask, request, jsonify, render_template, session
from chatbot.chatbot_engine import get_response, UNKNOWN_PROMPT
from chatbot.trainer import save_pending_knowledge
from chatbot.nlp_processor import normalize_text, normalize_repeated_letters, normalize_greeting, is_question_input, calculate_expression, get_small_talk_response
from database.db_setup import init_db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'chatbot.db')

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')

CANCEL_KEYWORDS = {'skip', 'cancel', 'no', 'never mind', 'nevermind', 'dont know', 'don\'t know'}
YES_KEYWORDS = {'yes', 'y'}


def has_vowel(text):
    return any(char in 'aeiou' for char in text.lower())


def is_random_letters(text):
    text_lower = text.lower()
    letters = ''.join([char for char in text_lower if char.isalpha()])
    if len(letters) < 4:
        return False
    vowel_count = sum(1 for char in letters if char in 'aeiou')
    if vowel_count == 0:
        return True
    return (vowel_count / len(letters)) < 0.2


def is_invalid_answer(message, normalized_text):
    answer = message.strip()
    if len(answer) < 4:
        return True
    if is_question_input(message, normalized_text):
        return True
    if get_small_talk_response(message) is not None:
        return True
    if calculate_expression(message) is not None:
        return True
    if not has_vowel(normalized_text):
        return True
    if is_random_letters(normalized_text):
        return True
    if len(normalized_text.split()) == 1 and len(normalized_text) < 4:
        return True
    return False


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
    pending_answer = session.get('pending_answer')

    if pending_answer:
        if normalized in YES_KEYWORDS:
            question = session.pop('pending_question', None)
            answer_text = session.pop('pending_answer', None)
            if not question or not answer_text:
                return jsonify({'response': 'Sorry, something went wrong. Please ask your question again.'}), 500
            saved = save_pending_knowledge(question, answer_text, DATABASE_PATH)
            if saved:
                return jsonify({'response': 'Thanks! I saved it for review :)'})
            return jsonify({'response': 'That answer is already saved. :)'})
        if normalized in CANCEL_KEYWORDS:
            session.pop('pending_question', None)
            session.pop('pending_answer', None)
            return jsonify({'response': 'That\'s okay :)'})
        return jsonify({'response': 'Please type yes or no to save this answer.'})

    if pending_question:
        if normalized in CANCEL_KEYWORDS:
            session.pop('pending_question', None)
            return jsonify({'response': 'That\'s okay :)'})
        if is_question_input(message, normalized):
            session.pop('pending_question', None)
            response_text = get_response(message, DATABASE_PATH)
            if response_text == UNKNOWN_PROMPT:
                session['pending_question'] = message
            return jsonify({'response': response_text})
        if is_invalid_answer(message, normalized):
            session.pop('pending_question', None)
            return jsonify({'response': 'That does not look like a clear answer :)'})
        session['pending_answer'] = message
        return jsonify({'response': f'You said: "{message}". Should I save this? Type yes or no.'})

    response_text = get_response(message, DATABASE_PATH)
    if response_text == UNKNOWN_PROMPT:
        session['pending_question'] = message
    return jsonify({'response': response_text})


if __name__ == '__main__':
    init_db(DATABASE_PATH)
    app.run(debug=True)

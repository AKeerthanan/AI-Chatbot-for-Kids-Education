# -*- coding: utf-8 -*-
import re

STOP_WORDS = {
    'what', 'is', 'a', 'an', 'the', 'please', 'can', 'you', 'me',
    'do', 'does', 'did', 'tell', 'about', 'of', 'for', 'in', 'on',
    'at', 'to', 'from', 'and', 'are', 'am', 'i', 'it', 'that', 'this',
    'explain', 'describe', 'define', 'say', 'said'
}
MATH_PATTERN = re.compile(r'\b\d+(?:\.\d+)?(?:\s*[+\-*/]\s*\d+(?:\.\d+)?)+\b')
SMALL_TALK_RESPONSES = {
    'hi': 'Hi there! :)',
    'hello': 'Hello! :)',
    'hey': 'Hey there! :)',
    'good morning': 'Good morning. Have a great day!',
    'good afternoon': 'Good afternoon. How is your day going?',
    'good evening': 'Good evening. Hope you had a nice day!',
    'how are you': 'I am doing great, thank you!',
    'thank you': 'You are welcome!',
    'thanks': 'You are welcome!',
    'yes': 'Okay :)',
    'yeah': 'Okay :)',
    'no': 'That is okay :)',
    'nah': 'That is okay :)',
    'nope': 'That is okay :)',
    'okay': 'Okay! :)',
    'ok': 'Okay! :)',
    'okey': 'Okay! :)',
    'bye': 'Goodbye! See you soon!',
    'goodbye': 'Goodbye! See you soon!',
    'see you': 'Goodbye! See you soon!',
}

EMOTION_RESPONSES = {
    'positive': 'That is great to hear :) What would you like to learn today?',
    'sad': 'I am sorry you feel that way. Please talk to a parent, teacher, or someone you trust',
    'bored': 'Let us learn something fun. You can ask me a math, science, or English question :)',
    'tired': 'Maybe you need a short break. Resting can help you feel better :)',
    'sick': 'I am sorry you feel unwell. Please tell a parent or teacher so they can help you'
}

POSITIVE_MOOD_KEYWORDS = {'great', 'good', 'happy', 'fine', 'excited', 'amazing', 'nice'}
SAD_KEYWORDS = {'sad', 'unhappy', 'upset', 'crying', 'lonely', 'bad'}
BORED_KEYWORDS = {'bored', 'boring', 'nothing to do'}
TIRED_KEYWORDS = {'tired', 'sleepy', 'lazy', 'exhausted', 'rest', 'sleep'}
SICK_KEYWORDS = {'sick', 'unwell', 'fever', 'pain', 'feeling well'}


def normalize_repeated_letters(text):
    text = text.lower()
    text = re.sub(r'(.)\1{2,}', r'\1\1', text)
    return text


def normalize_greeting(text):
    text = normalize_repeated_letters(text)
    if text.startswith('hi'):
        return 'hi'
    if text.startswith('hel'):
        return 'hello'
    if text.startswith('hey'):
        return 'hey'
    return text


def extract_math_expression(text):
    text = text.replace('*', '*').replace('/', '/')
    match = MATH_PATTERN.search(text)
    return match


def calculate_expression(user_input):
    match = extract_math_expression(user_input)
    if not match:
        return None

    expression = match.group()
    expression = re.sub(r'\s+', '', expression)

    if not re.match(r'^[\d.+\-*/]+$', expression):
        return None

    try:
        result = eval(expression, {"__builtins__": None}, {})
        if isinstance(result, (int, float)):
            if result.is_integer():
                return str(int(result))
            return str(result)
    except (ValueError, ZeroDivisionError, OverflowError):
        return None

    return None


def normalize_text(text):
    text = normalize_repeated_letters(text)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return ' '.join(text.split())


def is_question_input(text, normalized_text):
    if '?' in text:
        return True
    words = normalized_text.split()
    if words and words[0] in {'what', 'why', 'how', 'who', 'where', 'when'}:
        return True
    return False


def detect_emotion(text):
    """Detect emotion-based intent from user input."""
    normalized = normalize_text(text)
    words = set(normalized.split())
    
    # Check for positive mood
    if any(word in POSITIVE_MOOD_KEYWORDS for word in words):
        return 'positive'
    
    # Check for sadness
    if any(word in SAD_KEYWORDS for word in words):
        return 'sad'
    
    # Check for boredom
    if any(word in BORED_KEYWORDS for word in words):
        return 'bored'
    
    # Check for tired/lazy
    if any(word in TIRED_KEYWORDS for word in words):
        return 'tired'
    
    # Check for sick
    if any(word in SICK_KEYWORDS for word in words):
        return 'sick'
    
    return None


def get_emotion_response(emotion_type):
    """Get response for detected emotion."""
    return EMOTION_RESPONSES.get(emotion_type)


def get_small_talk_response(text):
    sentence = normalize_text(text)
    
    if sentence in SMALL_TALK_RESPONSES:
        return SMALL_TALK_RESPONSES[sentence]
    
    if sentence.startswith('thank'):
        return SMALL_TALK_RESPONSES['thanks']
    
    if sentence in {'how are you', 'how are you doing'}:
        return SMALL_TALK_RESPONSES['how are you']
    
    return None


def tokenize(text):
    cleaned = normalize_text(text)
    tokens = [word for word in cleaned.split() if word and word not in STOP_WORDS]
    return tokens


def get_keywords(text):
    return list(dict.fromkeys(tokenize(text)))

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
    'hi': 'Hi there! Smile',
    'hello': 'Hello! Wave',
    'hey': 'Hey there! Smile',
    'good morning': 'Good morning. Have a great day! Sun',
    'good afternoon': 'Good afternoon. How is your day going? Smile',
    'good evening': 'Good evening. Hope you had a nice day! Moon',
    'how are you': 'I am doing great, thank you! Smile',
    'thank you': 'You are welcome! Smile',
    'thanks': 'You are welcome! Smile',
    'yes': 'That is great! Smile',
    'no': 'That is okay Smile',
    'okay': 'Okay! Smile',
    'ok': 'Okay! Smile',
    'okey': 'Okay! Smile',
    'nah': 'That is okay Smile',
    'nope': 'That is okay Smile',
    'bye': 'Goodbye! See you soon! Wave',
    'goodbye': 'Goodbye! See you soon! Wave',
    'see you': 'Goodbye! See you soon! Wave',
    'i am bored': 'Let us learn something fun. You can ask me a math, science, or English question. Books',
    'im bored': 'Let us learn something fun. You can ask me a math, science, or English question. Books',
    'i am sleepy': 'Maybe you need some rest. Taking a short break can help. Sleepy',
    'im sleepy': 'Maybe you need some rest. Taking a short break can help. Sleepy',
    'i am tired': 'Maybe you need some rest. Taking a short break can help. Sleepy',
    'im tired': 'Maybe you need some rest. Taking a short break can help. Sleepy',
    'i do not feel well': 'I am sorry you feel that way. Please tell a parent or teacher so they can help you. Heart',
    'i dont feel well': 'I am sorry you feel that way. Please tell a parent or teacher so they can help you. Heart',
    'i am sad': 'I am sorry you feel sad. It is okay to feel sad sometimes. Talk to someone you trust about how you feel. Heart',
    'i am angry': 'It is okay to feel angry. Try taking deep breaths or talking about what made you angry. Calm',
    'im angry': 'It is okay to feel angry. Try taking deep breaths or talking about what made you angry. Calm',
    'i am scared': 'It is normal to feel scared sometimes. Remember, you are safe. Talk to a trusted adult if you need help. Hug',
    'help': 'I am here to help! Ask me questions about math, science, English, or tell me how you feel. Books',
    'what can you do': 'I can answer questions about math, science, and English. I can also listen if you want to talk! Smile',
    'what is your name': 'I am a Friendly Learning Chatbot! Nice to meet you! Smile'
}


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

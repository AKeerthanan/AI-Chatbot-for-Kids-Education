import re

STOP_WORDS = {
    'what', 'is', 'a', 'an', 'the', 'please', 'can', 'you', 'me',
    'do', 'does', 'did', 'tell', 'about', 'of', 'for', 'in', 'on',
    'at', 'to', 'from', 'and', 'are', 'am', 'i', 'it', 'that', 'this'
}
MATH_PATTERN = re.compile(r'(-?\d+(?:\.\d+)?)(?:\s*)([+\-*/])(?:\s*)(-?\d+(?:\.\d+)?)')
SMALL_TALK_RESPONSES = {
    'hi': 'Hi there! 😊',
    'hello': 'Hello! 😊',
    'good morning': 'Good morning 😊',
    'good evening': 'Good evening 😊',
    'how are you': 'I’m doing great, thank you! 😊',
    'thank you': 'You’re welcome! 😊',
    'thanks': 'You’re welcome! 😊',
    'bye': 'Goodbye! 😊',
    'goodbye': 'Goodbye! 😊',
    'see you': 'Goodbye! 😊'
}


def extract_math_expression(text):
    text = text.replace('×', '*').replace('÷', '/')
    match = MATH_PATTERN.search(text)
    return match


def calculate_expression(user_input):
    match = extract_math_expression(user_input)
    if not match:
        return None

    left_text, operator, right_text = match.groups()
    try:
        left_value = float(left_text)
        right_value = float(right_text)
    except ValueError:
        return None

    if operator == '+':
        result = left_value + right_value
    elif operator == '-':
        result = left_value - right_value
    elif operator == '*':
        result = left_value * right_value
    elif operator == '/':
        if right_value == 0:
            return 'I cannot divide by zero.'
        result = left_value / right_value
    else:
        return None

    if result.is_integer():
        return str(int(result))
    return str(result)


def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return ' '.join(text.split())


def get_small_talk_response(text):
    sentence = normalize_text(text)
    if sentence in SMALL_TALK_RESPONSES:
        return SMALL_TALK_RESPONSES[sentence]
    if sentence.startswith('thank you') or sentence.startswith('thanks'):
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

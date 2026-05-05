from .inference import find_best_answer
from .nlp_processor import calculate_expression, get_small_talk_response, normalize_greeting

UNKNOWN_PROMPT = 'I don\'t know that yet. Can you tell me the answer?'


def get_response(user_input, db_path):
    normalized_greeting = normalize_greeting(user_input)
    if normalized_greeting in ['hi', 'hello', 'hey']:
        if normalized_greeting == 'hi':
            return 'Hi there! :)'
        elif normalized_greeting == 'hello':
            return 'Hello! :)'
        else:
            return 'Hey there! :)'

    math_answer = calculate_expression(user_input)
    if math_answer is not None:
        return math_answer

    small_talk_answer = get_small_talk_response(user_input)
    if small_talk_answer is not None:
        return small_talk_answer

    response = find_best_answer(user_input, db_path)
    return response

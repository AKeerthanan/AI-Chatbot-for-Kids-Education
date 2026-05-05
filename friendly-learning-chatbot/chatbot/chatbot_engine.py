from .inference import find_best_answer
from .trainer import save_knowledge as store_knowledge
from .nlp_processor import calculate_expression, get_small_talk_response

UNKNOWN_PROMPT = 'I don’t know that yet. If you want to teach me, type: teach: your answer. Or type skip.'


def get_response(user_input, db_path):
    math_answer = calculate_expression(user_input)
    if math_answer is not None:
        return math_answer

    small_talk_answer = get_small_talk_response(user_input)
    if small_talk_answer is not None:
        return small_talk_answer

    return find_best_answer(user_input, db_path)


def save_knowledge(question, answer, db_path):
    return store_knowledge(question, answer, db_path)

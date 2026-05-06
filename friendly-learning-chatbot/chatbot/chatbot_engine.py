from .inference import find_best_answer
from .nlp_processor import (
    calculate_expression, get_small_talk_response, normalize_greeting,
    detect_emotion, get_emotion_response
)

UNKNOWN_PROMPT = 'I don\'t know that yet. Can you tell me the answer?'


def get_response(user_input, db_path):
    # Priority 1: Fuzzy greeting detection
    normalized_greeting = normalize_greeting(user_input)
    if normalized_greeting in ['hi', 'hello', 'hey']:
        if normalized_greeting == 'hi':
            return 'Hi there! :)'
        elif normalized_greeting == 'hello':
            return 'Hello! :)'
        else:
            return 'Hey there! :)'

    # Priority 2: Math expressions
    math_answer = calculate_expression(user_input)
    if math_answer is not None:
        return math_answer

    # Priority 3: Simple smalltalk (yes/no/okay)
    small_talk_answer = get_small_talk_response(user_input)
    if small_talk_answer is not None:
        return small_talk_answer

    # Priority 4: Emotion-based responses (before learning)
    emotion = detect_emotion(user_input)
    if emotion:
        emotion_response = get_emotion_response(emotion)
        if emotion_response:
            return emotion_response

    # Priority 5: Database search
    response = find_best_answer(user_input, db_path)
    return response

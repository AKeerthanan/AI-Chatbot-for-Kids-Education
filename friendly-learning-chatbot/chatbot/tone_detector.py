import random

# Tone definitions with keywords and emoji lists
TONE_RULES = {
    'happy': {
        'keywords': ['happy', 'good', 'great', 'excited', 'nice', 'amazing', 'fun', 'love', 'awesome', 'wonderful'],
        'emojis': ['😊', '😄', '🌟']
    },
    'sad': {
        'keywords': ['sad', 'unhappy', 'crying', 'upset', 'lonely', 'bad', 'sorry'],
        'emojis': ['💛', '😢']
    },
    'sick': {
        'keywords': ['sick', 'unwell', 'not feel well', 'fever', 'pain', 'tired', 'hurt'],
        'emojis': ['💛', '🧸']
    },
    'scared': {
        'keywords': ['scared', 'afraid', 'fear', 'worried', 'nervous', 'frightened'],
        'emojis': ['💛', '🫶']
    },
    'angry': {
        'keywords': ['angry', 'mad', 'annoyed', 'upset', 'frustrated'],
        'emojis': ['😌', '💛']
    },
    'greeting': {
        'keywords': ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'morning', 'afternoon', 'evening'],
        'emojis': ['👋', '😊']
    },
    'learning': {
        'keywords': ['help', 'explain', 'learn', 'teach', 'understand', 'what', 'how', 'why', 'tell'],
        'emojis': ['📘', '🌟']
    },
    'joke': {
        'keywords': ['joke', 'funny', 'laugh', 'fun', 'giggle'],
        'emojis': ['😂', '😄']
    }
}

DEFAULT_EMOJIS = ['😊']


def detect_tone(user_input):
    """
    Detect the tone of the user's input based on keywords.
    Returns the tone name or 'neutral' if no tone is detected.
    """
    user_words = user_input.lower().split()
    
    for tone, rules in TONE_RULES.items():
        if any(keyword in user_words for keyword in rules['keywords']):
            return tone
    
    return 'neutral'


def add_tone_emoji(response, user_input):
    """
    Add a random emoji based on the detected tone.
    Avoids adding emojis to pure math answers.
    """
    # Don't add emojis to pure math answers (just numbers)
    if response.strip().replace('.', '').replace('-', '').isdigit():
        return response
    
    tone = detect_tone(user_input)
    
    if tone in TONE_RULES:
        emoji_list = TONE_RULES[tone]['emojis']
    else:
        emoji_list = DEFAULT_EMOJIS
    
    # Select a random emoji
    selected_emoji = random.choice(emoji_list)
    
    # Avoid duplicate emojis if the response already ends with one
    if response.endswith(tuple(emoji_list + DEFAULT_EMOJIS)):
        return response
    
    return f"{response} {selected_emoji}"
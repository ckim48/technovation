# Natural Language Processing (NLP) --> giving ability to understand human language
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report
import random

# Tokenizers --> punkt
# Corpora  --> word/wordnet

# Rule-based
intents_patterns = {
    "greet": {
        "patterns": [
            "hello", "hi", "good day", "hey there", "good morning", "good evening", "hey", "yo", "howdy"
        ],
        "responses": [
            "Hello! How can I assist you today?",
            "Hi there! What can I do for you?",
            "Good day! How can I help you feel better today?"
        ]
    },
    "goodbye": {
        "patterns": [
            "bye", "goodbye", "see you later", "I have to go", "catch you later", "I'm off", "good night"
        ],
        "responses": [
            "Take care! If you need more help, just say hi again.",
            "Goodbye! Remember, I'm here whenever you need support.",
            "See you later! Don't hesitate to come back if you need anything."
        ]
    },
    "anxiety_support": {
        "patterns": [
            "I feel anxious", "I'm worried", "anxiety", "I can't stop worrying", "I'm feeling nervous",
            "nervousness is killing me", "my mind won't quiet", "I'm so tense"
        ],
        "responses": [
            "I'm sorry to hear you're feeling anxious. Let's try some deep breathing together. Breathe in slowly, hold for a few seconds, and exhale slowly. How do you feel?",
            "Anxiety can be tough, but I'm here to support you. Try to focus on the present moment. What do you see around you?",
            "Feeling anxious is something many of us experience. Let's talk about what might be causing it. Do you want to discuss what’s on your mind?"
        ]
    },
    "stress_management": {
        "patterns": [
            "I'm stressed", "too much pressure", "stress", "everything is overwhelming", "I'm burnt out",
            "there's too much going on", "I can't handle this", "it's all too much"
        ],
        "responses": [
            "Stress can be overwhelming. Let's discuss some relaxation techniques. Have you tried guided meditation or progressive muscle relaxation?",
            "It sounds like you're under a lot of stress. Taking a short break might help. What relaxes you? Maybe listening to some calm music or a walk?",
            "Managing stress is key to wellbeing. Have you tried writing down what you feel? Sometimes putting it on paper can help manage the load."
        ]
    },
    "depression_help": {
        "patterns": [
            "I feel sad", "I'm depressed", "nothing makes me happy", "I don't feel like doing anything",
            "life feels dull", "why do I feel so sad?", "everything is gray", "I feel hopeless"
        ],
        "responses": [
            "I'm really sorry to hear that. It's okay to talk about these feelings here. Talking can be really liberating. What’s been on your mind lately?",
            "Depression is a heavy burden. Would you like to talk more about what's been going on? Sometimes sharing can relieve a lot of pressure.",
            "Sometimes just sharing how you feel can be a start. I’m here to listen. What do you think has led to these feelings?"
        ]
    },
    "general_advice": {
        "patterns": [
            "Give me advice", "any tips?", "how can I feel better?", "what should I do?", "I need guidance",
            "how to improve my mood?", "what can I do right now?"
        ],
        "responses": [
            "Maintaining a regular routine can be helpful. Have you tried setting daily goals? It helps bring a sense of accomplishment.",
            "Sometimes, talking to someone can really help. Do you have someone to talk to about your feelings? If not, I’m here.",
            "Exercise can often lift your mood. Even a short walk might make a difference. When was the last time you had some fresh air?"
        ]
    },
    "encouragement": {
        "patterns": [
            "I need some encouragement", "cheer me up", "I'm feeling down", "can you motivate me?",
            "I need a boost", "give me a pep talk", "help me keep going"
        ],
        "responses": [
            "You're doing great, and don't forget how strong you are!",
            "Every step you take is one more toward your goal. Keep pushing, you're getting there!",
            "Remember, it's okay to have tough days. You're capable of overcoming them, and I believe in you. What’s one small thing you can do right now that you’d enjoy?"
        ]
    }
}

def text_preprocessing(user_message):
    user_message = user_message.lower()
    tokens = word_tokenize(user_message)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    result = " ".join(filtered_tokens)
    result = re.sub(r'[^\w\s]', '', result)
    return result

# Prepare training data
sentences, labels = [], []
for intent, details in intents_patterns.items():
    for pattern in details["patterns"]:
        sentences.append(pattern)
        labels.append(intent)

model = make_pipeline(TfidfVectorizer(), MultinomialNB())
model.fit(sentences, labels)

def get_response(user_input):
    try:
        preprocessed_input = text_preprocessing(user_input)
        predicted_intent = model.predict([preprocessed_input])[0]
        responses = intents_patterns[predicted_intent]["responses"]
        return random.choice(responses)
    except Exception as e:
        return "I'm sorry, I'm not sure how to respond to that. Can you try asking in a different way?"

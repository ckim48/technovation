# Natural Language Processing (NLP) --> giving ability to understand human language
import nltk
# nltk.download('punkt')
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
    "greet":{
        "patterns": ["hello", "hi", "greetings","hello, this is Scott, nice to meet you"],
        "responses": ["Hello!", "Hi there!", "Welcome"]
    },
    "goodbye":{
        "patterns": ["bye", "goodbye","see you"],
        "responses": ["Goodbye!", "See you later!", "Bye!"]
    },
    "help": {
        "patterns": ["I need a help", "help me", "i need assistant"],
        "responses": ["What do you need?", "How can i help you"]
    }
    # Class
    # Grade
    # relationship
    # ...
    # Others
}
# User:hello --> "greet"
# User: I need a help --> "help"/"support"
def text_preprocessing(user_message):
    # text_preprocessing
    # 1. lowercasing
    user_message = user_message.lower()
    # 2. tokenization
    tokens = word_tokenize(user_message)
    # 3. Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    # 4. Remove punctuations
    result = " ".join(filtered_tokens)
    result = re.sub(r'[^\w\s]','',result)
    return result

sentences = []
labels = []
for intent, details in intents_patterns.items():
    for pattern in details["patterns"]:
        sentences.append(pattern)
        labels.append(intent)
print(sentences)
print(labels)

model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# training
model.fit(sentences, labels)

def get_response(user_input):
    preprocessed_input = text_preprocessing(user_input)
    predicted_intent = model.predict([preprocessed_input])[0]
    responses = intents_patterns[predicted_intent]["responses"]
    return random.choice(responses)

user_input = "nice to meet you"
print(get_response(user_input))
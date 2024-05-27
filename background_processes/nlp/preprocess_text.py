import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer


def preprocess_text(text):
    # Lowercase conversion
    # This step converts all the characters in the text to lowercase
    # It helps in treating words consistently regardless of their case
    text = text.lower()

    # Remove special characters and digits
    # This step removes any characters that are not alphabetic or whitespace
    # It helps in cleaning the text and removing unnecessary characters
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # Tokenization
    # This step splits the text into individual words or tokens
    # It helps in processing the text at a word level
    tokens = nltk.word_tokenize(text)

    # Remove stopwords
    # This step removes common words that do not carry much meaning (e.g., "the", "is", "an")
    # It helps in reducing the dimensionality of the text and focusing on important words
    # Reference: Bird, S., Klein, E., & Loper, E. (2009). Natural Language Processing with Python. O'Reilly Media, Inc.
    stop_words = set(stopwords.words("english"))
    tokens = [token for token in tokens if token not in stop_words]

    # Lemmatization
    # This step reduces words to their base or dictionary form (e.g., "running" -> "run")
    # It helps in treating different word forms as the same concept
    # Reference: Bird, S., Klein, E., & Loper, E. (2009). Natural Language Processing with Python. O'Reilly Media, Inc.
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # Join tokens back into a string
    # This step combines the preprocessed tokens back into a single string
    # It prepares the text for further processing or analysis
    cleaned_text = " ".join(tokens)

    # Vectorize the cleaned text
    # This step converts the preprocessed text into a numerical representation using TF-IDF
    # TF-IDF (Term Frequency-Inverse Document Frequency) assigns weights to words based on their importance
    # Words that are frequent in a document but rare in the overall corpus receive higher weights
    vectorizer = TfidfVectorizer()
    vectorized_text = vectorizer.fit_transform([cleaned_text])

    return cleaned_text, vectorized_text

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

from tasks.nlp import extract_keywords

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def download_nltk_resources():
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

def preprocess_text(text):
    # Download the required NLTK resources
    download_nltk_resources()

    # Convert the text to lowercase to ensure uniformity
    text = text.lower()

    # Remove punctuation from the text as it doesn't add any extra information while processing text data.
    text = re.sub(r'[^\w\s]', '', text)

    # Remove numbers from the text as they are not needed for text processing
    text = re.sub(r'\d+', '', text)

    # Remove stop words as they are commonly used words that will likely appear in any text
    stop_words = set(stopwords.words('english'))
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    text = ' '.join(filtered_words)

    # Perform stemming - reducing inflected (or sometimes derived) words to their word stem (base form)
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in filtered_words]
    text = ' '.join(stemmed_words)

    # Tokenize the text by splitting the text into words
    tokens = nltk.word_tokenize(text)

    # Return the tokens
    return tokens

def train_and_save_classification_model():
    # Load the CSV data into a pandas DataFrame
    data = pd.read_csv('arxiv_training_data.csv')


    # Apply the function to the 'abstract' column and create a new column 'cleaned_abstract'.
    print('Cleaning the abstract text...')
    for i, abstract in enumerate(data['abstract']):
        if i % 1000 == 0:
            print(f'Processed {i} abstracts')
        data.loc[i, 'cleaned_abstract'] = ' '.join(preprocess_text(abstract))

    # Split the data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(data['cleaned_abstract'], data['main_category'],
                                                        test_size=0.2,
                                                        random_state=42)

    # Vectorize the text data
    print('Training the classification model...')
    vectorizer = TfidfVectorizer()
    x_train_vectorized = vectorizer.fit_transform(x_train)
    x_test_vectorized = vectorizer.transform(x_test)

    # Train the Naive Bayes model
    nb_classifier = MultinomialNB()
    nb_classifier.fit(x_train_vectorized, y_train)
    print('Classification model trained!')

    # Evaluate the model
    y_pred = nb_classifier.predict(x_test_vectorized)
    print(classification_report(y_test, y_pred))

    # Save the trained model and vectorizer
    print('Saving the model and vectorizer...')
    joblib.dump(nb_classifier, 'nb_classifier.joblib')
    joblib.dump(vectorizer, 'vectorizer.joblib')
    print('Model saved!')


def classify_new_abstract():
    # Classify a new article
    new_article_abstract = ''''''
    # Load the saved model and vectorizer
    nb_classifier = joblib.load('nb_classifier.joblib')
    vectorizer = joblib.load('vectorizer.joblib')

    new_article_vectorized = vectorizer.transform([new_article_abstract])
    predicted_category = nb_classifier.predict(new_article_vectorized)
    print(f"Predicted category for the new article: {predicted_category}")

# train_and_save_classification_model()
classify_new_abstract()
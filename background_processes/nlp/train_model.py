import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import logging

from background_processes.nlp import preprocess_text
from background_processes.nlp.common import download_nltk_resources

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def train_model():
    download_nltk_resources()

    # Load the CSV dataset
    df = pd.read_csv("arxiv_training_data.csv")

    # Preprocess the abstracts
    df["cleaned_abstract"] = df["abstract"].apply(preprocess_text)

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        df["cleaned_abstract"], df["main_category"], test_size=0.2, random_state=42
    )

    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform the training data
    X_train_tfidf = vectorizer.fit_transform(X_train)

    # Train the SVM model
    svm_model = SVC(kernel="linear", C=1.0, random_state=42)
    svm_model.fit(X_train_tfidf, y_train)

    # Transform the testing data
    X_test_tfidf = vectorizer.transform(X_test)

    # Evaluate the model
    y_pred = svm_model.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="weighted")
    recall = recall_score(y_test, y_pred, average="weighted")
    f1 = f1_score(y_test, y_pred, average="weighted")

    logging.info(f"Accuracy: {accuracy:.4f}")
    logging.info(f"Precision: {precision:.4f}")
    logging.info(f"Recall: {recall:.4f}")
    logging.info(f"F1-score: {f1:.4f}")

    # Save the trained model and vectorizer
    joblib.dump(svm_model, "svm_model.pkl")
    joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

    logging.info("Model and vectorizer saved successfully.")

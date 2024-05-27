import os
import joblib
import numpy as np
from background_processes.nlp.preprocess_text import preprocess_text

current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the file paths relative to the current directory
# This ensures that the model and vectorizer files can be located correctly
model_path = os.path.join(current_dir, "svm_model.pkl")
vectorizer_path = os.path.join(current_dir, "tfidf_vectorizer.pkl")


def predict_article_categories(text: str):
    # Load the saved model and vectorizer
    # This step retrieves the trained SVM model and TF-IDF vectorizer from disk
    loaded_model = joblib.load(model_path)
    loaded_vectorizer = joblib.load(vectorizer_path)

    # Preprocess the new article's abstract(s)
    # This step applies text preprocessing to the input text, such as lowercasing, tokenization, etc.
    preprocessed_text, _ = preprocess_text(text)

    # Transform the preprocessed abstract
    # This step converts the preprocessed text into a TF-IDF feature vector using the loaded vectorizer
    # TF-IDF (Term Frequency-Inverse Document Frequency) is a numerical statistic that reflects the importance
    # of a word in a document within a collection of documents. It considers both the frequency of a word in a
    # document (TF) and the inverse frequency of the word across all documents (IDF). Words that are frequent
    # in a document but rare in the overall collection receive higher TF-IDF scores.
    new_abstract_tfidf = loaded_vectorizer.transform([preprocessed_text])

    # Predict the main category
    # This step uses the loaded SVM model to predict the main category of the article based on the TF-IDF features
    # predicted_category = loaded_model.predict(new_abstract_tfidf)
    # print("Predicted Category:", predicted_category[0])

    # Get the decision function values
    # This step retrieves the decision function values from the SVM model for the input article
    decision_values = loaded_model.decision_function(new_abstract_tfidf)

    # Apply softmax function to convert decision function values to percentages
    # This step converts the decision function values into percentages using the softmax function
    percentages = np.exp(decision_values) / np.sum(
        np.exp(decision_values), axis=1, keepdims=True
    )
    percentages = percentages * 100

    # Get the class labels
    # This step retrieves the class labels (category names) from the trained SVM model
    class_labels = loaded_model.classes_

    # Create a dictionary to store the percentages for each class
    # This step associates each class label with its corresponding percentage and formats it as a string
    percentages_per_class = {
        label: f"{percentage:.2f}%"
        for label, percentage in zip(class_labels, percentages[0])
    }

    return percentages_per_class

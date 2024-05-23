import os
import joblib
import numpy as np

from background_processes.nlp.preprocess_text import preprocess_text

current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the file paths relative to the current directory
model_path = os.path.join(current_dir, 'svm_model.pkl')
vectorizer_path = os.path.join(current_dir, 'tfidf_vectorizer.pkl')

def predict_article_categories(text: str):
    # Load the saved model and vectorizer
    loaded_model = joblib.load(model_path)
    loaded_vectorizer = joblib.load(vectorizer_path)

    # Preprocess the new article's abstract(s)
    preprocessed_text, _ = preprocess_text(text)

    # Transform the preprocessed abstract
    new_abstract_tfidf = loaded_vectorizer.transform([preprocessed_text])

    # Predict the main category
    predicted_category = loaded_model.predict(new_abstract_tfidf)
    print("Predicted Category:", predicted_category[0])

    # Get the decision function values
    decision_values = loaded_model.decision_function(new_abstract_tfidf)

    # Apply softmax function to convert decision function values to percentages
    percentages = np.exp(decision_values) / np.sum(np.exp(decision_values), axis=1, keepdims=True)
    percentages = percentages * 100

    # Get the class labels
    class_labels = loaded_model.classes_

    percentages_per_class = {label: f"{percentage:.2f}%" for label, percentage in zip(class_labels, percentages[0])}

    return percentages_per_class


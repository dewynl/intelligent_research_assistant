import joblib
import numpy as np

from background_processes.nlp.preprocess_text import preprocess_text


def predict_article_category(text: str):
    # Load the saved model and vectorizer
    loaded_model = joblib.load('svm_model.pkl')
    loaded_vectorizer = joblib.load('tfidf_vectorizer.pkl')

    # Preprocess the new article's abstract
    preprocessed_abstract = preprocess_text(text)

    # Transform the preprocessed abstract
    new_abstract_tfidf = loaded_vectorizer.transform([preprocessed_abstract])

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

    # Print the percentages for each class
    print("\nPercentages for each class:")
    for label, percentage in zip(class_labels, percentages[0]):
        print(f"{label}: {percentage:.2f}%")

    return predicted_category[0]
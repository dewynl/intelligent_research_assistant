from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from collections import defaultdict
import string


def extract_keywords(text):
    # Tokenize the text into words
    # This step breaks the text into individual words for further processing
    words = word_tokenize(text.lower())

    # Remove punctuation, stopwords, and non-alphabetic words
    # We remove these to focus on meaningful words and reduce noise
    stop_words = set(stopwords.words("english") + list(string.punctuation))
    filtered_words = [
        word for word in words if word.isalpha() and word not in stop_words
    ]

    # If there is only one word, return it as the keyword
    # This is a base case to handle short or single-word texts
    if len(filtered_words) == 1:
        return filtered_words

    # Create a dictionary to store word co-occurrences
    # We use a defaultdict to automatically initialize nested dictionaries
    co_occurrences = defaultdict(lambda: defaultdict(int))

    # Build the co-occurrence matrix
    # We iterate over the filtered words and count the co-occurrences of word pairs
    # Co-occurrence refers to the frequency of two words appearing together in a given context
    # In this case, we consider two words as co-occurring if they appear next to each other in the text
    for i in range(len(filtered_words) - 1):
        for j in range(i + 1, len(filtered_words)):
            word1, word2 = filtered_words[i], filtered_words[j]
            co_occurrences[word1][word2] += 1
            co_occurrences[word2][word1] += 1

    # Calculate word scores based on co-occurrence frequency
    # We sum up the co-occurrence counts for each word to get its score
    word_scores = defaultdict(int)
    for word, neighbors in co_occurrences.items():
        score = sum(neighbors.values())
        word_scores[word] = score

    # Sort the words by their scores in descending order
    # This helps us identify the most important words based on their scores
    sorted_words = sorted(word_scores, key=word_scores.get, reverse=True)

    # Get the top N keywords
    # We extract the desired number of top keywords from the sorted list
    top_n = 10  # Adjust the number of keywords as needed
    top_keywords = sorted_words[:top_n]

    return top_keywords

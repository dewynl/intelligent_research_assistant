from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from collections import defaultdict
import string


def extract_keywords(text):
    # Tokenize the text into words
    words = word_tokenize(text.lower())

    # Remove punctuation, stopwords, and non-alphabetic words
    stop_words = set(stopwords.words('english') + list(string.punctuation))
    filtered_words = [word for word in words if word.isalpha() and word not in stop_words]

    if len(filtered_words) == 1:
        return filtered_words

    # Create a dictionary to store word co-occurrences
    co_occurrences = defaultdict(lambda: defaultdict(int))

    # Build the co-occurrence matrix
    for i in range(len(filtered_words) - 1):
        for j in range(i + 1, len(filtered_words)):
            word1, word2 = filtered_words[i], filtered_words[j]
            co_occurrences[word1][word2] += 1
            co_occurrences[word2][word1] += 1

    # Calculate word scores based on co-occurrence frequency
    word_scores = defaultdict(int)
    for word, neighbors in co_occurrences.items():
        score = sum(neighbors.values())
        word_scores[word] = score

    # Sort the words by their scores in descending order
    sorted_words = sorted(word_scores, key=word_scores.get, reverse=True)

    # Get the top N keywords
    top_n = 10  # Adjust the number of keywords as needed
    top_keywords = sorted_words[:top_n]

    return top_keywords

def extract_keywords_with_synonyms(text):
    # Tokenize the text into words
    words = word_tokenize(text.lower())

    # Remove punctuation and stopwords
    stop_words = set(stopwords.words('english') + list(string.punctuation))
    filtered_words = [word for word in words if word not in stop_words]

    # Create a dictionary to store word co-occurrences
    co_occurrences = defaultdict(lambda: defaultdict(int))

    # Build the co-occurrence matrix
    for i in range(len(filtered_words) - 1):
        for j in range(i + 1, len(filtered_words)):
            word1, word2 = filtered_words[i], filtered_words[j]
            co_occurrences[word1][word2] += 1
            co_occurrences[word2][word1] += 1

    # Calculate word scores based on co-occurrence frequency
    word_scores = defaultdict(int)
    for word, neighbors in co_occurrences.items():
        score = sum(neighbors.values())
        word_scores[word] = score

    # Sort the words by their scores in descending order
    sorted_words = sorted(word_scores, key=word_scores.get, reverse=True)

    # Get the top N keywords
    top_n = 10  # Adjust the number of keywords as needed
    top_keywords = sorted_words[:top_n]

    # Expand keywords with synonyms
    expanded_keywords = []
    for keyword in top_keywords:
        synonyms = []
        for syn in wordnet.synsets(keyword):
            for lemma in syn.lemmas():
                synonym = lemma.name().lower().replace("_", " ")
                if synonym != keyword and synonym not in synonyms:
                    synonyms.append(synonym)
        expanded_keywords.append((keyword, synonyms))

    return expanded_keywords
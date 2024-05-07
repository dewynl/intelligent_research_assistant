import os
import spacy
from collections import Counter
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc
from celery import Celery

app = Celery(
    "tasks", broker=os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
)

nlp = spacy.load("en_core_web_sm")  # Load a small English NLP model


@app.task
def extract_keywords(sentence, n=2):
    # Process the input sentence
    doc = nlp(sentence)

    # Define a function to generate n-grams from a list of tokens
    def generate_ngrams(tokens, n):
        ngrams = zip(*[tokens[i:] for i in range(n)])
        return [" ".join(ngram) for ngram in ngrams]

    # Get individual tokens from the processed sentence
    tokens = [
        token.text
        for token in doc
        if not token.is_stop
        and not token.is_punct
        and token.pos_ in ["NOUN", "VERB", "ADJ", "ADV"]
    ]

    # Generate n-grams
    ngrams = []
    for i in range(1, n + 1):
        ngrams.extend(generate_ngrams(tokens, i))

    # Convert n-grams to spaCy Doc objects
    ngram_docs = [Doc(nlp.vocab, words=ngram.split()) for ngram in ngrams]

    # Initialize a PhraseMatcher
    matcher = PhraseMatcher(nlp.vocab)
    matcher.add("NgramMatcher", None, *ngram_docs)

    # Find matches in the original document
    matches = matcher(doc)

    # Get the matched phrases
    matched_phrases = [doc[start:end].text for match_id, start, end in matches]

    # Count the occurrences of each keyword
    keyword_counter = Counter(matched_phrases)

    # Return the keywords sorted by frequency
    keywords = [keyword for keyword, _ in keyword_counter.most_common()]

    return keywords

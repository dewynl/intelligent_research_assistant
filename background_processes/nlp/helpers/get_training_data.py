import logging
import os

import arxiv
import pandas as pd

from data_sources.arxiv import format_arxiv_result

ARXIV_SEARCH_TERMS = {
    "artificial_intelligence": [
        'machine learning', 'deep learning', 'neural network', 'artificial intelligence',
        'natural language processing', 'computer vision', 'reinforcement learning',
        'supervised learning', 'unsupervised learning', 'semi-supervised learning'
    ],
    "math": [
        'algebra', 'geometry', 'calculus', 'statistics', 'probability', 'differential equations',
        'linear algebra', 'discrete mathematics', 'number theory', 'topology'
    ],
    "physics": [
        'quantum mechanics', 'thermodynamics', 'electromagnetism', 'relativity', 'astrophysics',
        'particle physics', 'nuclear physics', 'optics', 'fluid dynamics', 'plasma physics'
    ],
    "biology": [
        'genetics', 'ecology', 'microbiology', 'biochemistry', 'molecular biology',
        'cell biology', 'genomics', 'immunology', 'neuroscience', 'physiology'
    ],
    "computer_science": [
        'algorithms', 'data structures', 'computer architecture', 'operating systems',
        'networking', 'databases', 'software engineering', 'programming languages',
        'computer graphics', 'artificial intelligence', 'machine learning', 'computer vision'
    ],
    "finance": [
        'financial modeling', 'corporate finance', 'investment banking', 'portfolio management',
        'risk management', 'financial analysis', 'financial planning', 'quantitative finance',
        'asset management', 'financial markets', 'financial economics', 'financial reporting'
    ]
}


def get_arxiv_training_data():
    all_results = []
    client = arxiv.Client(delay_seconds=10)

    for category, terms in ARXIV_SEARCH_TERMS.items():
        for term in terms:
            logging.info(f"Searching for term: {term} in category: {category}")
            search = arxiv.Search(
                query=term,
                max_results=1000,
                sort_by=arxiv.SortCriterion.Relevance,
            )

            results = client.results(search)
            results_as_dictionaries = [r.model_dump() for r in format_arxiv_result(results)]

            for i in range(len(results_as_dictionaries)):
                results_as_dictionaries[i]['main_category'] = category

            all_results.extend(results_as_dictionaries)

    # Create a pandas DataFrame from the list of dictionaries
    new_data = pd.DataFrame(all_results)

    # If the file exists, load the existing data and append the new data to it
    if os.path.isfile("../arxiv_training_data.csv"):
        df = pd.read_csv("../arxiv_training_data.csv")
        df = pd.concat([df, new_data])
    else:
        df = new_data

    # Remove duplicates
    df = df.drop_duplicates()

    # Save the DataFrame to a CSV file
    df.to_csv("arxiv_training_data.csv", index=False)

    return all_results

get_arxiv_training_data()
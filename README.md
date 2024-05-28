# Intelligent Research Assistant

The Intelligent Research Assistant Application is a web-based tool designed to streamline and enhance the online academic research process. By leveraging intelligent agents and natural language processing (NLP) techniques, this application aims to assist researchers in finding, analyzing, and organizing relevant scholarly articles more efficiently.
Features

- **Intelligent Search**: Users can enter keywords related to their research topic, and the application fetches relevant articles from the arXiv API.
- **Article Preprocessing**: The fetched articles undergo text preprocessing using advanced NLP techniques, including tokenization, stopword removal, lemmatization, and vectorization.
- **Summary Generation**: The application generates concise summaries by combining the abstracts of selected articles, providing researchers with a quick overview of the content.
- **Research Categorization**: A trained machine learning model is employed to categorize articles into predefined research areas, helping users identify the most relevant content for their needs.
- **Related Article Suggestion**: The application proactively suggests related articles based on the user's current research collection, facilitating the discovery of additional relevant resources.
- **Keyword Extraction**: The preprocessed article text is analyzed to extract the most significant keywords using a co-occurrence-based approach, enabling users to quickly grasp the main themes and concepts.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### How to Run

This is a step by step series of examples that tell you how to get a development environment running:

1. Clone the repository: `https://github.com/dewynl/intelligent_research_assistant`
2. Create a pyenv virtual environment: `python -m venv ./venv`
3. Install all dependencies: `pip install -r requirements.txt`
4. Run the FastAPI dev server: `uvicorn main:app --reload`
5. Run Celery workers: `celery -A celery_setup.celery_app worker --loglevel=info`
6. Run Celery beat: `celery -A celery_setup.celery_app beat --lglevel=info`
7. Run the React App:
   - Go to the front end app directory: `cd frontend`
   - Install all dependencies: `yarn install`
   - Run the react application: `yarn start`
8. Go to `http://localhost:3000/` to start using the application.

### Docker

If you have Docker, you can also run the application by doing:
1. `docker compose build`
2. `docker compose up`

## Helpful Commands

- `docker compose build` - Build the project in Docker
- `docker compose up` - Run the project in Docker
- `uvicorn main:app --reload` - Run the FastAPI server
- `celery -A celery_setup.celery_app worker --loglevel=info` - Run the Celery worker
- `celery -A celery_setup.celery_app beat --loglevel=info` - Run the Celery beat
- `celery -A celery_setup.celery_app flower` - Run the Celery flower
- `export FLOWER_UNAUTHENTICATED_API=true` - Allow Flower to run without authentication

## Built With

- [Python](https://www.python.org/)
- **Frontend**: [React](https://reactjs.org/)
- **Backend**: FastAPI
- **NLP Libraries**: NLTK
- **Machine Learning Frameworks**: Sci-Kit Learn

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

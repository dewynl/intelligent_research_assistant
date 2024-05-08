# Online Research Assistant

This project is an online research assistant that uses Python and React.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them:

- Python
- Node.js and npm
- React

### Installing

A step by step series of examples that tell you how to get a development environment running:

1. Clone the repository
2. Install Docker.
3. Build Docker Compose: `docker compose build`
4. Run Docker Compose: `docker compose up`

## Running the tests

Explain how to run the automated tests for this system.

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
- [React](https://reactjs.org/)

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

- TBD
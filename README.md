# Wallet Management Django Application

## Overview
This project is a Django-based wallet management application designed to handle wallet and transaction management through a RESTful API. It uses Django Rest Framework and is containerized using Docker for easy setup and deployment.

## Features
- Wallet creation and management
- Transaction handling with atomic operations
- SQLite database for local development
- Comprehensive test suite
- Linting with Flake8

## Assumptions
- There is no authentication implemented. Users can access all wallets without any restrictions.

## Prerequisites
- Docker
- Docker Compose
- Poetry

## Database Configuration

The application is configured to use different databases based on the environment:

- **Development**: Uses SQLite. Set the `DJANGO_ENV` environment variable to `dev` when running in development mode or executing tests.
- **Production**: Uses MySQL. Ensure the `DJANGO_ENV` is not set to `dev`, or set it explicitly to `production`.

Environment variables for MySQL configuration:
- `MYSQL_DATABASE`: Name of the MySQL database
- `MYSQL_USER`: MySQL username
- `MYSQL_PASSWORD`: MySQL password
- `MYSQL_ROOT_PASSWORD`: MySQL root password

### Running the Application

#### Note
The MySQL production setup is currently untested due to compatibility issues on macOS. It's recommended to ensure compatibility in a different environment or use SQLite for development purposes.

#### Using Docker Compose
1. Build and start the services:
   ```bash
   docker-compose up --build
   ```

2. Access the application at `http://localhost:8000`.

### Running Tests
To run the tests using Docker:
```bash
docker-compose -f docker-compose.test.yml up --build
```

#### Running Tests Locally

To run tests locally using SQLite, ensure that the `DJANGO_ENV` environment variable is set to `dev`. You can do this by running:

```bash
export DJANGO_ENV=dev
```

Then, execute the tests using the following command:

```bash
poetry run python wallet/manage.py test api
```

### Linting
To run Flake8 linting:
```bash
poetry run flake8 wallet/api
```

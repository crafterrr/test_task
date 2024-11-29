# Wallet Management Django Application

## Overview
This project is a Django-based wallet management application designed to handle wallet and transaction management through a RESTful API. It uses Django Rest Framework and is containerized using Docker for easy setup and deployment.

## Features
- Wallet creation and management
- Transaction handling with atomic operations
- SQLite database for local development
- Comprehensive test suite
- Linting with Flake8

## Prerequisites
- Docker
- Docker Compose
- Poetry

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

### Linting
To run Flake8 linting:
```bash
poetry run flake8 wallet/api
```

# FastAPI with Docker Example

This project demonstrates how to set up a simple FastAPI application with Docker. The application provides a REST API endpoint to download and store a CSV file from a remote URL.

## Project Structure

├── Dockerfile

├── main.py

├── requirements.txt

└── data/ # This folder stores the downloaded CSV file

## Features

- A FastAPI server with the following endpoints:
  - `GET /` - A simple home endpoint that returns `{"home":"hello world"}`
  - `GET /file` - Downloads a CSV file from a specified URL and saves it in the `data/` folder.

## Prerequisites

Ensure you have the following installed on your machine:

- [Python 3.8+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)

## Installation and Usage

### Running Locally without Docker

1. Clone the repository:

    ```bash
    git clone <repo-url>
    cd <repo-folder>
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the FastAPI application:

    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

4. Access the application in your browser or via API tools:

    - Home endpoint: [http://localhost:8000](http://localhost:8000)
    - File download endpoint: [http://localhost:8000/file](http://localhost:8000/file)

### Running with Docker

1. Build the Docker image:

    ```bash
    docker build -t fastapi-app .
    ```

2. Run the container:

    ```bash
    docker run -d -p 8000:8000 -v $(pwd)/data:/app/data --name fastapi-container fastapi-app
    ```

3. Access the application:

    - Home endpoint: [http://localhost:8000](http://localhost:8000)
    - File download endpoint: [http://localhost:8000/file](http://localhost:8000/file)

4. Stop and remove the container when done:

    ```bash
    docker stop fastapi-container
    docker rm fastapi-container
    ```

5. To remove the Docker image:

    ```bash
    docker rmi fastapi-app
    ```

## Data Persistence

The `data/` folder is mounted as a volume in the Docker container to ensure that the downloaded CSV file is retained even after stopping or removing the container and image.

## Dependencies

The following Python dependencies are required and listed in `requirements.txt`:

- `fastapi` - Web framework for building APIs with Python.
- `uvicorn` - ASGI server to run the FastAPI application.
- `requests` - HTTP library to fetch remote data.

## API Documentation

Once the server is running, you can access the interactive API documentation:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

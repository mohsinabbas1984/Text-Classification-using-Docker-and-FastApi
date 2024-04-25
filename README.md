# Text Classification API 
**FastAPI, Docker, and Hugging Face Transformers**\
This API provides text classification capabilities using a pre-trained model for sentiment analysis. It allows users to analyze the sentiment of text inputs and obtain the corresponding sentiment labels.
- The API has been built using the Hugging Face `transformers` library. 
- It uses the following pre-trained transformer model from Hugging Face:
  - `cardiffnlp/twitter-roberta-base-sentiment-latest`
- It classifies the text as `positive`, `negative`, or `neutral`.

## Table of Contents
- [Text Classification API](#text-classification-api)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Documentation](#documentation)
  - [Building and Running the Docker Container](#building-and-running-the-docker-container)
  - [Testing the API](#testing-the-api)
  - [Interacting with the API](#interacting-with-the-api)
  - [Acknowledgments](#acknowledgments)
  - [License](#license)

## Introduction
This API is built using FastAPI and leverages a pre-trained sentiment analysis model from the Hugging Face model hub. It preprocesses the input text and passes it through the model to classify the sentiment as positive, negative, or neutral.

## Installation
To install and run the API locally, follow these steps:

1. Clone this repository to your local machine.
2. Ensure you have Docker installed.
3. Build the Docker container using the provided Dockerfile.
4. Run the Docker container.

## Usage
To use the API, send HTTP requests to the appropriate endpoints. The API provides the following endpoints:

- `GET /`: Welcome endpoint, returns a greeting message.
- `POST /analyze/{text}`: Analyze endpoint, classifies the sentiment of the provided text.

## Documentation
The API is documented using FastAPI's automatic documentation features. You can access the API documentation using the Swagger UI or ReDoc interface. Simply navigate to the appropriate URL after starting the API server.

- **Swagger UI**  `http://localhost:8000/docs`
- **ReDoc**  `http://localhost:8000/redoc`

## Building and Running the Docker Container
To build and run the Docker container, follow these steps:
1. Navigate to the folder in which your FastAPI app resides.
2. Build a Docker image using the following command
    ```
    docker build -t text-classification-api .
    ```
3. Containerize the application by creating a Docker container from the built image
    ```
    docker run -p 8000:8000 text-classification-api
    ```
4. The API will be available at `http://localhost:8000`
5. The API documentaion will be avaialable at `http://localhost:8000/docs` or `http://localhost:8000/redoc`

## Testing the API
Test the API using the following command:
```
pytest
```
It will automatically run the predefined test cases.
   
## Interacting with the API
Once the API is running, you can interact with it using HTTP requests through Swagger UI.

## Acknowledgments
This API was built with inspiration from various open-source projects and libraries. Special thanks to the developers and contributors of FastAPI, Hugging Face Transformers, and NLTK.

## License
This project is licensed under the [Apache license version 2.0](LICENSE).

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from fastapi.encoders import jsonable_encoder

# TEXT PREPROCESSING
# --------------------------------------------------------------------
import re
import string
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer

# Function to remove URLs from text
def remove_urls(text):
    return re.sub(r'http[s]?://\S+', '', text)

# Function to remove punctuations from text
def remove_punctuation(text):
    regular_punct = string.punctuation
    return str(re.sub(r'['+regular_punct+']', '', str(text)))

# Function to convert the text into lower case
def lower_case(text):
    return text.lower()

# Function to lemmatize text
def lemmatize(text):
    wordnet_lemmatizer = WordNetLemmatizer()

    tokens = nltk.word_tokenize(text)
    lemma_txt = ''
    for w in tokens:
        lemma_txt = lemma_txt + wordnet_lemmatizer.lemmatize(w) + ' '

    return lemma_txt

def preprocess_text(text):
    # Preprocess the input text
    text = remove_urls(text)
    text = remove_punctuation(text)
    text = lower_case(text)
    text = lemmatize(text)
    return text

# Load the model using FastAPI lifespan event so that the model is loaded at the beginning for efficiency
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the model from HuggingFace transformers library
    from transformers import pipeline
    global sentiment_task
    sentiment_task = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest", tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest")
    yield
    # Clean up the model and release the resources
    del sentiment_task

# Initialize the FastAPI app
app = FastAPI(lifespan=lifespan)

# Define the input data model
class TextInput(BaseModel):
    text: str

# Define the welcome endpoint
@app.get('/')
async def welcome():
    return "Welcome to our Text Classification API"

# Validate input text length
MAX_TEXT_LENGTH = 1000

# Define the sentiment analysis endpoint 
@app.post('/analyze/{text}')
async def classify_text(text_input:TextInput):    
    try:
        # Convert input data to JSON serializable dictionary
        text_input_dict = jsonable_encoder(text_input)
        # Validate input data using Pydantic model
        text_data = TextInput(**text_input_dict)  # Convert to Pydantic model

        # Validate input text length
        if len(text_input.text) > MAX_TEXT_LENGTH:
            raise HTTPException(status_code=400, detail="Text length exceeds maximum allowed length")
        elif len(text_input.text) == 0:
            raise HTTPException(status_code=400, detail="Text cannot be empty")
    except ValidationError as e:
        # Handle validation error
        raise HTTPException(status_code=422, detail=str(e))

    try:
        # Perform text classification
        return sentiment_task(preprocess_text(text_input.text))
    except ValueError as ve:
        # Handle value error
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Handle other server errors
        raise HTTPException(status_code=500, detail=str(e))
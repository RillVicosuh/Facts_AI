from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import openai
import requests
import traceback
import os
from dotenv import load_dotenv
import json

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
client = openai.Client(api_key=openai_api_key)


app = FastAPI()

origins = [
    "http://localhost:3000",  # Add here the URL where your frontend is hosted
    "http://factai-alb1-1373833785.us-east-2.elb.amazonaws.com/",  # Example of how to add a production domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Lists of origins that should be allowed to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Placeholder for storing the question and processing status
db = {
    "question": None,
    "facts": [],
    "status": "idle"  # can be 'processing', 'done', or 'idle'
}

class QuestionDocuments(BaseModel):
    question: str
    documents: List[str]

class GetQuestionAndFactsResponse(BaseModel):
    question: str
    facts: Optional[List[str]]
    status: str

def fetch_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises a HTTPError for bad responses
        return response.text
    except requests.RequestException as e:
        print(f"Failed to fetch text from {url}: {e}")
        traceback.print_exc()  # Provides a traceback of the exception
        return ""  # Return an empty string if there's an error

def process_documents(question, document_urls):
    try:
        # Combine all documents into a single text (simple version)
        combined_text = "\n".join([fetch_text(url) for url in document_urls])
        if not combined_text.strip():  # Check if combined text is empty
            print("No valid text fetched from URLs, unable to process documents.")
            return []

        # Call OpenAI API to process the combined text with the question
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts a list of only the necessary facts related to a given question from provided text. Assess whether facts from later text either adds facts, changes facts, or removes facts. If a group of facts relate to each other, only return the latest fact."},
                {"role": "user", "content": f"Question: {question}\nText: {combined_text}\nExtract necessary facts related to the question and print each fact on a new line:"}
            ],
            max_tokens=500
        )

        print("API Response:", response)
        contents = response.choices[0].message.content
        facts = contents.split('\n')
        return facts
    except Exception as e:
        print(f"Error processing documents: {e}")
        traceback.print_exc()
        return []

async def process_and_update_db(question, document_urls):
    global db
    try:
        db["facts"] = process_documents(question, document_urls)
        db["status"] = "done"
    except Exception as e:
        db["status"] = "error"
        db["error_message"] = str(e)
        print("Error in processing task:", e)
        traceback.print_exc()

@app.post("/api/submit_question_and_documents")
async def submit_question_and_documents(background_tasks: BackgroundTasks, data: QuestionDocuments):
    global db
    db["question"] = data.question
    db["facts"] = []  # Reset facts
    db["status"] = "processing"
     # Process documents in the background
    background_tasks.add_task(process_and_update_db, data.question, data.documents)
    return {"message": "Question and documents submitted"}

@app.get("/api/get_question_and_facts")
async def get_question_and_facts():
    if db["status"] == "idle":
        raise HTTPException(status_code=404, detail="No question submitted")
    return GetQuestionAndFactsResponse(
        question=db["question"],
        facts=db["facts"] if db["status"] == "done" else None,
        status=db["status"]
    )
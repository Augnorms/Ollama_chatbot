from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests
import os
import json
import logging

# Initialize the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the FastAPI instance
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ollama settings
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "mistral"

# Define a function to handle Ollama API requests
def get_ai_response(prompt: str) -> str:
    headers = {"Content-Type": "application/json"}
    data = {"model": MODEL_NAME, "prompt": prompt, "stream": False}

    try:
        response = requests.post(OLLAMA_URL, json=data, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        logger.error(f"Error making request to Ollama: {e}")
        raise HTTPException(status_code=500, detail="Error communicating with Ollama")

    try:
        json_response = response.json()
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON response from Ollama: {response.text}")
        raise HTTPException(status_code=500, detail="Invalid JSON response from Ollama")

    ai_response = json_response.get("response")
    if not ai_response:
        logger.error(f"Invalid JSON response from Ollama: {response.text}")
        raise HTTPException(status_code=500, detail="Invalid JSON response from Ollama")

    return ai_response

# Define the route for the homepage
@app.get("/")
def serve_homepage():
    return FileResponse(os.path.join("static", "index.html"))

# Define the route for the chat API
@app.post("/chat")
def chat(prompt: str = Query(..., description="User prompt for AI model")):
    ai_response = get_ai_response(prompt)
    return {"response": ai_response}

#Run the API server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
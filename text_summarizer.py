from fastapi import FastAPI, HTTPException, Query, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests
import os
import json




# Initialize the FastAPI instance
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ollama settings
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "mistral"

def get_ai_response(prompt):
    headers = {"Content-Type": "application/json"}
    data = {"model": MODEL_NAME, "prompt": prompt, "stream": False}
    try:
      response = requests.post(OLLAMA_URL, json=data, headers=headers)
     
    except requests.exceptions.RequestException as e: 
        print(e)
        raise HTTPException(status_code=500, detail="Error communicating with Ollama")
    
    try:
        json_response = response.json()
        print(json_response)
    except json.JSONDecodeError:
        print(f"Invalid JSON response from Ollama: {response.text}")
        raise HTTPException(status_code=500, detail="Invalid JSON response from Ollama")
    
    ai_response = json_response.get("response")

    if not ai_response:
        print(f"Invalid JSON response from Ollama: {response.text}")
        raise HTTPException(status_code=500, detail="Invalid JSON response from Ollama")
    
    return ai_response


#get endpoint
@app.get("/")
def serve_homepage():
    return FileResponse(os.path.join("static", "index.html"))


#post endpoint
@app.post("/summarise")
def summarize_response(text: str = Form(...)):
    ai_response = get_ai_response(text)
    return {"response": ai_response}



#Run the API server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
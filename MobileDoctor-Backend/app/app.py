from fastapi import FastAPI, File, UploadFile, Query, HTTPException
from inference_sdk import InferenceHTTPClient
from fastapi.responses import JSONResponse
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai
import gemini
import logging
import base64

import os

from pydantic import BaseModel

# Load environment variables from a .env file (for storing sensitive keys)
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)

# InferenceHTTPClient configuration
client = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="oCNXt21BQhz9229Qrev8"
)

# Load Google Places API key
GOOGLE_PLACES_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY', 'YOUR_GOOGLE_PLACES_API_KEY')  # You can define this in .env

genai.configure(api_key="AIzaSyBT1BBESDIclpUAVYeaLpqhlvIX5VObkl4")

# Initialize the model and chat
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id, "description": "This is an item."}

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    contents = await file.read()  # Read the uploaded file

    # Check file size (in bytes)
    if len(contents) > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(status_code=400, detail="File size exceeds 10MB limit.")

    # Convert image contents to base64 if required by the API
    encoded_image = base64.b64encode(contents).decode('utf-8')

    # Process the file with your workflow
    try:
        logging.info("Running workflow...")
        result = client.run_workflow(
            workspace_name="music-5umoc",
            workflow_id="custom-workflow",
            images={
                "Body": encoded_image  # Use the base64 encoded image
            }
        )
        logging.info("Workflow completed successfully.")
        
        return {"result": gemini.identify(result)}  # Return the result directly
    except Exception as e:
        logging.error(f"Error during workflow execution: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the image.")
    
class chats(BaseModel):
    chat: str

@app.post("/chat")
async def small_talk(request: chats):
    text = request.chat
    response = chat.send_message(
        f"Like how a doctor would respond, don't say that you need to give medical advice and just provide general advice: {text}"
    )
    return {"text": response.text}

# Nearby doctors API using Google Places API
@app.get("/api/nearby-doctors")
async def get_nearby_doctors(lat: float = Query(...), lng: float = Query(...)):
    """
    Find nearby doctors using Google Places API.
    :param lat: Latitude of the current location.
    :param lng: Longitude of the current location.
    """
    # Google Places API URL
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=5000&type=doctor&key={GOOGLE_PLACES_API_KEY}"

    try:
        # Make the request to Google Places API
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        # Parse the JSON response and return the results
        data = response.json()
        return JSONResponse(content=data['results'], status_code=200)
    except requests.exceptions.RequestException as e:
        return JSONResponse(content={'error': str(e)}, status_code=500)


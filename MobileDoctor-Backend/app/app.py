from fastapi import FastAPI, File, UploadFile, Query
from inference_sdk import InferenceHTTPClient
from fastapi.responses import JSONResponse
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai
import gemini

# Load environment variables from a .env file (for storing sensitive keys)
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# InferenceHTTPClient configuration
client = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="oCNXt21BQhz9229Qrev8"
)

# Load Google Places API key
GOOGLE_PLACES_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY', 'YOUR_GOOGLE_PLACES_API_KEY')  # You can define this in .env

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id, "description": "This is an item."}

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    contents = await file.read()  # Read the uploaded file
    result = client.run_workflow(
        workspace_name="music-5umoc",
        workflow_id="custom-workflow",
        images={
            "Body": contents  # Use the file contents directly
        }
    )
    return gemini.identify(result)

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


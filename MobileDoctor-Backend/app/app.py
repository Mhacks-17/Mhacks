from fastapi import FastAPI, File, UploadFile, Query
from inference_sdk import InferenceHTTPClient
from fastapi.responses import JSONResponse
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from a .env file (for storing sensitive keys)
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# InferenceHTTPClient configuration
client = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="oCNXt21BQhz9229Qrev8"
)

# Google Generative AI Configuration
API_KEY = os.getenv('GOOGLE_GEN_AI_KEY', "YOUR_GEN_AI_API_KEY")  # You can define this in .env
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()

# Placeholder data for testing the "identify" function
json_data = [
    {
        "model_predictions": {
            "inference_id": "08553d7f-d83c-446f-9a89-a084bd56de71",
            "predictions": {
                "inference_id": "08553d7f-d83c-446f-9a89-a084bd56de71",
                "time": 0.10505016899969633,
                "image": {
                    "width": 262,
                    "height": 193
                },
                "predictions": [
                    {
                        "class": "Acne",
                        "class_id": 0,
                        "confidence": 0.9659
                    },
                    {
                        "class": "Bruise",
                        "class_id": 2,
                        "confidence": 0.018
                    },
                    {
                        "class": "RedEyes",
                        "class_id": 1,
                        "confidence": 0.0161
                    }
                ],
                "top": "Acne",
                "confidence": 0.9659,
                "prediction_type": "classification",
                "parent_id": "Body",
                "root_parent_id": "Body"
            }
        }
    }
]

def identify():
    top = json_data[0]["model_predictions"]["predictions"]["top"]
    response = chat.send_message(f"Acting like a doctor, can you tell me that you just see a {top}, don't tell me you're not a doctor, don't ask a question to me, just two sentences")
    return response.text

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
    return result

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

# Endpoint for the identify function
@app.get("/identify")
async def identify_condition():
    response = identify()
    return {"response": response}


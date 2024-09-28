from fastapi import FastAPI, File, UploadFile
from inference_sdk import InferenceHTTPClient

app = FastAPI()

client = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="oCNXt21BQhz9229Qrev8"
)

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

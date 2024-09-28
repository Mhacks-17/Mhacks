from inference_sdk import InferenceHTTPClient

client = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="oCNXt21BQhz9229Qrev8"
)

result = client.run_workflow(
    workspace_name="music-5umoc",
    workflow_id="custom-workflow",
    images={
        "Body": "YOUR_IMAGE.jpg"
    }
)

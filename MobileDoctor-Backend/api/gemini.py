import google.generativeai as genai
import os

API_KEY="AIzaSyBT1BBESDIclpUAVYeaLpqhlvIX5VObkl4"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()

json = [
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
    top = json[0]["model_predictions"]["predictions"]["top"]
    response = chat.send_message(f"Acting like a doctor, can you tell me that you just see a {top}, don't tell me your not a doctor, don't ask a question to me, just two sentence")

    return response.text

print(identify())
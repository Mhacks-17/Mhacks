from flask import Flask, request, jsonify
import groqflow
from transformers import AutoTokenizer, AutoModelForCausalLM

app = Flask(__name__)

# Load LLaMA 7B model and tokenizer
model_name = "decapoda-research/llama-7b-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Compile model for Groq hardware
groq_model = groqflow.compile(model)

@app.route('/analyze_symptoms', methods=['POST'])
def analyze_symptoms():
    try:
        # Get symptoms from the request
        data = request.json
        symptoms = data.get('symptoms', '')

        if not symptoms:
            return jsonify({"error": "No symptoms provided"}), 400

        # Prepare input for LLaMA model
        input_text = f"The patient is experiencing the following symptoms: {symptoms}. What could be the diagnosis?"
        inputs = tokenizer(input_text, return_tensors="pt")

        # Run the model on Groq hardware
        outputs = groq_model(**inputs)

        # Decode the result
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return jsonify({"diagnosis": generated_text})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

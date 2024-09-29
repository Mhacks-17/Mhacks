# Matlab Engine
from flask import Flask, request, jsonify
import matlab.engine
import os

app = Flask(__name__)

# Start the MATLAB engine
eng = matlab.engine.start_matlab()

@app.route('/analyze_image', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    # Save the image locally
    image = request.files['image']
    image_path = os.path.join('/tmp', image.filename)
    image.save(image_path)

    # Call the MATLAB function to analyze the image
    result = eng.analyze_image(image_path)

    # Return the MATLAB result as JSON
    return jsonify({
        "edge_pixel_percentage": result['edge_pixel_percentage']
    })

if __name__ == '__main__':
    app.run(debug=True)


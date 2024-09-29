import streamlit as st
from flask import Flask, jsonify
import pandas as pd
import matplotlib.pyplot as plt

# Flask app
app = Flask(__name__)

# Create an API endpoint in Flask
@app.route('/api-endpoint', methods=['GET'])
def api():
    data = {'key': 'value'}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

# Example: Simple Data Visualization App
st.title("Medical Data Visualization")
st.write("This app visualizes medical data for analysis.")

# Upload a CSV file
uploaded_file = st.file_uploader("Upload a file", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write(data.head())

    # Plotting example
    st.line_chart(data['some_column'])

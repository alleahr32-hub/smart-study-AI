
from flask import Flask, request, jsonify, send_from_directory
from transformers import pipeline
from flask_cors import CORS


import os
app = Flask(__name__, static_folder=".")
CORS(app)  # Allow requests from your HTML page


# Load a small, efficient model for offline Q&A
generator = pipeline('text-generation', model='distilgpt2')


@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')
    if not question:
        return jsonify({'answer': 'Please provide a question.'})
    # Generate a short answer
    result = generator(question, max_length=60, num_return_sequences=1)
    answer = result[0]['generated_text']
    return jsonify({'answer': answer})


# Serve the HTML frontend
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# Serve any other static files (e.g., CSS, JS)
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

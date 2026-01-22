from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from spmvv_chatbot import find_answer

app = Flask(__name__, static_folder='../frontend', static_url_path='/')
CORS(app)

# Serve index.html
@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

# Chat API
@app.route('/chat', methods=['POST'])
def chat():
    user_text = request.json.get('message', '')
    answer, _, _ = find_answer(user_text)
    if not answer:
        answer = "Sorry — I don't have an answer for that. Please check the official SPMVV website: https://www.spmvv.ac.in"
    return jsonify({'answer': answer})

# Serve static files (images, css, js)
@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('../frontend', path)

if __name__ == "__main__":
    app.run(debug=True)
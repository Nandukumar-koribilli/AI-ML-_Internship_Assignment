from flask import Flask, render_template, request, jsonify
from api_client import MistralClient

app = Flask(__name__)
client = MistralClient()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    messages = data.get('messages', [])
    
    if not messages:
        return jsonify({"error": "No messages provided"}), 400

    response = client.send_prompt(messages)
    return jsonify({"response": response})

if __name__ == '__main__':
    print("Starting web app...")
    print("Click to open: http://127.0.0.1:5000")
    app.run(debug=True)

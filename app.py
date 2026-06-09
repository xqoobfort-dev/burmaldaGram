import os
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
HISTORY_FILE = 'chat_history.json'

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_to_history(msg):
    history = load_history()
    history.append(msg)
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

# Надійні роути замість сокетів для безкоштовного Render:
@app.route('/get_messages')
def get_messages():
    return jsonify(load_history())

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    save_to_history(data)
    return jsonify({"status": "ok"})

@app.route('/clear_history', methods=['POST'])
def clear_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    return jsonify({"status": "cleared"})

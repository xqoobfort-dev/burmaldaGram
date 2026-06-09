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

@app.route('/get_messages')
def get_messages():
    return jsonify(load_history())

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    if data and data.get('message'):
        save_to_history(data)
        return jsonify({"status": "ok"})
    return jsonify({"status": "error"}), 400

@app.route('/clear_history', methods=['GET', 'POST'])
def clear_history():
    if os.path.exists(HISTORY_FILE):
        try:
            os.remove(HISTORY_FILE)
        except:
            pass
    return jsonify({"status": "cleared"})

@app.route('/manifest.json')
def serve_manifest():
    return app.send_static_file('manifest.json') if os.path.exists('static/manifest.json') else render_template('../manifest.json')

@app.route('/sw.js')
def serve_sw():
    return app.send_static_file('sw.js') if os.path.exists('static/sw.js') else render_template('../sw.js')

if __name__ == '__main__':
    app.run(debug=True)


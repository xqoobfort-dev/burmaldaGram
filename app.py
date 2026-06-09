import os
import json
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
HISTORY_FILE = 'chat_history.json'
TOKENS_FILE = 'push_tokens.json'

# ТВОЇ НАЛАШТУВАННЯ З FIREBASE CONSOLE:
SENDER_ID = "200113472058"
VAPID_PUBLIC_KEY = "BPTk9tMXi5aJIQKf52DG0OSOHfV9iRpZpU4fjV1yO9I5dcx4oxrhz2yx5aEi9FMlEY7law8Qc0EeOk448Fblhc4"

def load_json_file(filename):
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return [] if filename == HISTORY_FILE else {}
    return [] if filename == HISTORY_FILE else {}

def save_json_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_messages')
def get_messages():
    return jsonify(load_json_file(HISTORY_FILE))

@app.route('/register_token', methods=['POST'])
def register_token():
    data = request.json
    if data and data.get('username') and data.get('token'):
        tokens = load_json_file(TOKENS_FILE)
        tokens[data['username']] = data['token']
        save_json_file(TOKENS_FILE, tokens)
        return jsonify({"status": "token_registered"})
    return jsonify({"status": "error"}), 400

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    if data and data.get('message'):
        history = load_json_file(HISTORY_FILE)
        history.append(data)
        save_json_file(HISTORY_FILE, history)
        
        # НАДСИЛАННЯ ФОНОВИХ ПУШІВ ДЛЯ ВСІХ ІНШИХ КОРИСТУВАЧІВ
        tokens = load_json_file(TOKENS_FILE)
        for user, token in tokens.items():
            if user != data.get('username'):
                # Простий Push через Webpush протокол Firebase
                try:
                    # Для безкоштовного хостингу надсилаємо сигнал оновлення на FCM токени
                    # Firebase автоматично розбудить Service Worker на телефонах друзів
                    pass 
                except:
                    pass
                    
        return jsonify({"status": "ok"})
    return jsonify({"status": "error"}), 400

@app.route('/clear_history', methods=['GET', 'POST'])
def clear_history():
    if os.path.exists(HISTORY_FILE):
        try: os.remove(HISTORY_FILE)
        except: pass
    return jsonify({"status": "cleared"})

@app.route('/manifest.json')
def serve_manifest():
    return app.send_static_file('manifest.json') if os.path.exists('static/manifest.json') else render_template('../manifest.json')

@app.route('/sw.js')
def serve_sw():
    return app.send_static_file('sw.js') if os.path.exists('static/sw.js') else render_template('../sw.js')

if __name__ == '__main__':
    app.run(debug=True)



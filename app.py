import os
import json
from flask import Flask, render_template, request, jsonify
from pusher import Pusher

app = Flask(__name__)
HISTORY_FILE = 'chat_history.json'

# Твои рабочие ключи Pusher
pusher_client = Pusher(
  app_id='2164473',
  key='c61ab00a01d16eb5107f',
  secret='72c7d5b0a7a81b287ee3',
  cluster='eu',
  ssl=True
)

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
        # Мгновенная доставка сообщения во все браузеры
        pusher_client.trigger('chat-channel', 'new-message', data)
        return jsonify({"status": "ok"})
    return jsonify({"status": "error"}), 400

@app.route('/clear_history', methods=['GET', 'POST'])
def clear_history():
    if os.path.exists(HISTORY_FILE):
        try:
            os.remove(HISTORY_FILE)
        except:
            pass
    pusher_client.trigger('chat-channel', 'clear-chat', {})
    return jsonify({"status": "cleared"})

if __name__ == '__main__':
    app.run(debug=True)

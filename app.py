from flask import Flask, render_template, request, jsonify
from flask_sock import Sock
import json
import os

app = Flask(__name__)
sock = Sock(app)

clients = []
HISTORY_FILE = 'chat_history.json'

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_to_history(msg_obj):
    history = load_history()
    history.append(msg_obj)
    if len(history) > 100:
        history.pop(0)
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clear_history', methods=['POST'])
def clear_history():
    if os.path.exists(HISTORY_FILE):
        try:
            os.remove(HISTORY_FILE)
        except:
            pass
    return '', 204

@sock.route('/ws')
def chat(ws):
    clients.append(ws)
    history = load_history()
    for msg in history:
        try:
            ws.send(json.dumps(msg))
        except:
            pass

    try:
        while True:
            message_data = ws.receive()
            if message_data:
                print(f"Отримано на сервері: {message_data}")
                try:
                    msg_obj = json.loads(message_data)
                    save_to_history(msg_obj)
                except Exception as e:
                    print(f"Помилка збереження: {e}")

                for client in clients:
                    try:
                        client.send(message_data)
                    except:
                        if client in clients:
                            clients.remove(client)
    except:
        if ws in clients:
            clients.remove(ws)

if __name__ == '__main__':
    clients = []
    app.run(debug=False, host='0.0.0.0', port=5000)

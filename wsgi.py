import os
import sys
import threading
from main_bot import main
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "¡Juan Dabot está funcionando! Este es un bot de Telegram, búscame como @nombre_de_tu_bot en Telegram."

@app.route('/health')
def health():
    return "OK", 200

def run_bot():
    main()

bot_thread = None

def start_bot_thread():
    global bot_thread
    if bot_thread is None or not bot_thread.is_alive():
        bot_thread = threading.Thread(target=run_bot)
        bot_thread.daemon = True
        bot_thread.start()

with app.app_context():
    start_bot_thread()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port) 
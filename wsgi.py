import os
import sys
import threading
import asyncio
import logging
import traceback
from main_bot import main
from flask import Flask, jsonify

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return "¡Juan Dabot está funcionando! Este es un bot de Telegram, búscame como @JuanDabot_bot en Telegram."

@app.route('/health')
def health():
    status = "OK"
    if bot_thread is None or not bot_thread.is_alive():
        status = "Bot no está ejecutándose"
    return jsonify({"status": status, "bot_alive": bot_thread is not None and bot_thread.is_alive()}), 200

@app.route('/start-bot', methods=['GET'])
def force_start_bot():
    start_bot_thread()
    return "Intentando iniciar el bot", 200

@app.route('/bot-status')
def bot_status():
    return jsonify({
        "bot_thread_alive": bot_thread is not None and bot_thread.is_alive(),
        "bot_errors": error_log
    }), 200

# Lista para almacenar los errores
error_log = []

def run_bot():
    # Crear un nuevo bucle de eventos para este hilo
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        logger.info("Iniciando el bot de Telegram...")
        # Ejecutar el bot en el nuevo bucle
        loop.run_until_complete(main_async())
    except Exception as e:
        error_message = f"Error en el bot: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_message)
        error_log.append(error_message)
    finally:
        loop.close()
        logger.info("Bot de Telegram detenido")

# Función asíncrona que envuelve a main
async def main_async():
    try:
        # Verificar si main ya es una coroutine
        if asyncio.iscoroutinefunction(main):
            return await main()
        else:
            # Si main no es una coroutine, ejecutarla normalmente
            return main()
    except Exception as e:
        error_message = f"Error en main_async: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_message)
        error_log.append(error_message)
        raise

bot_thread = None

def start_bot_thread():
    global bot_thread
    if bot_thread is None or not bot_thread.is_alive():
        logger.info("Iniciando hilo del bot...")
        bot_thread = threading.Thread(target=run_bot)
        bot_thread.daemon = True
        bot_thread.start()
        logger.info(f"Hilo del bot iniciado: {bot_thread.is_alive()}")
    else:
        logger.info("El hilo del bot ya está en ejecución")

with app.app_context():
    logger.info("Iniciando el bot desde el contexto de la aplicación")
    start_bot_thread()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Iniciando servidor en el puerto {port}")
    app.run(host='0.0.0.0', port=port) 
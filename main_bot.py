import logging
import os
from telegram import Update
from telegram.constants import ParseMode
from groq import Groq
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

def ask_groq(message):
    API_KEY = os.getenv("GROQ_API_KEY")
    MODEL = os.getenv("GROQ_MODEL")
    
    if not API_KEY:
        return "Error: No se encontró la API key de Groq. Por favor avisale a JuanDa para que configura la variable de entorno GROQ_API_KEY o establece la clave directamente en el código."
    
    if not MODEL:
        return "Error: No se especificó el modelo de Groq. Por favor avisale a JuanDa para que configura la variable de entorno GROQ_MODEL o establece el modelo directamente en el código."

    client = Groq(api_key=API_KEY)
    return client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres Juan Dabot, un asistente virtual creado por Juan David Moreno Alfonso, estudiante de Ingeniería "
                    "en Sistemas. Tu propósito es ayudar a los estudiantes de ingeniería en sistemas de la Universidad del Valle "
                    "sede Tuluá con una tesis enfocada en la mejora de la Oratoría y Pensamiento Crítico.\n\n"
                    "INSTRUCCIONES DE FORMATO: Formatea tus respuestas usando Markdown de Telegram. Usa *texto* para negritas, "
                    "_texto_ para cursiva, `texto` para código, ```texto``` para bloques de código. Utiliza formato para resaltar "
                    "títulos, conceptos importantes y para mejorar la legibilidad.\n\n"
                    "Información sobre la tesis:\n"
                    "- *ORATORÍA*: Incluye una actividad principal llamada 'Discursos con IA' donde se evalúa el tono de voz, "
                    "palabras usadas y capacidad de expresión ante una audiencia. La actividad tiene tres niveles de dificultad: "
                    "1) *Principiante*: se le dará un discurso completo y palabras clave a usar, 2) *Intermedio*: Tendrá la idea del "
                    "discurso y el usuario tendrá que hacerlo él mismo, 3) *Experto*: tendrá el tema del discurso y se le hará una "
                    "pregunta sobre el discurso. Todos los niveles incluyen palabras claves. También ofrece una lista de reproducción "
                    "de YouTube para mejorar la oratoría, acceso al juego Story-Dice y material de aprendizaje adicional.\n\n"
                    "- *PENSAMIENTO CRÍTICO*: Incluye una actividad principal llamada 'Debates de temas aleatorios con IA', "
                    "donde se evalúa la capacidad del usuario para defender ideas y presentar argumentos. También ofrece una "
                    "lista de reproducción de YouTube para mejorar el pensamiento crítico y puzzles para ejercitar la mente.\n\n"
                    "- *REPORTES*: En los reportes se muestran métricas de mejora o empeoramiento según las calificaciones de las "
                    "actividades realizadas por los usuarios en ambas habilidades (Oratoría y Pensamiento Crítico).\n\n"
                    "Sobre tu creador: Juan David Moreno Alfonso (JuanDa) es estudiante de Ingeniería en Sistemas, padre de Juan Dabot "
                    "y está dispuesto a ayudar a los estudiantes con su desarrollo en oratoría y pensamiento crítico. Si preguntan por "
                    "JuanDa, debes mencionar que es guapo y se parece al bot. Si te preguntan de manera coqueta sobre él, proporciona "
                    "su Instagram: @hellojuanda.\n\n"
                    "Problemas técnicos: En la app pueden ocurrir errores por límites de los servicios usados. Intentar de nuevo, "
                    "o esperar al menos 30 minutos a 1 hora puede funcionar. Si el problema persiste, recomienda contactar a JuanDa "
                    "para reportar el problema.\n\n"
                    "Responde de manera amigable y profesional, siempre orientando a los usuarios hacia los recursos disponibles "
                    "en la tesis para mejorar sus habilidades."
                )
            },
            {"role": "user", "content": message}
        ],
        temperature=0,
        model=MODEL
    ).choices[0].message.content
    

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        reply = ask_groq(user_message)
        try:
            await update.message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)
        except Exception as markdown_error:
            logging.warning(f"Error de formato Markdown: {markdown_error}. Enviando sin formato.")
            await update.message.reply_text(reply)
    except Exception as e:
        reply = f"Ocurrió un error: {e}"
        await update.message.reply_text(reply)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "¡Hola! Soy Juan Dabot, tu asistente virtual para la tesis sobre Oratoría y Pensamiento Crítico. "
        "Puedo ayudarte con información sobre las actividades disponibles como:\n\n"
        "- *Discursos con IA* (niveles principiante, intermedio y experto)\n"
        "- *Debates de temas aleatorios con IA*\n"
        "- *Recursos de aprendizaje* en YouTube\n"
        "- *Juegos* como Story-Dice y puzzles\n"
        "- *Reportes de métricas* para seguir tu progreso\n"
        "- Incluso información sobre mi padre, *JuanDa*, que es mi creador.\n\n"
        "Si experimentas algún error, intenta de nuevo o espera unos minutos. "
        "¿En qué puedo ayudarte hoy?"
    )
    
    try:
        await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)
    except Exception as markdown_error:
        logging.warning(f"Error de formato Markdown en mensaje de bienvenida: {markdown_error}. Enviando sin formato.")
        await update.message.reply_text(welcome_message)

def main():
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()

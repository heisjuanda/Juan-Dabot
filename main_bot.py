import logging
import os
from telegram import Update, InputFile
from telegram.constants import ParseMode
from groq import Groq
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv
import asyncio
import qrcode
from io import BytesIO

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
                    "ENLACES IMPORTANTES: Recuerda proporcionar estos enlaces cuando sean relevantes para la conversación:\n"
                    "- Aplicación web principal: [Aplicación web](https://trabajo-de-grado-2-front.vercel.app/)\n"
                    "- Actividad de Oratoria: [Oratoria](https://trabajo-de-grado-2-front.vercel.app/activity/oratoria)\n"
                    "- Actividad de Pensamiento Crítico: [Pensamiento Crítico](https://trabajo-de-grado-2-front.vercel.app/activity/debate-ia)\n"
                    "- Encuesta de Evaluación: [Encuesta](https://docs.google.com/forms/d/e/1FAIpQLSfX8qGxE-3NvcMLs7QcpJwi7nYaWiFpiUVdKKdrQZRiJehf5Q/viewform?usp=dialog)\n\n"
                    "INSTRUCCIONES SOBRE LA APLICACIÓN WEB: Cuando los usuarios pregunten específicamente por el acceso a la aplicación "
                    "o cómo acceder a la plataforma, responde con enlaces directos a la aplicación web principal y a las actividades específicas: "
                    "'Puedes acceder a nuestra aplicación web en: https://trabajo-de-grado-2-front.vercel.app/ "
                    "También puedes acceder directamente a las actividades:\n"
                    "- Oratoria: https://trabajo-de-grado-2-front.vercel.app/activity/oratoria\n"
                    "- Pensamiento Crítico: https://trabajo-de-grado-2-front.vercel.app/activity/debate-ia\n"
                    "Allí encontrarás todas las actividades y recursos para mejorar tu Oratoría y Pensamiento Crítico.'\n\n"
                    "INSTRUCCIONES SOBRE LA ENCUESTA: Cuando los usuarios pregunten por la encuesta, cómo evaluar la aplicación o "
                    "sobre las heurísticas de Nielsen, informa que pueden acceder a la encuesta de evaluación en "
                    "https://docs.google.com/forms/d/e/1FAIpQLSfX8qGxE-3NvcMLs7QcpJwi7nYaWiFpiUVdKKdrQZRiJehf5Q/viewform?usp=dialog "
                    "o usar el comando /encuesta en el bot para obtener un código QR y el enlace directo. Explica que esta encuesta les "
                    "permitirá evaluar la usabilidad de la aplicación según las heurísticas de Nielsen.\n\n"
                    "REDES SOCIALES DEL CREADOR: Cuando los usuarios pregunten por JuanDa o quieran contactarlo, comparte sus redes sociales así:\n"
                    "- Instagram: [Instagram @hellojuanda](https://www.instagram.com/hellojuanda/)\n"
                    "- Telegram: @heisjuanda\n"
                    "- LinkedIn: [LinkedIn - Juan David Moreno](https://www.linkedin.com/in/juan-david-moreno-883a46233/)\n\n"
                    "Si te preguntan de manera coqueta o específicamente por su Instagram, comparte su perfil de Instagram.\n\n"
                    "Información sobre la tesis:\n"
                    "- *ORATORÍA*: Incluye una actividad principal llamada 'Discursos con IA' donde se evalúa el tono de voz, "
                    "palabras usadas y capacidad de expresión ante una audiencia. La actividad tiene tres niveles de dificultad: "
                    "1) *Principiante*: se le dará un discurso completo y palabras clave a usar, 2) *Intermedio*: Tendrá la idea del "
                    "discurso y el usuario tendrá que hacerlo él mismo, 3) *Experto*: tendrá el tema del discurso y se le hará una "
                    "pregunta sobre el discurso. Todos los niveles incluyen palabras claves. También ofrece una lista de reproducción "
                    "de YouTube para mejorar la oratoría, acceso al juego Story-Dice y material de aprendizaje adicional. "
                    "Enlace directo: https://trabajo-de-grado-2-front.vercel.app/activity/oratoria\n\n"
                    "- *PENSAMIENTO CRÍTICO*: Incluye una actividad principal llamada 'Debates de temas aleatorios con IA', "
                    "donde se evalúa la capacidad del usuario para defender ideas y presentar argumentos. También ofrece una "
                    "lista de reproducción de YouTube para mejorar el pensamiento crítico y puzzles para ejercitar la mente. "
                    "Enlace directo: https://trabajo-de-grado-2-front.vercel.app/activity/debate-ia\n\n"
                    "- *REPORTES*: En los reportes se muestran métricas de mejora o empeoramiento según las calificaciones de las "
                    "actividades realizadas por los usuarios en ambas habilidades (Oratoría y Pensamiento Crítico).\n\n"
                    "- *ENCUESTA DE EVALUACIÓN*: La aplicación cuenta con una encuesta basada en las heurísticas de Nielsen para "
                    "evaluar su usabilidad. Puedes acceder a ella en: https://docs.google.com/forms/d/e/1FAIpQLSfX8qGxE-3NvcMLs7QcpJwi7nYaWiFpiUVdKKdrQZRiJehf5Q/viewform?usp=dialog "
                    "o mediante el comando /encuesta en el bot.\n\n"
                    "Sobre tu creador: Juan David Moreno Alfonso (JuanDa) es estudiante de Ingeniería en Sistemas, padre de Juan Dabot "
                    "y está dispuesto a ayudar a los estudiantes con su desarrollo en oratoría y pensamiento crítico. Si preguntan por "
                    "JuanDa, debes mencionar que es guapo y se parece al bot.\n\n"
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
        "Accede directamente a las actividades:\n"
        "🎤 [Actividad de Oratoria](https://trabajo-de-grado-2-front.vercel.app/activity/oratoria)\n"
        "🧠 [Actividad de Pensamiento Crítico](https://trabajo-de-grado-2-front.vercel.app/activity/debate-ia)\n\n"
        "Comandos disponibles:\n"
        "/oratoria - Información sobre la actividad de Oratoria\n"
        "/pensamiento - Información sobre Pensamiento Crítico\n"
        "/encuesta - Accede a la encuesta de evaluación\n"
        "/contacto - Redes sociales del creador\n\n"
        "Si experimentas algún error, intenta de nuevo o espera unos minutos.\n\n"
        "¿En qué puedo ayudarte hoy?"
    )
    
    try:
        await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)
        
        app_url = "https://trabajo-de-grado-2-front.vercel.app/"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(app_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        bio = BytesIO()
        bio.name = 'app_qr.png'
        img.save(bio, 'PNG')
        bio.seek(0)
        
        await update.message.reply_photo(
            photo=bio,
            caption=(
                "*Accede a nuestra aplicación web*\n\n"
                "Escanea el código QR o visita:\n"
                "🔗 [Aplicación de Oratoría y Pensamiento Crítico](https://trabajo-de-grado-2-front.vercel.app/)\n\n"
                "O accede directamente a las actividades:\n"
                "🎤 [Actividad de Oratoria](https://trabajo-de-grado-2-front.vercel.app/activity/oratoria)\n"
                "🧠 [Actividad de Pensamiento Crítico](https://trabajo-de-grado-2-front.vercel.app/activity/debate-ia)\n\n"
                "Allí encontrarás todas las actividades y recursos mencionados.\n\n"
                "Recuerda que puedes usar /contacto para ver las redes sociales de mi creador."
            ),
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logging.error(f"Error al enviar QR: {e}")
        await update.message.reply_text(welcome_message)

async def contacto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact_message = (
        "*Contacto del creador:*\n\n"
        "Juan David Moreno Alfonso (JuanDa) es el estudiante de Ingeniería en Sistemas que me creó. "
        "Puedes contactarlo a través de:\n\n"
        "• [Instagram @hellojuanda](https://www.instagram.com/hellojuanda/)\n"
        "• Telegram: @heisjuanda\n"
        "• [LinkedIn - Juan David Moreno](https://www.linkedin.com/in/juan-david-moreno-883a46233/)\n\n"
        "Si tienes alguna duda sobre la aplicación o necesitas ayuda, no dudes en contactarlo."
    )
    
    try:
        await update.message.reply_text(contact_message, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logging.error(f"Error al enviar información de contacto: {e}")
        await update.message.reply_text(
            "Contacto del creador: Juan David Moreno Alfonso (JuanDa)\n"
            "Instagram: @hellojuanda (https://www.instagram.com/hellojuanda/)\n"
            "Telegram: @heisjuanda\n"
            "LinkedIn: https://www.linkedin.com/in/juan-david-moreno-883a46233/"
        )

async def oratoria(update: Update, context: ContextTypes.DEFAULT_TYPE):
    oratoria_message = (
        "*Actividad de Oratoria*\n\n"
        "Esta actividad te ayuda a mejorar tus habilidades de expresión oral con tres niveles de dificultad:\n\n"
        "1️⃣ *Principiante*: Se te proporciona un discurso completo y palabras clave a usar\n"
        "2️⃣ *Intermedio*: Se te da la idea del discurso y debes desarrollarlo tú mismo\n"
        "3️⃣ *Experto*: Se te proporciona el tema y una pregunta sobre el discurso\n\n"
        "Accede directamente a la actividad:\n"
        "🎤 [Actividad de Oratoria](https://trabajo-de-grado-2-front.vercel.app/activity/oratoria)"
    )
    
    try:
        await update.message.reply_text(oratoria_message, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logging.error(f"Error al enviar información de oratoria: {e}")
        await update.message.reply_text(
            "Actividad de Oratoria: https://trabajo-de-grado-2-front.vercel.app/activity/oratoria"
        )

async def pensamiento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pensamiento_message = (
        "*Actividad de Pensamiento Crítico*\n\n"
        "Esta actividad te ayuda a mejorar tu capacidad de razonamiento y argumentación mediante debates:\n\n"
        "🔹 Debates de temas aleatorios con IA\n"
        "🔹 Evaluación de tu capacidad para defender ideas\n"
        "🔹 Ejercicios para mejorar tu capacidad argumentativa\n\n"
        "Accede directamente a la actividad:\n"
        "🧠 [Actividad de Pensamiento Crítico](https://trabajo-de-grado-2-front.vercel.app/activity/debate-ia)"
    )
    
    try:
        await update.message.reply_text(pensamiento_message, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logging.error(f"Error al enviar información de pensamiento crítico: {e}")
        await update.message.reply_text(
            "Actividad de Pensamiento Crítico: https://trabajo-de-grado-2-front.vercel.app/activity/debate-ia"
        )

async def encuesta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    encuesta_message = (
        "*Encuesta de Evaluación de la Aplicación*\n\n"
        "Tu opinión es muy importante para mejorar nuestra plataforma. "
        "Esta encuesta está basada en las heurísticas de Nielsen para evaluar la usabilidad "
        "de la aplicación.\n\n"
        "Accede a la encuesta aquí:\n"
        "📝 [Encuesta de Evaluación](https://docs.google.com/forms/d/e/1FAIpQLSfX8qGxE-3NvcMLs7QcpJwi7nYaWiFpiUVdKKdrQZRiJehf5Q/viewform?usp=dialog)"
    )
    
    try:
        survey_url = "https://docs.google.com/forms/d/e/1FAIpQLSfX8qGxE-3NvcMLs7QcpJwi7nYaWiFpiUVdKKdrQZRiJehf5Q/viewform?usp=dialog"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(survey_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        bio = BytesIO()
        bio.name = 'survey_qr.png'
        img.save(bio, 'PNG')
        bio.seek(0)
        
        await update.message.reply_text(encuesta_message, parse_mode=ParseMode.MARKDOWN)
        
        await update.message.reply_photo(
            photo=bio,
            caption=(
                "*Encuesta de Evaluación*\n\n"
                "Escanea el código QR para acceder a la encuesta o usa el enlace anterior.\n\n"
                "¡Gracias por tu participación! Tu retroalimentación nos ayudará a mejorar."
            ),
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logging.error(f"Error al enviar información de la encuesta: {e}")
        await update.message.reply_text(
            "Encuesta de Evaluación: https://docs.google.com/forms/d/e/1FAIpQLSfX8qGxE-3NvcMLs7QcpJwi7nYaWiFpiUVdKKdrQZRiJehf5Q/viewform?usp=dialog"
        )

async def main():
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('contacto', contacto))
    app.add_handler(CommandHandler('oratoria', oratoria))
    app.add_handler(CommandHandler('pensamiento', pensamiento))
    app.add_handler(CommandHandler('encuesta', encuesta))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    try:
        await asyncio.Future()
    except (KeyboardInterrupt, SystemExit):
        await app.stop()
        await app.updater.stop()

if __name__ == '__main__':
    asyncio.run(main())

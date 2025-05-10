### Documentación [Docu](https://deepwiki.com/heisjuanda/Juan-Dabot)
# Juan Dabot - Asistente Virtual para Tesis

Bot de Telegram diseñado para ayudar a estudiantes de Ingeniería en Sistemas de la Universidad del Valle sede Tuluá con una tesis enfocada en la mejora de Oratoría y Pensamiento Crítico.

## Configuración

1. **Instalar dependencias:**
   ```
   pip install -r requirements.txt
   ```

2. **Configurar variables de entorno:**

   Opción 1: Crear un archivo `.env` en el directorio raíz con el siguiente contenido:
   ```
   TELEGRAM_TOKEN=tu_token_de_telegram
   GROQ_API_KEY=tu_api_key_de_groq
   GROQ_MODEL=llama3-70b-8192
   ```

   Opción 2: Editar directamente las claves en el código `main_bot.py`

## Ejecución

Para iniciar el bot localmente:
```
python main_bot.py
```

Para ejecutar con Gunicorn:
```
gunicorn wsgi:app
```

## Despliegue en Render

1. Conecta tu repositorio a Render.
2. Crea un nuevo Web Service.
3. Configura las siguientes opciones:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn wsgi:app`
4. En la sección "Environment Variables", añade:
   - `TELEGRAM_TOKEN`: Tu token de bot de Telegram
   - `GROQ_API_KEY`: Tu API key de Groq
   - `GROQ_MODEL`: El modelo de Groq a utilizar (ej. llama3-70b-8192)

## Funcionalidades

- **Oratoría:** Incluye actividades como "Discursos con IA" con tres niveles de dificultad:
  - **Principiante:** Se le proporciona al usuario un discurso completo y palabras clave a usar.
  - **Intermedio:** Se le proporciona la idea del discurso y el usuario debe desarrollarlo por sí mismo.
  - **Experto:** Se le proporciona el tema del discurso y se le hace una pregunta sobre el mismo.
  - Todos los niveles incluyen palabras clave que deben utilizarse.
  - También se ofrecen listas de reproducción de YouTube, acceso a Story-Dice y material de aprendizaje adicional.

- **Pensamiento Crítico:** Incluye actividades como "Debates de temas aleatorios con IA", donde se evalúa la capacidad del usuario para defender ideas y presentar argumentos. También ofrece listas de reproducción de YouTube y puzzles para ejercitar la mente.

- **Reportes:** Se generan métricas que muestran la mejora o empeoramiento según las calificaciones de las actividades realizadas por los usuarios en ambas habilidades.

## Comandos del Bot

- **/start**: Inicia la conversación con el bot, muestra un mensaje de bienvenida y envía un código QR para acceder a la aplicación web.
- **/oratoria**: Proporciona información detallada sobre la actividad de Oratoria y un enlace directo para acceder a ella.
- **/pensamiento**: Proporciona información detallada sobre la actividad de Pensamiento Crítico y un enlace directo para acceder a ella.
- **/encuesta**: Proporciona un enlace y código QR para acceder a la encuesta de evaluación basada en las heurísticas de Nielsen.
- **/contacto**: Muestra información de contacto del desarrollador, incluyendo enlaces a sus redes sociales (Instagram, Telegram y LinkedIn).

## Enlaces Directos

- **Aplicación Web**: [https://trabajo-de-grado-2-front.vercel.app/](https://trabajo-de-grado-2-front.vercel.app/)
- **Actividad de Oratoria**: [https://trabajo-de-grado-2-front.vercel.app/activity/oratoria](https://trabajo-de-grado-2-front.vercel.app/activity/oratoria)
- **Actividad de Pensamiento Crítico**: [https://trabajo-de-grado-2-front.vercel.app/activity/debate-ia](https://trabajo-de-grado-2-front.vercel.app/activity/debate-ia)
- **Encuesta de Evaluación**: [https://docs.google.com/forms/d/e/1FAIpQLSfX8qGxE-3NvcMLs7QcpJwi7nYaWiFpiUVdKKdrQZRiJehf5Q/viewform?usp=dialog](https://docs.google.com/forms/d/e/1FAIpQLSfX8qGxE-3NvcMLs7QcpJwi7nYaWiFpiUVdKKdrQZRiJehf5Q/viewform?usp=dialog)

## Gestión de Errores

En la app pueden ocurrir errores por límites de los servicios utilizados. Algunas soluciones:
- Intentar nuevamente la acción
- Esperar entre 30 minutos y 1 hora
- Si el problema persiste, contactar al desarrollador

## Desarrollador

Juan David Moreno Alfonso, estudiante de Ingeniería en Sistemas de la Universidad del Valle sede Tuluá.

### Contacto
- Instagram: [@hellojuanda](https://www.instagram.com/hellojuanda/)
- Telegram: @heisjuanda
- LinkedIn: [Juan David Moreno](https://www.linkedin.com/in/juan-david-moreno-883a46233/)

# Diagrama de la App
![JuanDaBot (2)](https://github.com/user-attachments/assets/8c203115-7f8d-4f05-a93c-5e6c7de1bd98)

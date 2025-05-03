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

## Gestión de Errores

En la app pueden ocurrir errores por límites de los servicios utilizados. Algunas soluciones:
- Intentar nuevamente la acción
- Esperar entre 30 minutos y 1 hora
- Si el problema persiste, contactar al desarrollador

## Desarrollador

Juan David Moreno Alfonso, estudiante de Ingeniería en Sistemas de la Universidad del Valle sede Tuluá.
Instagram: @hellojuanda 
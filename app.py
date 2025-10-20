# Importaciones necesarias
# Necessary imports
from flask import Flask, render_template, request
from google import genai
from PIL import Image
from io import BytesIO
import requests
import uuid
import torch
from TTS.api import TTS
import os, re
import time
import threading
from dotenv import load_dotenv
load_dotenv()

# Iniciamos la aplicación Flask
# We start the Flask application
app = Flask(__name__)

TTS_MODEL = None
TTS_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Ruta al archivo .wav de referencia para la clonación de voz
# Path to the reference .wav file for voice cloning
SPEAKER_WAV_PATH = "static/audio/audio_ref/7927fdfc.wav"
TTS_LANGUAGE = "en"

# Carga el modelo XTTSv2 para la generación de voz
# Loads the XTTSv2 model for voice generation
try:
    TTS_MODEL = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(TTS_DEVICE)
except Exception as e:
    TTS_MODEL = None

# Definir API Key de IA Gemini
# Define Gemini AI API Key
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Definir API Key de HF
# Define HF API Key
hf_api_key = os.getenv("HF_API_KEY")

# Definimos URL de acceso para el modelo de generación de imágenes
# Define access URL for the image generation model
HF_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

# Función para la generación de imágenes a partir del prompt
# Function for image generation from the prompt
def generar_imagen(prompt, nombre):

    # Encabezados de la solicitud
    # Request headers
    headers = {"Authorization": f"Bearer {hf_api_key}"}

    # Creación de Payload
    # Payload creation
    payload = {"inputs": prompt}

    max_retries = 5

    # Realiza 5 intentos de conexión
    # Makes 5 connection attempts
    for attempt in range(max_retries):
        try:
            # Envía la solicitud POST
            # Sends the POST request
            response = requests.post(HF_API_URL, headers=headers, json=payload)

            # Conexión exitosa
            # Successful connection
            if response.status_code == 200:

                image_bytes = response.content
                image = Image.open(BytesIO(image_bytes))

                # Creamos el directorio para guardar las imágenes y creamos el nombre del archivo (filename)
                # We create the directory to save the images and create the filename
                os.makedirs("static/logos", exist_ok=True)
                filename = f"{nombre.lower().replace(' ', '_')}.png"
                filepath = os.path.join("static/logos", filename)
                image.save(filepath)

                return f"/static/logos/{filename}"

            # Conexión suspendida (modelo cargándose o en cola)
            # Suspended connection (model loading or queued)
            elif response.status_code == 503:
                time.sleep(10)
                continue

            # Conexión errónea
            # Erroneous connection
            else:
                return None

        except requests.exceptions.RequestException as e:
            return None
        except Exception as e:
            return None

    return None

# Función para la generación de audio/voz
# Function for audio/voice generation
def generar_audio(texto: str, emocion: str = "neutra"):

    # Variables globales
    # Global variables
    global TTS_MODEL, SPEAKER_WAV_PATH, TTS_LANGUAGE

    # Modelo no disponible
    # Model not available
    if TTS_MODEL is None:
        return None

    # Busca el archivo de voz de referencia
    # Searches for the reference voice file
    if not os.path.exists(SPEAKER_WAV_PATH):
        return None

    # Limpieza de texto y definición de ruta...
    # Text cleaning and path definition...
    texto_limpio = re.sub(r'["\n]', ' ', texto).strip()
    filename = f"audio_{uuid.uuid4().hex[:8]}.wav"
    filepath = os.path.join("static", "audio", filename)
    os.makedirs(os.path.join("static", "audio"), exist_ok=True)

    try:
        # Llama a la función de síntesis de voz
        # Calls the voice synthesis function
        TTS_MODEL.tts_to_file(
            text=texto_limpio,
            speaker_wav=SPEAKER_WAV_PATH,
            language=TTS_LANGUAGE,
            file_path=filepath
        )

        return f"/static/audio/{filename}"

    except Exception as e:
        return None

# Ruta home
# Home route
@app.route('/', methods=['GET'])
def home():
    # Renderizado del template home
    # Rendering of the home template
    return render_template('index.html')

# Ruta para generación de imagen/audio
# Route for image/audio generation
@app.route('/generate', methods=['POST'])
def generate_response():

    # Obtención de inputs
    # Getting inputs
    emocion_input = request.form['emocion']
    elemento_input = request.form['elemento']
    lang = request.form.get('lang', 'en')

    # Actualiza la variable global TTS_LANGUAGE con el idioma seleccionado
    # Updates the global variable TTS_LANGUAGE with the selected language
    global TTS_LANGUAGE
    TTS_LANGUAGE = lang

    # Generación de Prompt en Inglés
    # English Prompt Generation
    if lang == "en":

        titulo_tag = 'Conceptual Title'
        interp_tag = 'Poetic Interpretation'
        prompt_tag = 'Photorealistic AI Prompt'

        prompt_conceptual = f"""
            You are a visual poet and an expert art director specializing in **surrealism** and **high-fidelity rendering**. Your task is to conceptualize and fuse the emotion or mental state '{emocion_input}' with the central object '{elemento_input}' to create a photorealistic, emotionally dense, and conceptually rich scene.

            Generate your response in THREE CLEAR sections, separated strictly by the double hashtag symbol (##):

            ## {titulo_tag}
            Invent a poetic and striking title that encapsulates the fusion of the emotion and the object.

            ## {interp_tag}
            Write a brief description of the scene's meaning and mood (Max 3 lines).

            ## {prompt_tag}
            Write a LONG, highly detailed image prompt for a generative AI model (SDXL). The image must be rendered in a **Surreal, Photorealistic, and Hyper-detailed** style. The scene must dramatically showcase the central object in an oneiric setting, using **cinematic lighting, deep volumetric fog, complex textures, and an intense color palette**. Crucially, you must include technical quality modifiers at the end (e.g., **8k, ultra-detailed, sharp focus, Octane Render, cinematic photo, style of Zdzisław Beksiński**). The composition must be artistic, focused on the narrative, and avoid any unwanted elements.
            AVOID: text, watermark, low quality, cartoon, illustration.
        """
    else:
        titulo_tag = 'Título Conceptual'
        interp_tag = 'Interpretación Poética'
        prompt_tag = 'Prompt Fotorrealista para IA'

        prompt_conceptual = f"""
            Eres un poeta visual y un director de arte experto especializado en **surrealismo** y **renderizado de alta fidelidad**. Tu tarea es conceptualizar y fusionar la emoción o estado mental '{emocion_input}' con el objeto central '{elemento_input}' para crear una escena **fotorrealista, emocionalmente intensa y conceptualmente rica**.

            Genera tu respuesta en **TRES SECCIONES CLARAS**, separadas estrictamente por el símbolo de doble almohadilla (##):

            ## {titulo_tag}
            Inventa un título poético e impactante que encapsule la fusión de la emoción y el objeto.

            ## {interp_tag}
            Escribe una breve descripción del significado y la atmósfera de la escena (máx. 3 líneas).

            ## {prompt_tag}
            Escribe un prompt LARGO y altamente detallado para un modelo generativo de IA (SDXL). **¡IMPORTANTE! Este prompt DEBE ESTAR ESCRITO COMPLETAMENTE EN INGLÉS.** La imagen debe ser renderizada en un estilo **surrealista, fotorrealista y ultra detallado**. La escena debe mostrar dramáticamente el objeto central en un entorno onírico, usando **iluminación cinematográfica, niebla volumétrica profunda, texturas complejas y una paleta de colores intensa**. Crucialmente, debes incluir modificadores de calidad técnica al final (por ejemplo: **8k, ultra detallado, enfoque nítido, Octane Render, foto cinematográfica, estilo de Zdzisław Beksiński**). La composición debe ser artística, centrada en la narrativa y evitar cualquier elemento no deseado.
            EVITAR: texto, marcas de agua, baja calidad, caricatura, ilustración.
        """

    # Llama a la API de Gemini
    # Calls the Gemini API
    text_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt_conceptual]
    )

    respuesta_bruta = text_response.text.strip()

    # Separar la respuesta en partes
    # Separate the response into parts
    try:
        partes = re.split(r'##\s*', respuesta_bruta)

        titulo_concepto = partes[1].replace(titulo_tag, '').strip()
        interpretacion_poetica = partes[2].replace(interp_tag, '').strip()
        prompt_para_sdxl = partes[3].replace(prompt_tag, '').strip()

    except (IndexError, AttributeError) as e:
        # En caso de error en el formato de la respuesta
        # In case of an error in the response format
        pass

    # Definición de hilos para la ejecución en simultáneo y acortar tiempos
    # Definition of threads for simultaneous execution and time reduction
    class TaskResult:
        def __init__(self):
            self.result = None

    result_imagen = TaskResult()
    result_audio = TaskResult()

    def run_generar_imagen(prompt, nombre, result_obj):
        result_obj.result = generar_imagen(prompt, nombre)

    def run_generar_audio(texto, emocion, result_obj):
        result_obj.result = generar_audio(texto, emocion)

    t_imagen = threading.Thread(
        target=run_generar_imagen,
        args=(prompt_para_sdxl, elemento_input, result_imagen)
    )

    t_audio = threading.Thread(
        target=run_generar_audio,
        args=(interpretacion_poetica, elemento_input, result_audio)
    )

    t_imagen.start()
    t_audio.start()

    t_imagen.join()
    t_audio.join()

    # Llamada a función para generar imagen
    # Call to function to generate image
    dream_url = result_imagen.result

    # Llamada a función para generar audio
    # Call to function to generate audio
    audio_url = result_audio.result

    # Retorno de datos al template
    # Return data to the template
    return render_template('index.html',
                           current_lang=lang,
                           input_emocion=emocion_input,
                           input_elemento=elemento_input,
                           title=titulo_concepto,
                           interpretation=interpretacion_poetica,
                           dream_url=dream_url,
                           audio_url=audio_url )

if __name__ == "__main__":
    app.run(debug=True)
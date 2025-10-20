# 🎨 Generador de Arte Conceptual con Música

Una aplicación web que combina inteligencia artificial para crear arte conceptual surrealista con música instrumental generada automáticamente.

## ✨ Características

- **Generación de Conceptos**: Usa Gemini AI para crear títulos poéticos e interpretaciones artísticas
- **Música Sintética**: Genera música instrumental basada en la interpretación emocional
- **Interfaz Moderna**: Diseño glassmorphism con gradientes y efectos visuales
- **Sin API Keys para Música**: La generación musical es completamente gratuita

## 🚀 Instalación

### 1. Instalar dependencias necesarias
```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno
Crear archivo `.env`:
```
GEMINI_API_KEY=tu_api_key_de_google_aqui
HF_API_KEY=tu_api_key_de_huggingface_aqui  # Opcional para imágenes
```

### 3. Ejecutar la aplicación
```bash
python app.py
```

## 🧹 Limpieza de Dependencias

Si tienes paquetes innecesarios instalados, ejecuta:
```bash
python cleanup_dependencies.py
```

Esto desinstalará automáticamente:
- elevenlabs
- bark
- music21
- transformers
- torch
- datasets
- huggingface_hub
- soundfile
- Y otros paquetes no utilizados

## 📋 Dependencias Necesarias

- **Flask**: Framework web
- **google-generativeai**: Para generar conceptos poéticos
- **Pillow**: Procesamiento de imágenes
- **python-dotenv**: Manejo de variables de entorno
- **requests**: Llamadas HTTP
- **numpy**: Cálculos numéricos para audio
- **scipy**: Generación de audio sintético

## 🎵 Cómo Funciona

1. **Usuario ingresa**: Emoción + Elemento
2. **Gemini analiza**: Crea título e interpretación poética
3. **Sistema musical**: Analiza emociones y genera música sintética
4. **Resultado**: Muestra título, interpretación y reproductor de música

## 🔧 API Keys Requeridas

- **GEMINI_API_KEY**: Obligatoria para generar conceptos poéticos
- **HF_API_KEY**: Opcional para generar imágenes (actualmente deshabilitado)

## 🎼 Generación de Música

La música se genera localmente sin API keys:
- Analiza palabras clave emocionales
- Crea audio sintético de 30 segundos
- Diferentes estilos según la emoción detectada
- Fallback a Python puro si numpy/scipy no están disponibles

## 📁 Estructura del Proyecto

```
Practice2/
├── app.py                 # Aplicación principal
├── requirements.txt       # Dependencias necesarias
├── cleanup_dependencies.py # Script de limpieza
├── README.md             # Este archivo
├── .env                  # Variables de entorno
├── templates/
│   └── index.html        # Interfaz web
└── static/
    ├── logos/            # Imágenes generadas
    └── audio/            # Archivos de música
```

## 🐛 Solución de Problemas

### Error de music21
Si ves errores de music21, ejecuta el script de limpieza:
```bash
python cleanup_dependencies.py
```

### Error de audio
Si no se genera música, verifica que numpy esté instalado:
```bash
pip install numpy scipy
```

### Error de API
Verifica que GEMINI_API_KEY esté configurada en el archivo `.env`

## 🎯 Uso

1. Abre http://localhost:5000
2. Ingresa una emoción (ej: "Melancolía")
3. Ingresa un elemento (ej: "Cabina telefónica")
4. Haz clic en "Generar Arte Conceptual y Música"
5. Disfruta del resultado poético con música

¡Disfruta creando arte conceptual con música! 🎨🎵

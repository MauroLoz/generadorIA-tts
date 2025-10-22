# Conceptual Art Generator with AI Voice Narration

A web application that combines artificial intelligence to create surreal conceptual art with AI-generated voice narration that interprets the artistic concepts.

## ✨ Features

- **Concept Generation**: Uses Gemini AI to create poetic titles and artistic interpretations
- **AI Voice Narration**: Generates voice narration that interprets the artistic concept using XTTSv2
- **Image Generation**: Creates photorealistic surreal images using Stable Diffusion XL
- **Multi-language Support**: Supports both English and Spanish for voice narration
- **Modern Interface**: Glassmorphism design with gradients and visual effects
- **Interactive Audio Player**: Custom audio controls with progress tracking and volume control
- **Responsive Design**: Adapts seamlessly to different screen sizes and devices

## 🚀 Installation

### 1. Install necessary dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment variables
Create `.env` file:
```
GEMINI_API_KEY=your_google_api_key_here
HF_API_KEY=your_huggingface_api_key_here
```

### 3. Run the application
```bash
python app.py
```

## 📋 Required Dependencies

- **Flask**: Web framework
- **google-genai**: For generating poetic concepts using Gemini AI
- **Pillow**: Image processing
- **python-dotenv**: Environment variables management
- **requests**: HTTP calls
- **torch**: PyTorch for AI model inference
- **TTS**: Text-to-Speech library for voice generation

## 🎵 How It Works

1. **User Input**: Emotion + Element
2. **Gemini Analysis**: Creates poetic title and artistic interpretation
3. **AI Processing**: Generates both image and voice narration simultaneously
4. **Result**: Displays title, interpretation, generated image, and audio player

## 🔧 Required API Keys

- **GEMINI_API_KEY**: Required for generating poetic concepts
- **HF_API_KEY**: Required for image generation using Stable Diffusion XL

## 🎤 Voice Generation

Voice narration is generated using XTTSv2:
- Uses voice cloning with a reference audio file
- Supports multiple languages (English/Spanish)
- Generates natural-sounding narration of the artistic interpretation
- Runs locally without additional API costs

## 🎨 Frontend Features

The web interface includes:

### CSS (index.css)
- **Glassmorphism Design**: Modern glass-like effects with transparency and blur
- **Responsive Layout**: Grid-based layout that adapts to different screen sizes
- **Gradient Backgrounds**: Beautiful color transitions and visual effects
- **Interactive Elements**: Hover effects, smooth transitions, and visual feedback

### JavaScript (index.js)
- **Audio Player Controls**: Custom audio player with play/pause, progress bar, and volume control
- **Language Switching**: Dynamic language toggle between English and Spanish
- **Real-time Updates**: Live audio progress tracking and time display
- **User Experience**: Smooth interactions and responsive feedback

## 📁 Project Structure

```
Practice2/
├── app.py                 # Main application
├── requirements.txt       # Required dependencies
├── README.md             # This file
├── .env                  # Environment variables
├── templates/
│   └── index.html        # Web interface template
└── static/
    ├── css/
    │   └── index.css     # Glassmorphism styles and responsive design
    ├── js/
    │   └── index.js      # Audio player controls and language switching
    ├── logos/            # Generated images
    ├── audio/            # Generated voice files
    └── audio_ref/        # Reference voice file for cloning
```

## 🐛 Troubleshooting

### TTS Model Loading Error
If you see TTS model loading errors, make sure you have sufficient disk space and memory:
```bash
# The XTTSv2 model will be downloaded automatically on first run
# Ensure you have at least 4GB of free disk space
```

### Audio Generation Error
If voice generation fails, check that the reference audio file exists:
```bash
# Ensure the reference voice file is present at:
# static/audio/audio_ref/7927fdfc.wav
```

### API Errors
Verify that both API keys are configured in the `.env` file:
- GEMINI_API_KEY for concept generation
- HF_API_KEY for image generation

## 🎯 Usage

1. Open http://localhost:5000
2. Select language (English/Spanish)
3. Enter an emotion (e.g., "Melancholy")
4. Enter an element (e.g., "Phone booth")
5. Click "Generate Conceptual Art and Voice Narration"
6. Enjoy the poetic result with AI voice narration

Enjoy creating conceptual art with AI voice narration! 🎨🎤

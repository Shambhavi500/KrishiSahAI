
import os
import uuid
import threading
from pathlib import Path
from flask import jsonify

# Configure paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_FOLDER = BASE_DIR / 'uploads'
AUDIO_FOLDER = BASE_DIR / 'uploads' / 'audio'
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# Try imports
try:
    import whisper
    WHISPER_AVAILABLE = True
    # Load model lazily to avoid startup delay
    whisper_model = None
except ImportError:
    WHISPER_AVAILABLE = False
    print("Warning: 'openai-whisper' not installed. STT will not work.")

try:
    from gtts import gTTS
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("Warning: 'gTTS' not installed. TTS will not work.")


class VoiceService:
    def __init__(self):
        self.model = None

    def _load_model(self):
        if not WHISPER_AVAILABLE:
            raise ImportError("Whisper is not installed")
        
        if self.model is None:
            print("Loading Whisper model (base)... this may take a moment.")
            try:
                # Use 'base' model for balance of speed/accuracy
                self.model = whisper.load_model("base") 
            except Exception as e:
                print(f"Error loading whisper model: {e}")
                raise e

    def transcribe(self, file_path):
        """Transcribe audio file to text"""
        if not WHISPER_AVAILABLE:
            return {"error": "STT service unavailable (missing dependency)"}
        
        try:
            self._load_model()
            result = self.model.transcribe(file_path)
            return {"text": result["text"].strip()}
        except Exception as e:
            print(f"Transcription error: {e}")
            return {"error": str(e)}

    def text_to_speech(self, text, language='en'):
        """Convert text to speech audio file"""
        if not TTS_AVAILABLE:
            return {"error": "TTS service unavailable (missing dependency)"}
            
        try:
            # Map language codes if necessary
            lang_map = {'en': 'en', 'hi': 'hi', 'mr': 'mr'} # gTTS supports hi, mr
            lang = lang_map.get(language, 'en')
            
            filename = f"tts_{uuid.uuid4()}.mp3"
            filepath = AUDIO_FOLDER / filename
            
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(filepath)
            
            # Return relative path for frontend to fetch
            return {"audio_url": f"/uploads/audio/{filename}", "filepath": str(filepath)}
            
        except Exception as e:
            print(f"TTS error: {e}")
            return {"error": str(e)}

# Singleton instance
voice_service = VoiceService()

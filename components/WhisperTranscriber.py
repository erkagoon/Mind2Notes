import whisper
import openai
from constants import OPENAI_API_KEY, OPENAI_AUDIO_MODEL

class WhisperTranscriber:
    def __init__(self, record: str, type: str, use_api: bool = False):
        self.record = record
        self.whisper = whisper
        self.type = type
        self.use_api = use_api

    def transcribe(self):
        try:
            if not self.use_api:
                print("Transcribing using local model...")
                print("Loading model...")
                model = self.whisper.load_model(self.type)
                print("Model loaded. Starting transcription...")
                print ("self.record: ", self.record)
                result = model.transcribe(self.record)
                print("Transcription completed.")
                return result["text"]
            else:
                print("Transcribing using OpenAI API...")
                openai.api_key = OPENAI_API_KEY
                model = OPENAI_AUDIO_MODEL
                f = open(self.record, "rb")
                transcript = openai.Audio.transcribe("whisper-1", f)
                print("Transcription completed.")
                return transcript['text']
        except Exception as error:
            print(f"Error during transcription: {error}")
            return ""
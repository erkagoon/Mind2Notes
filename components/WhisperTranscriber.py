import whisper
from constants import OPENAI_AUDIO_MODEL
from components.OpenAIHandler import OpenAIHandler

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
                #print("Transcribing using OpenAI API...")
                openai_handler = OpenAIHandler()
                response_format = "text"
                transcript = openai_handler.post_audio(model=OPENAI_AUDIO_MODEL, file_path=self.record, response_format=response_format)
                #print("Transcription completed.")
                return transcript
        except Exception as error:
            print(f"Error during transcription: {error}")
            return ""
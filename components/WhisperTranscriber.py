class WhisperTranscriber:
    def __init__(self, record: str, whisper, type: str):
        self.record = record
        self.whisper = whisper
        self.type = type

    def transcribe(self):
        try:
            model = self.whisper.load_model(self.type)
            result = model.transcribe(self.record)
            return result["text"]
        except Exception as error:
            print(f"Error during transcription: {error}")
            return ""
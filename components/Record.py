import os
import pyaudio
import wave
from PyQt6 import QtWidgets, QtCore
from Ui.Overlay import Overlay
from components.WhisperTranscriber import WhisperTranscriber
import whisper

class Record:
    def __init__(self, filename="../records/output.wav", rate=44100, chunk=1024, channels=2, format=pyaudio.paInt16):
        self.filename = filename
        self.rate = rate
        self.chunk = chunk
        self.channels = channels
        self.format = format
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.overlay = None

        # Initialiser QTimer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.record_chunk)

    def record_chunk(self):
        data = self.stream.read(self.chunk)
        self.frames.append(data)

        # Si l'overlay n'est plus visible, stopper l'enregistrement
        if not self.overlay.isVisible():
            self.stop_record()

    def start_record(self):
        # Initialiser l'enregistrement
        self.stream = self.audio.open(format=self.format, channels=self.channels,
                                      rate=self.rate, input=True,
                                      frames_per_buffer=self.chunk)
        self.frames = []

        # Afficher l'overlay
        self.overlay = QtWidgets.QWidget()
        self.overlay_ui = Overlay()
        self.overlay_ui.setupUi(self.overlay)
        self.overlay_ui.closed.connect(self.stop_record)  # Connectez le signal 'closed' de l'overlay à la méthode stop_record

        # Affichage de l'overlay dans le coin supérieur droit
        screen_geometry = QtWidgets.QApplication.primaryScreen().geometry()
        overlay_geometry = self.overlay.frameGeometry()
        overlay_x = screen_geometry.width() - overlay_geometry.width()
        overlay_y = 0  # Pour le coin supérieur
        self.overlay.move(overlay_x, overlay_y)

        self.overlay.show()

        # Démarrer le timer pour enregistrer périodiquement
        self.timer.start(10)

        print("Recording started...")

    def stop_record(self):
        self.timer.stop()  # Arrêtez le timer

        print("Recording stopped.")
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.audio = pyaudio.PyAudio()

        # Construire le chemin complet pour sauvegarder le fichier
        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, self.filename)

        # S'assurer que le dossier existe avant d'écrire le fichier
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))

        print(f"File saved as {file_path}")

        record_path = "records\output.wav"
        whisper_module = whisper
        model_type = "small"
        transcriber = WhisperTranscriber(record_path, whisper_module, model_type)
        transcription = transcriber.transcribe()
        print(transcription)
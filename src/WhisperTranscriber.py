import whisper
import torch
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class WhisperTranscriber:
    
    def __init__(self, device="cuda" if torch.cuda.is_available() else "cpu"):
        self.device = device
        logging.info(f"Initializing WhisperTranscriber with device: {self.device}")
        try:
            self.model = whisper.load_model("medium", device=self.device)
            logging.info("Whisper model loaded successfully")
        except Exception as e:
            logging.error(f"Failed to load Whisper model: {e}")
            raise

    def transcribe_audio(self, file_name):
        """
        Транскрибирует аудиофайл и возвращает текст.
        """
        logging.info(f"Transcribing audio file: {file_name}")
        try:
            result = self.model.transcribe(file_name)
            logging.info(f"Transcription successful for file: {file_name}")
            return result["text"]
        except Exception as e:
            logging.error(f"Failed to transcribe audio file: {file_name}. Error: {e}")
            raise

    def clear_model(self):
        """
        Освобождает ресурсы, занятые моделью.
        """
        logging.info("Clearing Whisper model")
        try:
            del self.model
            torch.cuda.empty_cache()
            logging.info("Whisper model cleared successfully")
        except Exception as e:
            logging.error(f"Failed to clear Whisper model: {e}")
            raise
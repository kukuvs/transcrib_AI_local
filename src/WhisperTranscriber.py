import whisper
import torch
import logging

# Настройка логирования (по умолчанию уровень INFO)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WhisperTranscriber:
    """
    Класс для транскрибирования аудиофайлов с использованием модели Whisper.
    """

    def __init__(self, device="cuda" if torch.cuda.is_available() else "cpu"):
        """
        Инициализация модели Whisper с указанием устройства (CUDA или CPU).

        Args:
            device (str): Устройство для выполнения модели ("cuda" или "cpu").
        """
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
        Транскрибирует аудиофайл и возвращает распознанный текст.

        Args:
            file_name (str): Путь к аудиофайлу.

        Returns:
            str: Распознанный текст из аудиофайла.
        """
        logging.debug(f"Transcribing audio file: {file_name}")
        if not file_name or not isinstance(file_name, str):
            logging.error("Invalid file name provided for transcription")
            raise ValueError("Invalid file name")

        try:
            result = self.model.transcribe(file_name)
            logging.debug(f"Transcription successful for file: {file_name}")
            return result["text"]
        except Exception as e:
            logging.error(f"Failed to transcribe audio file: {file_name}. Error: {e}")
            raise

    def clear_model(self):
        """
        Освобождает ресурсы, занятые моделью Whisper, и очищает кэш GPU.
        """
        logging.info("Clearing Whisper model")
        try:
            del self.model
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            logging.debug("Whisper model cleared successfully")
        except Exception as e:
            logging.error(f"Failed to clear Whisper model: {e}")
            raise

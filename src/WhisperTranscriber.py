import whisper
import torch
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class WhisperTranscriber:
    """
    Класс для транскрипции аудиофайлов с использованием модели Whisper.

    Attributes:
        device (str): Устройство для выполнения вычислений (CPU или GPU).
        model (whisper.model.Whisper): Загруженная модель Whisper.
    """

    def __init__(self, device: str = "cuda" if torch.cuda.is_available() else "cpu"):
        """
        Инициализация объекта WhisperTranscriber.

        Args:
            device (str): Устройство для выполнения вычислений (CPU или GPU).
        """
        self.device = device
        logging.info(f"Initializing WhisperTranscriber with device: {self.device}")
        try:
            # Загрузка модели Whisper
            self.model = whisper.load_model("medium", device=self.device)
            logging.info("Whisper model loaded successfully")
        except Exception as e:
            logging.error(f"Failed to load Whisper model: {e}")
            raise

    def transcribe_audio(self, file_name: str) -> str:
        """
        Транскрибирует аудиофайл и возвращает текст.

        Args:
            file_name (str): Путь к аудиофайлу.

        Returns:
            str: Транскрибированный текст.
        """
        logging.info(f"Transcribing audio file: {file_name}")
        try:
            # Транскрипция аудиофайла
            result = self.model.transcribe(file_name)
            logging.info(f"Transcription successful for file: {file_name}")
            return result["text"]
        except FileNotFoundError:
            logging.error(f"File not found: {file_name}")
            raise
        except Exception as e:
            logging.error(f"Failed to transcribe audio file: {file_name}. Error: {e}")
            raise

    def clear_model(self):
        """
        Освобождает ресурсы, занятые моделью.
        """
        logging.info("Clearing Whisper model")
        try:
            # Удаление модели и очистка кэша CUDA
            del self.model
            torch.cuda.empty_cache()
            logging.info("Whisper model cleared successfully")
        except AttributeError:
            logging.error("Whisper model was not loaded or already cleared")
        except Exception as e:
            logging.error(f"Failed to clear Whisper model: {e}")
            raise

    def __del__(self):
        """
        Деструктор для освобождения ресурсов при удалении объекта.
        """
        self.clear_model()

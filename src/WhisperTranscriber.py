import whisper
import torch

class WhisperTranscriber:
    def __init__(self, device="cuda" if torch.cuda.is_available() else "cpu"):
        self.device = device
        self.model = whisper.load_model("small", device=self.device)

    def transcribe_audio(self, file_name):
        """
        Транскрибирует аудиофайл и возвращает текст.
        """
        result = self.model.transcribe(file_name)
        return result["text"]

    def clear_model(self):
        """
        Освобождает ресурсы, занятые моделью.
        """
        del self.model
        torch.cuda.empty_cache()

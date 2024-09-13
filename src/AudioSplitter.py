from pydub import AudioSegment
import os
import logging
import subprocess

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class AudioSplitter:
    """
    Класс для разделения аудиофайлов на части.

    Attributes:
        split_parts (int): Количество частей, на которые будет разделен аудиофайл.
    """

    def __init__(self, split_parts: int = 3):
        """
        Инициализация объекта AudioSplitter.

        Args:
            split_parts (int): Количество частей, на которые будет разделен аудиофайл.
                               Должно быть положительным целым числом.
        """
        if split_parts <= 0 or not isinstance(split_parts, int):
            raise ValueError("Number of split parts must be greater than 0")
        self.split_parts = split_parts

    def check_ffmpeg(self):
        """
        Проверяет наличие ffmpeg и устанавливает его, если необходимо.
        """
        try:
            # Проверка наличия ffmpeg
            subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logging.info("ffmpeg is installed")
        except subprocess.CalledProcessError:
            logging.warning("ffmpeg is not installed. Attempting to install...")
            try:
                # Установка ffmpeg
                subprocess.run(["winget", "install", "ffmpeg"], check=True)
                logging.info("ffmpeg installed successfully")
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to install ffmpeg: {e}")
                raise

    def split_audio(self, file_path: str, output_dir: str) -> list:
        """
        Дробит аудиофайл на указанное количество частей и сохраняет их в указанной директории.

        Args:
            file_path (str): Путь к аудиофайлу, который нужно разделить.
            output_dir (str): Директория для сохранения разделенных частей аудиофайла.

        Returns:
            list: Список путей к разделенным частям аудиофайла.
        """
        # Проверка наличия ffmpeg
        self.check_ffmpeg()

        # Создаем директорию, если её нет
        os.makedirs(output_dir, exist_ok=True)

        try:
            # Загрузка аудиофайла
            audio = AudioSegment.from_file(file_path)
            duration = len(audio)  # Длительность в миллисекундах
            part_duration = duration // self.split_parts

            output_files = []
            for i in range(self.split_parts):
                start = i * part_duration
                end = start + part_duration if i < self.split_parts - 1 else duration
                part = audio[start:end]
                output_file = os.path.join(output_dir, f"part_{i + 1}.mp3")
                part.export(output_file, format="mp3")
                output_files.append(output_file)
                logging.info(f"Successfully exported part {i + 1} to {output_file}")

            logging.info(f"Successfully split audio file '{file_path}' into {self.split_parts} parts")
            return output_files

        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
            return []
        except Exception as e:
            logging.error(f"Failed to split audio file '{file_path}': {e}")
            return []

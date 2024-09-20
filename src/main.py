import os
import shutil
import logging
from multiprocessing import Pool, cpu_count
from .WhisperTranscriber import WhisperTranscriber
from .AudioSplitter import AudioSplitter
from .FileManager import FileManager

# Настройка логирования (по умолчанию уровень INFO)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_audio_file(args):
    """
    Обрабатывает один аудиофайл: транскрибирует и записывает результат.
    
    Args:
        args (tuple): file_path (str) - путь к аудиофайлу, 
                      output_dir_path (str) - директория для сохранения результата.
    
    Returns:
        str: Распознанный текст из аудиофайла.
    """
    file_path, output_dir_path = args
    transcriber = WhisperTranscriber()
    file_manager = FileManager()

    try:
        logging.debug(f"Processing audio file: {file_path}")
        
        # Транскрибируем аудиофайл
        text = transcriber.transcribe_audio(file_path)
        logging.debug(f"Transcription successful for file: {file_path}")

        # Записываем результат в файл
        output_text_file = os.path.join(output_dir_path, "recognized.txt")
        file_manager.write_text_to_file(f"{file_path}\n{text}\n\n", output_text_file)
        logging.debug(f"Transcription result written to file: {output_text_file}")

        return text
    except Exception as e:
        logging.error(f"Error processing audio file: {file_path}. Error: {e}")
        raise
    finally:
        transcriber.clear_model()
        logging.debug(f"Model cleared for file: {file_path}")

        # Удаление аудиофайла после обработки
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                logging.debug(f"Audio file removed: {file_path}")
            except Exception as e:
                logging.error(f"Error removing audio file: {file_path}. Error: {e}")
        else:
            logging.warning(f"Audio file not found for removal: {file_path}")


def process_audio_files(input_file_path, output_dir_path, split_parts, progress_callback=None):
    """
    Обрабатывает основной аудиофайл: разбивает на части, транскрибирует и объединяет результаты.

    Args:
        input_file_path (str): Путь к исходному аудиофайлу.
        output_dir_path (str): Директория для сохранения результатов.
        split_parts (int): Количество частей, на которые нужно разделить аудиофайл.
        progress_callback (function, optional): Функция для отслеживания прогресса.

    Returns:
        str: Полный распознанный текст из всех частей аудиофайла.
    """
    if not os.path.isfile(input_file_path):
        raise ValueError(f"Invalid input file path: {input_file_path}")

    if not os.path.isdir(output_dir_path):
        raise ValueError(f"Invalid output directory path: {output_dir_path}")

    try:
        logging.info(f"Starting audio file processing for: {input_file_path}")
        
        # Создание временной директории для хранения частей
        res_dir = os.path.join(output_dir_path, "res")
        os.makedirs(res_dir, exist_ok=True)
        logging.debug(f"Created temporary directory: {res_dir}")

        # Разделение аудиофайла
        splitter = AudioSplitter(split_parts)
        sliced_files = splitter.split_audio(input_file_path, res_dir)
        logging.info(f"Audio file split into {len(sliced_files)} parts")

        # Подготовка аргументов для параллельной обработки
        args_list = [(file_path, output_dir_path) for file_path in sliced_files]

        recognized_texts = []

        # Параллельная обработка частей файла
        with Pool(processes=cpu_count()) as pool:
            for i, recognized_text in enumerate(pool.imap_unordered(process_audio_file, args_list)):
                recognized_texts.append(recognized_text)
                if progress_callback:
                    progress_callback(i + 1, len(sliced_files))

        full_recognized_text = " ".join(recognized_texts)
        logging.info("All transcriptions combined into a single text")

        # Удаление временной директории после обработки
        if os.path.exists(res_dir):
            try:
                shutil.rmtree(res_dir)
                logging.debug(f"Temporary directory removed: {res_dir}")
            except Exception as e:
                logging.error(f"Error removing temporary directory: {res_dir}. Error: {e}")
        else:
            logging.warning(f"Temporary directory not found for removal: {res_dir}")

        return full_recognized_text
    except Exception as e:
        logging.error(f"Error processing audio files. Error: {e}")
        raise

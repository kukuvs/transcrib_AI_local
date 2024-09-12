import os
import shutil
import sys
import logging
from multiprocessing import Pool, cpu_count
from .WhisperTranscriber import WhisperTranscriber
from .AudioSplitter import AudioSplitter
from .FileManager import FileManager

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def process_audio_file(args):
    """
    Обрабатывает один аудиофайл: транскрибирует и записывает результат.
    """
    file_path, output_dir_path = args
    transcriber = WhisperTranscriber()
    file_manager = FileManager()

    try:
        logging.info(f"Processing audio file: {file_path}")
        # Транскрибируем аудиофайл
        text = transcriber.transcribe_audio(file_path)
        logging.info(f"Transcription successful for file: {file_path}")

        # Записываем результат в файл
        output_text_file = os.path.join(output_dir_path, "recognized.txt")
        file_manager.write_text_to_file(f"{file_path}\n{text}\n\n", output_text_file)
        logging.info(f"Transcription result written to file: {output_text_file}")

        return text  # Возвращаем результат транскрипции
    except Exception as e:
        logging.error(f"Error processing audio file: {file_path}. Error: {e}")
        raise
    finally:
        # Очистка модели
        transcriber.clear_model()
        logging.info(f"Model cleared for file: {file_path}")

def process_audio_files(input_file_path, output_dir_path, split_parts, progress_callback=None):
    try:
        logging.info(f"Starting audio file processing for: {input_file_path}")
        splitter = AudioSplitter(split_parts)
        res_dir = os.path.join(output_dir_path, "res")
        os.makedirs(res_dir, exist_ok=True)
        logging.info(f"Created temporary directory: {res_dir}")

        sliced_files = splitter.split_audio(input_file_path, res_dir)
        logging.info(f"Audio file split into {len(sliced_files)} parts")

        args_list = [(file_path, output_dir_path) for file_path in sliced_files]

        recognized_texts = []

        with Pool(processes=cpu_count()) as pool:
            for i, recognized_text in enumerate(pool.imap_unordered(process_audio_file, args_list)):
                recognized_texts.append(recognized_text)
                if progress_callback:
                    progress_callback(i + 1, len(sliced_files))

        full_recognized_text = " ".join(recognized_texts)
        logging.info("All transcriptions combined into a single text")

        if os.path.exists(res_dir):
            shutil.rmtree(res_dir)
            logging.info(f"Temporary directory removed: {res_dir}")

        return full_recognized_text
    except Exception as e:
        logging.error(f"Error processing audio files. Error: {e}")
        raise
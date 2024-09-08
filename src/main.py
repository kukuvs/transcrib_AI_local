import os
import shutil
import sys
sys.path.append("./")
from multiprocessing import Pool, cpu_count
from .WhisperTranscriber import WhisperTranscriber
from .AudioSplitter import AudioSplitter
from .FileManager import FileManager

def process_audio_file(args):
    """
    Обрабатывает один аудиофайл: транскрибирует и записывает результат.
    """
    file_path, output_dir_path = args
    transcriber = WhisperTranscriber()
    file_manager = FileManager()

    try:
        # Транскрибируем аудиофайл
        text = transcriber.transcribe_audio(file_path)
        
        # Записываем результат в файл
        output_text_file = os.path.join(output_dir_path, "recognized.txt")
        file_manager.write_text_to_file(f"{file_path}\n{text}\n\n", output_text_file)
        
        return text  # Возвращаем результат транскрипции
    finally:
        # Очистка модели
        transcriber.clear_model()

def process_audio_files(input_file_path, output_dir_path, split_parts, progress_callback=None):
    """
    Основной процесс обработки аудиофайлов: дробление, транскрипция и сохранение текста.
    """
    # Инициализация компонентов
    splitter = AudioSplitter(split_parts)
    res_dir = os.path.join(output_dir_path, "res")
    os.makedirs(res_dir, exist_ok=True)

    # Дробим аудиофайл
    sliced_files = splitter.split_audio(input_file_path, res_dir)

    # Создаем список аргументов для процесса
    args_list = [(file_path, output_dir_path) for file_path in sliced_files]

    recognized_texts = []

    # Используем пул процессов для параллельной обработки файлов
    with Pool(processes=cpu_count()) as pool:
        for i, recognized_text in enumerate(pool.imap_unordered(process_audio_file, args_list)):
            recognized_texts.append(recognized_text)  # Собираем результаты транскрипции
            if progress_callback:
                progress_callback(i + 1, len(sliced_files))

    # Объединяем все части текста в один
    full_recognized_text = " ".join(recognized_texts)

    # Удаляем папку 'res' после завершения обработки
    if os.path.exists(res_dir):
        shutil.rmtree(res_dir)

    return full_recognized_text

import os
import logging
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from ..main import process_audio_files
from src.WhisperTranscriber import init_whisper_transcriber
import threading

init_whisper_transcriber()# сразу загружаем модель
# Настраиваем логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Создаем экземпляр приложения Flask
app = Flask(__name__)

# Папка для загрузки файлов
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Создаем папку для загрузки, если она не существует
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Глобальная переменная для отслеживания прогресса
progress = [0]

@app.route('/')
def index():
    """
    Главная страница.
    Возвращает HTML-шаблон index.html.
    """
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    """
    Обрабатывает запросы на favicon.
    Возвращает пустой ответ с кодом 204.
    """
    return '', 204

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Обрабатывает загрузку файла и начинает процесс его обработки в отдельном потоке.

    Возвращает JSON с сообщением об успешном начале обработки или ошибкой.
    """
    global progress
    logging.debug("Received upload request")

    # Проверка наличия файла в запросе
    if 'file' not in request.files:
        logging.error("No file part in request")
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    
    # Проверка наличия имени файла
    if file.filename == '':
        logging.error("No selected file")
        return jsonify({'error': 'No selected file'}), 400

    # Проверяем размер файла
    file.stream.seek(0, os.SEEK_END)
    file_size = file.stream.tell()
    file.stream.seek(0)
    if file_size == 0:
        logging.error("Empty file")
        return jsonify({'error': 'Empty file'}), 400

    # Безопасное получение имени файла
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Сохранение файла
    try:
        file.save(file_path)
        logging.info(f"File saved successfully: {file_path}")
    except Exception as e:
        logging.error(f"Error saving file: {e}")
        return jsonify({'error': 'Error saving file'}), 500

    # Получение выходной директории из формы
    output_dir = request.form.get('output_dir')
    if not output_dir:
        logging.error("No output directory specified")
        return jsonify({'error': 'No output directory specified'}), 400

    # Получение и проверка количества частей
    try:
        split_parts = int(request.form['split_parts'])
        if split_parts <= 0:
            raise ValueError("Split parts must be positive")
    except (KeyError, ValueError) as e:
        logging.error(f"Invalid split parts value: {e}")
        return jsonify({'error': 'Invalid split parts value'}), 400

    # Запуск обработки файла в отдельном потоке
    def process_and_update_progress():
        """
        Обрабатывает аудиофайл и обновляет прогресс.
        Удаляет исходный файл после завершения обработки.
        """
        global progress
        progress[0] = 0
        try:
            # Процесс обработки аудиофайла
            full_recognized_text = process_audio_files(
                file_path, output_dir, split_parts,
                lambda i, total: progress.__setitem__(0, i * 100 // total)
            )
            progress[0] = 100
            logging.info("Processing completed successfully")
        except Exception as e:
            logging.error(f"Processing error: {e}")
            progress[0] = -1  # Ошибка в процессе обработки

        # Удаление исходного файла
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logging.info(f"File removed: {file_path}")
            else:
                logging.warning(f"File not found for removal: {file_path}")
        except Exception as e:
            logging.error(f"Error removing file: {file_path}. Error: {e}")

    # Стартуем поток
    thread = threading.Thread(target=process_and_update_progress)
    thread.start()

    return jsonify({'message': 'Processing started'})

@app.route('/status')
def status():
    """
    Возвращает текущий статус прогресса обработки файла.
    
    Возвращает JSON с текущим значением прогресса.
    """
    global progress
    return jsonify({'progress': progress[0]})

# Точка входа для запуска приложения
if __name__ == '__main__':
    app.run(debug=True)

import os
import shutil
import logging
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from ..main import process_audio_files
import threading


# Создаем папку для загрузки файлов, если она не существует


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
# Глобальная переменная для отслеживания прогресса
progress = [0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return '', 204  # Возвращаем пустой ответ для favicon

@app.route('/upload', methods=['POST'])
def upload_file():
    global progress
    logging.debug(f"Request form data: {request.form}")
    logging.debug(f"Request files: {request.files}")
    
    if 'file' not in request.files:
        logging.error("No file part in request")
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        logging.error("No selected file")
        return jsonify({'error': 'No selected file'}), 400

    # Сбрасываем указатель на начало файла перед проверкой размера
    file.stream.seek(0, os.SEEK_END)  # Перемещаемся в конец файла
    file_size = file.stream.tell()    # Узнаем текущую позицию (размер файла)
    file.stream.seek(0)               # Возвращаем указатель в начало

    if file_size == 0:
        logging.error("Empty file")
        return jsonify({'error': 'Empty file'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        file.save(file_path)
    except Exception as e:
        logging.error(f"Error saving file: {e}")
        return jsonify({'error': 'Error saving file'}), 500

    output_dir = request.form.get('output_dir')
    if not output_dir:
        logging.error("No output directory specified")
        return jsonify({'error': 'No output directory specified'}), 400

    try:
        split_parts = int(request.form['split_parts'])
    except (KeyError, ValueError):
        logging.error("Invalid split parts value")
        return jsonify({'error': 'Invalid split parts value'}), 400

    # Запуск обработки в отдельном потоке
    def process_and_update_progress():
        global progress
        progress[0] = 0
        try:
            # Обработка аудиофайлов
            full_recognized_text = process_audio_files(file_path, output_dir, split_parts, lambda i, total: progress.__setitem__(0, i * 100 // total))
            progress[0] = 100
        except Exception as e:
            logging.error(f"Processing error: {e}")
            progress[0] = -1  # Отметить ошибку

        # Удаление исходного файла после обработки
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logging.info(f"Audio file removed: {file_path}")
            else:
                logging.warning(f"Audio file not found for removal: {file_path}")
        except Exception as e:
            logging.error(f"Error removing audio file: {file_path}. Error: {e}")

    thread = threading.Thread(target=process_and_update_progress)
    thread.start()

    return jsonify({'message': 'Processing started'})

@app.route('/status')
def status():
    global progress
    return jsonify({'progress': progress[0]})

if __name__ == '__main__':
    app.run(debug=True)
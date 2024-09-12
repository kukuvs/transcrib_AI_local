import os
import shutil
import logging
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from ..main import process_audio_files
import threading

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Глобальная переменная для отслеживания прогресса
progress = [0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global progress
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    output_dir = request.form['output_dir']
    split_parts = int(request.form['split_parts'])
    
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

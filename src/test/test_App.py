import os
import shutil
import pytest
from io import BytesIO
from flask import Flask
from ..veu.App import app  # Замените your_module на имя вашего модуля

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = 'test_uploads/'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    with app.test_client() as client:
        yield client
    # Попытка удалить папку с загрузками
    try:
        shutil.rmtree(app.config['UPLOAD_FOLDER'])
    except PermissionError:
        pass  # Игнорировать ошибку, если файл занят

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'<!DOCTYPE html>' in rv.data

def test_upload_no_file(client):
    rv = client.post('/upload', data={})
    assert rv.status_code == 400
    assert rv.json == {'error': 'No file part'}

def test_upload_empty_file(client):
    data = {
        'file': (BytesIO(), 'test.wav'),
        'output_dir': 'test_output/',
        'split_parts': 2
    }
    rv = client.post('/upload', data=data)
    assert rv.status_code == 400
    assert rv.json == {'error': 'Empty file'}

def test_upload_file(client):
    data = {
        'file': (BytesIO(b'fake audio data'), 'test.wav'),
        'output_dir': 'test_output/',
        'split_parts': 2
    }
    rv = client.post('/upload', data=data)
    assert rv.status_code == 200
    assert rv.json == {'message': 'Processing started'}

def test_status(client):
    rv = client.get('/status')
    assert rv.status_code == 200
    assert 'progress' in rv.json

def test_upload_and_status(client):
    data = {
        'file': (BytesIO(b'fake audio data'), 'test.wav'),
        'output_dir': 'test_output/',
        'split_parts': 2
    }
    rv = client.post('/upload', data=data)
    assert rv.status_code == 200
    assert rv.json == {'message': 'Processing started'}

    # Проверка статуса обработки
    rv = client.get('/status')
    assert rv.status_code == 200
    assert 'progress' in rv.json

if __name__ == '__main__':
    pytest.main()

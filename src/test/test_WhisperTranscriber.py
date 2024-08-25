import pytest
import torch
import os
from gtts import gTTS
from ..WhisperTranscriber import WhisperTranscriber

@pytest.fixture
def transcriber():
    """
    Фикстура для создания экземпляра класса WhisperTranscriber.
    """
    transcriber = WhisperTranscriber()
    yield transcriber
    if hasattr(transcriber, 'model'):
        transcriber.clear_model()

@pytest.fixture
def create_test_audio():
    """
    Фикстура для создания тестового аудиофайла с текстом.
    """
    file_name = "test_audio.mp3"
    text = "This is a test audio file for transcription."  # Текст для преобразования в аудио
    
    # Создание аудиофайла с помощью gTTS
    tts = gTTS(text=text, lang="en")
    tts.save(file_name)

    yield file_name
    
    # Удаление тестового аудиофайла после теста
    if os.path.exists(file_name):
        os.remove(file_name)

def test_transcribe_audio(transcriber, create_test_audio):
    """
    Тестирование метода транскрибации аудио.
    """
    test_audio = create_test_audio
    result = transcriber.transcribe_audio(test_audio)
    
    assert isinstance(result, str)  # Проверка, что результат является строкой
    assert len(result) > 0  # Проверка, что транскрибированный текст не пуст
    assert "test audio file" in result.lower()  # Проверка, что транскрибированный текст содержит ожидаемую фразу

def test_clear_model(transcriber):
    """
    Тестирование метода очистки модели.
    """
    transcriber.clear_model()
    with pytest.raises(AttributeError):
        _ = transcriber.model  # Проверяем, что модель удалена

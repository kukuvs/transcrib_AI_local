import pytest
import sys
sys.path.append('../')
from AudioSplitter import AudioSplitter
from unittest.mock import patch
from pydub import AudioSegment

class TestAudioSplitter:
    def test_split_audio(self):
        # Создаем объект AudioSplitter с split_parts=3
        splitter = AudioSplitter(3)

        # Создаем временный файл для тестирования
        with patch('pydub.AudioSegment.from_file') as mock_from_file:
            mock_from_file.return_value = AudioSegment.empty()
            file_path = 'test.mp3'
            output_dir = 'test_dir'

            # Вызываем метод split_audio
            output_files = splitter.split_audio(file_path, output_dir)
            assert len(output_files) == 3
    
    def test_split_audio_with_zero_split_parts(self):
        # Ожидаем ValueError при split_parts=0
        with pytest.raises(ValueError, match="Number of split parts must be greater than 0"):
            AudioSplitter(0)
    
    def test_split_audio_with_negative_split_parts(self):
        # Ожидаем ValueError при split_parts=-1
        with pytest.raises(ValueError, match="Number of split parts must be greater than 0"):
            AudioSplitter(-1)

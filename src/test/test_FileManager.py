import pytest  # noqa: F401
from unittest.mock import patch
import sys
sys.path.append('../')
from FileManager import FileManager

class TestFileManager:
    def test_write_text_to_file(self):
        # Тестирует запись непустого текста в файл

        
        with patch('builtins.open') as mock_open:
            mock_open.return_value.__enter__.return_value.write.return_value = None
            text = 'Hello, world!'
            filename = 'test.txt'

            # Вызываем метод write_text_to_file с непустым текстом
            FileManager.write_text_to_file(text, filename)

            # Проверяем, что метод open был вызван с правильными аргументами
            mock_open.assert_called_once_with(filename, "a", encoding="utf-8")

            # Проверяем, что метод write был вызван с правильным текстом
            mock_open.return_value.__enter__.return_value.write.assert_called_once_with(text)

    def test_write_text_to_file_with_empty_text(self):
        # Тестирует, что при передаче пустого текста файл не открывается

        
        with patch('builtins.open') as mock_open:
            text = ''
            filename = 'test.txt'

            # Вызываем метод write_text_to_file с пустым текстом
            FileManager.write_text_to_file(text, filename)

            # Проверяем, что метод open не был вызван, так как текст пустой
            mock_open.assert_not_called()

    def test_write_text_to_file_with_none_text(self):
        # Тестирует, что при передаче None в качестве текста файл не открывается

        
        with patch('builtins.open') as mock_open:
            text = None
            filename = 'test.txt'

            # Вызываем метод write_text_to_file с текстом, равным None
            FileManager.write_text_to_file(text, filename)

            # Проверяем, что метод open не был вызван, так как текст равен None
            mock_open.assert_not_called()

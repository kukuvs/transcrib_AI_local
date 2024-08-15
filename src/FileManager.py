import os

class FileManager:
    @staticmethod
    def write_text_to_file(text, filename):
        """
        Записывает текст в файл с указанием кодировки utf-8.
        """
        with open(filename, "a", encoding="utf-8") as f:
            f.write(text)

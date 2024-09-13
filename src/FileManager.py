import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class FileManager:
    """
    Класс для управления файлами.

    Methods:
        write_text_to_file(text: str, filename: str): Записывает текст в файл.
    """

    @staticmethod
    def write_text_to_file(text: str, filename: str):
        """
        Записывает текст в файл.

        Args:
            text (str): Текст для записи.
            filename (str): Путь к файлу для записи.
        """
        if not text:  # Проверка на пустой текст или None
            logging.warning(f"Attempt to write empty or None text to file '{filename}'")
            return

        try:
            # Запись текста в файл
            with open(filename, "a", encoding="utf-8") as file:
                file.write(text)
                logging.info(f"Successfully wrote text to file '{filename}'")
        except Exception as e:
            logging.error(f"Failed to write text to file '{filename}': {e}")

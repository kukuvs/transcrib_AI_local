import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FileManager:
    @staticmethod
    def write_text_to_file(text, filename):
        if not text:  # Проверка на пустой текст или None
            logging.warning(f"Attempt to write empty or None text to file '{filename}'")
            return

        try:
            with open(filename, "a", encoding="utf-8") as file:
                file.write(text)
                logging.info(f"Successfully wrote text to file '{filename}'")
        except Exception as e:
            logging.error(f"Failed to write text to file '{filename}': {e}")
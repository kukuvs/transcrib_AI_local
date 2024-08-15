
class FileManager:
    @staticmethod
    def write_text_to_file(text, filename):
        if not text or None:  # Проверка на пустой текст или None
            return
        with open(filename, "a", encoding="utf-8") as file:
            file.write(text)

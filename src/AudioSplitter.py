from pydub import AudioSegment
import os

class AudioSplitter:
    def __init__(self, split_parts=3):
        if split_parts <= 0 or not isinstance(split_parts, int) :
            raise ValueError("Number of split parts must be greater than 0")
        self.split_parts = split_parts

    def split_audio(self, file_path, output_dir):
        """
        Дробит аудиофайл на указанное количество частей и сохраняет их в указанной директории.
        """
        # Создаем директорию, если её нет
        os.makedirs(output_dir, exist_ok=True)
        
        audio = AudioSegment.from_file(file_path)
        duration = len(audio)  # Длительность в миллисекундах
        part_duration = duration // self.split_parts

        output_files = []
        for i in range(self.split_parts):
            start = i * part_duration
            end = start + part_duration if i < self.split_parts - 1 else duration
            part = audio[start:end]
            output_file = os.path.join(output_dir, f"part_{i + 1}.mp3")
            part.export(output_file, format="mp3")
            output_files.append(output_file)

        return output_files

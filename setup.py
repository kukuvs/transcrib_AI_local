from cx_Freeze import setup, Executable
import os
import sys

# Определите пути к основным модулям и файлам
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Используйте "Console" если приложение имеет консольный интерфейс

# Путь к директории с исходными файлами
src_dir = os.path.join(os.path.dirname(__file__), 'src')

include_files = [
    ("src/WhisperTranscriber.py", "WhisperTranscriber.py"),
    ("src/AudioSplitter.py", "AudioSplitter.py"),
    ("src/FileManager.py", "FileManager.py"),
    ("src/main.py", "main.py")
]

build_exe_options = {
    "packages": ["os", "tkinter", "multiprocessing", "pydub", "whisper", "torch"],
    "excludes": [],
    "include_files": include_files,
}

setup(
    name="AudioTranscriptionApp",
    version="0.1",
    description="Audio Transcription Application",
    options={"build_exe": build_exe_options},
    executables=[Executable("src/veu/App.py", base=base)],
)

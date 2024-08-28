import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import threading
from ..main import process_audio_files





class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Transcription App")
        self.root.geometry("500x500")

        # Переменные для путей
        self.input_file_path = tk.StringVar()
        self.output_dir_path = tk.StringVar()
        self.split_parts = tk.IntVar(value=3)

        # Выбор файла для распознавания
        tk.Label(root, text="Выберите файл для распознавания:").pack(pady=10)
        tk.Entry(root, textvariable=self.input_file_path, width=50).pack(padx=10)
        tk.Button(root, text="Обзор", command=self.browse_input_file).pack(pady=5)

        # Выбор директории для сохранения результата
        tk.Label(root, text="Выберите папку для сохранения результата:").pack(pady=10)
        tk.Entry(root, textvariable=self.output_dir_path, width=50).pack(padx=10)
        tk.Button(root, text="Обзор", command=self.browse_output_dir).pack(pady=5)

        # Количество частей для разделения файла
        tk.Label(root, text="Количество частей для разделения файла:").pack(pady=10)
        tk.Spinbox(root, from_=1, to=10, textvariable=self.split_parts).pack(padx=10, pady=5)

        # Кнопки запуска и остановки
        self.start_button = tk.Button(root, text="Запуск", command=self.start_processing)
        self.start_button.pack(pady=20)

        self.stop_button = tk.Button(root, text="Стоп", state=tk.DISABLED, command=self.stop_processing)
        self.stop_button.pack(pady=5)

        # Прогрессбар
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=20)

        # Переменная для управления потоком
        self.stop_event = threading.Event()

    def browse_input_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3")])
        if file_path:
            self.input_file_path.set(file_path)

    def browse_output_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.output_dir_path.set(dir_path)

    def start_processing(self):
        if not self.input_file_path.get() or not self.output_dir_path.get():
            messagebox.showerror("Ошибка", "Пожалуйста, выберите файл и папку для сохранения.")
            return
        
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.progress.config(value=0)
        self.stop_event.clear()

        # Запуск процесса
        self.run_processing()

    def run_processing(self):
        def target():
            try:
                process_audio_files(self.input_file_path.get(), self.output_dir_path.get(), self.split_parts.get(), self.update_progress)
                messagebox.showinfo("Готово", "Обработка завершена!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
            finally:
                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)
                self.progress.config(value=0)

        # Запускаем обработку в отдельном потоке
        processing_thread = threading.Thread(target=target)
        processing_thread.start()

    def update_progress(self, current, total):
        progress_value = (current / total) * 100
        self.progress['value'] = progress_value
        self.root.update_idletasks()

    def stop_processing(self):
        self.stop_event.set()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

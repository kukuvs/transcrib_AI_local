// Добавляем обработчик события для формы загрузки
document.getElementById('upload-form').addEventListener('submit', function (e) {
	e.preventDefault() // Предотвращаем стандартное поведение формы

	var formData = new FormData(this) // Создаем объект FormData из формы
	var xhr = new XMLHttpRequest() // Создаем новый объект XMLHttpRequest

	xhr.open('POST', '/upload', true) // Открываем соединение для отправки данных на сервер

	xhr.onload = function () {
		if (xhr.status === 200) {
			// Если запрос успешен, отображаем сообщение и запускаем проверку прогресса
			document.getElementById('message').innerHTML = 'Обработка началась.'
			checkProgress() // Запуск проверки прогресса
		} else {
			// Если запрос неуспешен, отображаем сообщение об ошибке
			document.getElementById('message').innerHTML = 'Ошибка загрузки.'
		}
	}

	xhr.onerror = function () {
		// Если произошла ошибка при загрузке, отображаем сообщение об ошибке
		document.getElementById('message').innerHTML = 'Ошибка при загрузке.'
	}

	try {
		xhr.send(formData) // Отправляем данные формы на сервер
	} catch (error) {
		document.getElementById('message').innerHTML =
			'Ошибка отправки данных: ' + error.message
	}
})

/**
 * Функция для проверки прогресса обработки файла.
 */
function checkProgress() {
	var xhr = new XMLHttpRequest() // Создаем новый объект XMLHttpRequest
	xhr.open('GET', '/status', true) // Открываем соединение для получения статуса обработки

	xhr.onload = function () {
		if (xhr.status === 200) {
			try {
				// Парсим ответ сервера в формате JSON
				var response = JSON.parse(xhr.responseText)
				var progress = response.progress

				// Отображаем прогресс обработки
				document.getElementById('progress-container').style.display = 'block'
				document.getElementById('progress-bar').value = progress
				document.getElementById('progress-text').textContent = progress + '%'

				if (progress < 100) {
					// Если обработка не завершена, повторяем запрос через 1 секунду
					setTimeout(checkProgress, 1000)
				} else {
					// Если обработка завершена, отображаем сообщение
					document.getElementById('message').innerHTML = 'Обработка завершена!'
				}
			} catch (e) {
				// Если произошла ошибка при обработке ответа, отображаем сообщение об ошибке
				document.getElementById('message').innerHTML =
					'Ошибка обработки ответа: ' + e.message
			}
		} else {
			// Если запрос неуспешен, отображаем сообщение об ошибке
			document.getElementById('message').innerHTML = 'Ошибка запроса статуса.'
		}
	}

	xhr.onerror = function () {
		// Если произошла ошибка при запросе к серверу, отображаем сообщение об ошибке
		document.getElementById('message').innerHTML = 'Ошибка запроса к серверу.'
	}

	try {
		xhr.send() // Отправляем запрос на сервер
	} catch (error) {
		document.getElementById('message').innerHTML =
			'Ошибка отправки запроса: ' + error.message
	}
}

// Добавляем обработчик события для переключения темы
document.getElementById('theme-toggle').addEventListener('click', function () {
	// Переключаем класс темы у body
	document.body.classList.toggle('dark-theme')
})

// Добавляем обработчик события для ввода файла
document
	.getElementById('file-input')
	.addEventListener('change', function (event) {
		// Получаем имя выбранного файла или отображаем сообщение по умолчанию
		var fileName =
			event.target.files.length > 0
				? event.target.files[0].name
				: 'Выберите аудиофайл'
		document.getElementById('file-label').textContent = fileName
	})

// Добавляем обработчик события для проверки ввода файла
document
	.getElementById('file-input')
	.addEventListener('input', function (event) {
		var fileInput = event.target
		var file = fileInput.files[0]

		if (file) {
			// Проверка типа файла
			if (file.type !== 'audio/mpeg' && file.type !== 'audio/wav') {
				document.getElementById('message').innerHTML =
					'Неподдерживаемый тип файла. Пожалуйста, выберите файл в формате MP3 или WAV.'
				fileInput.value = '' // Очищаем поле ввода
				return
			}

			// Проверка размера файла
			if (file.size > 10 * 1024 * 1024) {
				// 10 MB
				document.getElementById('message').innerHTML =
					'Файл слишком большой. Пожалуйста, выберите файл меньше 10 MB.'
				fileInput.value = '' // Очищаем поле ввода
				return
			}

			document.getElementById('message').innerHTML = '' // Очищаем сообщение об ошибке
		}
	})

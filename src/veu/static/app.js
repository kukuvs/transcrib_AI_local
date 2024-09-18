document.getElementById('upload-form').addEventListener('submit', function (e) {
	e.preventDefault() // Предотвращаем стандартное поведение формы

	var formData = new FormData(this) // Создаем объект FormData из формы
	console.log([...formData.entries()]) // Вывод всех полей формы в консоль для отладки

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

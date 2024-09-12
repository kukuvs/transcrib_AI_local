document.getElementById('upload-form').addEventListener('submit', function (e) {
	e.preventDefault()

	var formData = new FormData(this)
	var xhr = new XMLHttpRequest()

	xhr.open('POST', '/upload', true)

	xhr.onload = function () {
		if (xhr.status === 200) {
			document.getElementById('message').innerHTML = 'Обработка началась.'
			checkProgress() // Запуск проверки прогресса
		} else {
			document.getElementById('message').innerHTML = 'Ошибка загрузки.'
		}
	}

	xhr.onerror = function () {
		document.getElementById('message').innerHTML = 'Ошибка при загрузке.'
	}

	xhr.send(formData)
})

function checkProgress() {
	var xhr = new XMLHttpRequest()
	xhr.open('GET', '/status', true)

	xhr.onload = function () {
		if (xhr.status === 200) {
			try {
				var response = JSON.parse(xhr.responseText)
				var progress = response.progress

				document.getElementById('progress-container').style.display = 'block'
				document.getElementById('progress-bar').value = progress
				document.getElementById('progress-text').textContent = progress + '%'

				if (progress < 100) {
					setTimeout(checkProgress, 1000) // Повторяем запрос через 1 сек
				} else {
					document.getElementById('message').innerHTML = 'Обработка завершена!'
				}
			} catch (e) {
				document.getElementById('message').innerHTML =
					'Ошибка обработки ответа.'
			}
		} else {
			document.getElementById('message').innerHTML = 'Ошибка запроса статуса.'
		}
	}

	xhr.onerror = function () {
		document.getElementById('message').innerHTML = 'Ошибка запроса к серверу.'
	}

	xhr.send()
}

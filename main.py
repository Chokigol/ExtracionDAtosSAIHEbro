import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = "http://www.saihebro.com/semobile/index.php?url=/tr/graficas_numeros/tag:A069T65QRIO1"

# Hacer la solicitud HTTP
response = requests.get(url)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
	# Parsear el contenido HTML con BeautifulSoup
	soup = BeautifulSoup(response.text, 'html.parser')

	# Encontrar la tabla
	table = soup.find('table')

	# Encontrar todas las filas de la tabla
	rows = table.find_all('tr')

	# Inicializar listas para almacenar los valores de la segunda columna, sus índices y las fechas
	values = []
	indices = []
	dates = []

	# Iterar sobre las filas y obtener los valores de la segunda columna y las fechas
	for index, row in enumerate(rows[1:], start=1):  # Empezar desde la segunda fila para omitir los encabezados
		cells = row.find_all('td')
		# Verificar si hay al menos dos celdas en la fila
		if len(cells) >= 2:
			value = cells[1].text.replace(',', '.')
			date_str = cells[0].text.strip()
			# Intentar convertir el valor a float y la fecha a un objeto de fecha
			try:
				values.append(float(value))
				indices.append(index)
				dates.append(datetime.strptime(date_str, "%d/%m/%Y %H:%M"))
			except (ValueError, ValueError) as e:
				print(f"Error al convertir valor o fecha: {e}")

	# Encontrar el valor máximo y su posición
	max_value = max(values)
	max_index = indices[values.index(max_value)]
	max_date = dates[values.index(max_value)]

	# Encontrar el valor mínimo y su posición
	min_value = min(values)
	min_index = indices[values.index(min_value)]
	min_date = dates[values.index(min_value)]

	print(f"El valor máximo en la segunda columna de la tabla es: {max_value}")
	# print(f"Se encuentra en la fila con índice: {max_index}")
	print(f"La fecha correspondiente al máximo es: {max_date.strftime('%d/%m/%Y %H:%M')}")

	# Tomar solo los últimos 10 valores para determinar la tendencia
	first_values = values[:10]
	mean_first_values = sum(first_values) / len(first_values)
	# Determinar la tendencia
	if first_values[0] > mean_first_values+1.5:
		trend = "Ascendente"
	elif first_values[0] < mean_first_values-1.5:
		trend = "Descendente"
	else:
		trend = "Constante"

	print(f"\nLa tendencia de los últimos 10 valores es: {trend}")
else:
		print(f"No se pudo acceder a la página. Código de estado: {response.status_code}")
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
    estacion = soup.find('span', class_='bloque2').text.strip()
    
    # Imprimir el contenido formateado
    parts = estacion.split('(')
    name_part = parts[0].strip()
    # Encontrar todas las tablas en la página
    tables = soup.find_all('table')

    # Inicializar listas para almacenar los valores, índices y fechas de todas las tablas
    all_values = []
    all_indices = []
    all_dates = []

    # Iterar sobre todas las tablas
    for table in tables:
        # Encontrar todas las filas de la tabla actual
        rows = table.find_all('tr')

        # Inicializar listas para almacenar los valores, índices y fechas de la tabla actual
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

        # Agregar los valores, índices y fechas de la tabla actual a las listas globales
        all_values.extend(values)
        all_indices.extend(indices)
        all_dates.extend(dates)
    

    max_value = max(all_values)
    max_index = all_indices[all_values.index(max_value)]
    max_date = all_dates[all_values.index(max_value)]
    
    # Ordenar las fechas y los valores en función de las fechas
    sorted_data = sorted(zip(all_dates, all_values, all_indices), key=lambda x: x[0])
    
    # Determinar la tendencia
    first_values = all_values[:10]
    mean_first_values = sum(first_values) / len(first_values)
    if first_values[0] > mean_first_values + 1.5:
        trend = "Ascendente"
    elif first_values[0] < mean_first_values - 1.5:
        trend = "Descendente"
    else:
        trend = "Constante"
    
    # print("Lista completa con fechas ordenadas:")
    # for date, value, index in sorted_data:
    #     print(f"{date.strftime('%d/%m/%Y %H:%M')} - Valor: {value} - Índice: {index}")
    print(f"{name_part}")
    print(f"El valor máximo en la segunda columna de todas las tablas es: {max_value}")
    # print(f"Se encuentra en la fila con índice: {max_index}")
    print(f"La fecha correspondiente al máximo es: {max_date.strftime('%d/%m/%Y %H:%M')}")
    print(f"La tendencia de los últimos 10 valores es: {trend}")

else:
    print(f"No se pudo acceder a la página. Código de estado: {response.status_code}")

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re

lista_urls = []
lista_libros = []
n = 1

for pagina in range(1, 4):
    url_pagina = f"https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once?page={pagina}"

    pedido_pagina = requests.get(url_pagina)
    pedido_pagina_html = pedido_pagina.text

    soup = BeautifulSoup(pedido_pagina_html, "html.parser")

    elementos_book_title = soup.find_all("a", class_="bookTitle")

    for elemento in elementos_book_title:
        url_libro = elemento['href']
        lista_urls.append(url_libro)

for url_libro in lista_urls:
    pedido_libro = requests.get("https://www.goodreads.com"+url_libro)
    pedido_libro_html = pedido_libro.text
    soup_libro = BeautifulSoup(pedido_libro_html, "html.parser")

    titulo = soup_libro.find("h1", class_="Text Text__title1")
    nombre_titulo = titulo.text if titulo else ""

    autor = soup_libro.find("span", class_="ContributorLink__name")
    nombre_autor = autor.text if autor else ""

    calificacion = soup_libro.find("div", class_="RatingStatistics__rating")
    valor_calificacion = calificacion.text if calificacion else ""

    generos = soup_libro.find_all("span", class_="BookPageMetadataSection__genreButton", limit=3)
    nombres_generos = [i.find("span", class_="Button__labelItem").text.strip() for i in generos]

    fecha = soup_libro.find("p", {"data-testid": "publicationInfo"})
    fecha_entera = fecha.text.strip() if fecha else ""
    fecha_coincide = re.search(r"(\w+ \d{1,2}, \d{4})", fecha_entera)
    fecha_formateada = ""
    if fecha_coincide:
        fecha_publicacion_linda = fecha_coincide.group(0)
        fecha_ordenada = datetime.strptime(fecha_publicacion_linda, "%B %d, %Y")
        fecha_formateada = fecha_ordenada.strftime("%d/%m/%Y")

    # Obtener el precio
    boton_precio = soup_libro.find("button", {"class": "Button Button--buy Button--medium Button--block"})

    try:
        precio = boton_precio.find("span", {"class": "Button__labelItem"}).string.split("$")[1]
    except:
        precio = 0

    informacion_libro = {
        "titulo": nombre_titulo,
        "autor": nombre_autor,
        "calificacion": valor_calificacion,
        "generos": nombres_generos,
        "fecha_publicacion": fecha_formateada,
        "precio": precio
    }

    lista_libros.append(informacion_libro)

    with open('libros.json', 'w', encoding='utf-8') as json_file:
        json.dump(lista_libros, json_file, ensure_ascii=False, indent=4)

    print(f"La información de todos los libros se ha guardado en un archivo JSON.{n}")
    n = n+1

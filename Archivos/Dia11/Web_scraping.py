import bs4
import requests

# crear url sin numero de página
url_base = 'https://books.toscrape.com/catalogue/page-{}.html'

# lista de titulos con 4 o 5 estrellas
titulos_rating_alto = []

# iterar paginas
for pagina in range(1, 2):  # pueden ser desde 1 hasta 51
    # crear sopa en cada pagina
    url_pagina = url_base.format(pagina)
    resultado = requests.get(url_pagina)
    sopa = bs4.BeautifulSoup(resultado.text, 'lxml')

    # seleccionar datos de los libros
    libros = sopa.select('.product_pod')  # obtiene una lista

    # iterar libros
    for libro in libros:

        # chequear estrellas
        if len(libro.select('.star-rating.Four')) != 0 or len(libro.select('.star-rating.Five')) != 0:
            # se remplaza con punto cuando la clase tiene espacio
            titulo_libro = libro.select('a')[1]['title']  # se usa [1] porque [0] tiene la imagen
            titulos_rating_alto.append(titulo_libro)

# ver libros
for t in titulos_rating_alto:
    print(t)

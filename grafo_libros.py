import json
from grafo import Grafo


class GrafoLibros:
    def __init__(self):
        self.grafo = Grafo()

    def agregar_libro(self, libro):
        for propiedad in libro:
            self.grafo.nuevo_nodo(propiedad)

        self.grafo.nueva_arista(libro["autor"], libro["titulo"], tipo="escribio")
        self.grafo.nueva_arista(libro["titulo"], libro["fecha_publicacion"], tipo="escrito")
        for genero in libro["generos"]:
            self.grafo.nueva_arista(libro["titulo"], genero, bid=True, tipo="genero_libro")
            self.grafo.nueva_arista(genero, libro["autor"], tipo="autores_generos")
        self.grafo.nueva_arista(libro["titulo"], libro["calificacion"], tipo="calificacion")
        self.grafo.nueva_arista(libro["titulo"], libro["precio"], tipo="precio")

    def libros_por_autor_ordenados_por_fecha(self, autor):
        libros_del_autor = []

        if autor in self.grafo.adj_list:
            for arista in self.grafo.adj_list[autor]:
                if arista[1] == 'escribio':
                    libro_titulo = arista[0]

                    fecha_lanzamiento = None
                    for fecha_arista in self.grafo.adj_list[libro_titulo]:
                        if fecha_arista[1] == 'escrito':
                            fecha_lanzamiento = fecha_arista[0]
                            break

                    if fecha_lanzamiento is not None:
                        libros_del_autor.append({
                            "titulo": libro_titulo,
                            "fecha_lanzamiento": fecha_lanzamiento
                        })

            if not libros_del_autor:
                print(f"No se encontraron libros escritos por {autor}.")

        libros_del_autor = sorted(libros_del_autor, key=lambda x: (int(x["fecha_lanzamiento"].split('/')[-1]), x["fecha_lanzamiento"]))

        return libros_del_autor

    def recomendar_libros_por_genero_y_decada(self, libro_titulo, n):
        libros_recomendados = []

        genero_libro_x = None
        decada_libro_x = None
        for arista in self.grafo.adj_list[libro_titulo]:
            if arista[1] == 'genero_libro':
                genero_libro_x = arista[0]
            elif arista[1] == 'escrito':
                decada_libro_x = int(arista[0].split('/')[-1][:3] + '0')

        if genero_libro_x is None or decada_libro_x is None:
            print(f"No se encontró información suficiente para el libro {libro_titulo}.")
            return libros_recomendados

        for nodo in self.grafo.adj_list:
            if nodo != libro_titulo:
                for arista in self.grafo.adj_list[nodo]:
                    if arista[1] == 'genero_libro' and arista[0] == genero_libro_x:
                        # Obtener la década del libro
                        decada_libro = None
                        for fecha_arista in self.grafo.adj_list[nodo]:
                            if fecha_arista[1] == 'escrito':
                                decada_libro = int(fecha_arista[0].split('/')[-1][:3] + '0')
                                break

                        if decada_libro is not None and decada_libro == decada_libro_x:
                            libros_recomendados.append({
                                "titulo": nodo,
                                "genero": genero_libro_x,
                                "decada": decada_libro
                            })

        libros_recomendados = sorted(libros_recomendados, key=lambda x: x["titulo"])

        libros_recomendados = libros_recomendados[:n]

        return libros_recomendados

    def listar_autores_por_genero(self, genero):
        autores = {}

        for nodo, aristas in self.grafo.adj_list.items():
            if nodo == genero:
                for arista in aristas:
                    autor = arista[0]
                    if autor in self.grafo.adj_list and arista[1] == "autores_generos":
                        autores[autor] = autores.get(autor, 0) + 1

        autores_ordenados = sorted(autores.items(), key=lambda x: x[1], reverse=True)

        return autores_ordenados

    def recomendar_libros_por_puntaje_y_genero(self, puntaje_minimo, generos):
        recomendaciones = set()

        for libro, aristas in self.grafo.adj_list.items():
            cumple_generos = all(
                any(arista[1] == "genero_libro" and g in arista[0] for arista in aristas)
                for g in generos
            )

            cumple_calificacion = any(
                arista[1] == "calificacion" and arista[0] and float(arista[0]) > puntaje_minimo
                for arista in aristas
            )

            if cumple_generos and cumple_calificacion:
                recomendaciones.add(libro)

        return list(recomendaciones)


def cargar_libros_desde_json(ruta):
    with open(ruta, 'r', encoding='utf-8') as archivo:
        libros = json.load(archivo)
    return libros


from grafo_libros import GrafoLibros, cargar_libros_desde_json

def mostrar_menu():
    print("1. Mostrar libros por autor ordenados por fecha")
    print("2. Recomendar libros por género y década")
    print("3. Listar autores por género")
    print("4. Recomendar libros por puntaje y género")
    print("0. Salir")


def imprimir_libros(libros):
    if libros:
        for titulo in libros:
            print(f"Título: {titulo}")
    else:
        print("No se encontraron libros.")


def main():
    libros_desde_json = cargar_libros_desde_json('libros.json')
    grafo_libros = GrafoLibros()

    for libro in libros_desde_json:
        grafo_libros.agregar_libro(libro)

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (0-4): ")

        if opcion == '1':
            autor_consulta = input("Ingrese el nombre del autor: ")
            libros_del_autor_ordenados = grafo_libros.libros_por_autor_ordenados_por_fecha(autor_consulta)
            imprimir_libros(libros_del_autor_ordenados)
        elif opcion == '2':
            libro_consulta = input("Ingrese el título del libro: ")
            num_libros_recomendados = int(input("Ingrese el número de libros recomendados: "))
            libros_recomendados = grafo_libros.recomendar_libros_por_genero_y_decada(libro_consulta, num_libros_recomendados)
            imprimir_libros(libros_recomendados)
        elif opcion == '3':
            genero_buscar = input("Ingrese el género a buscar: ")
            autores_ordenados = grafo_libros.listar_autores_por_genero(genero_buscar)
            if autores_ordenados:
                for autor, cantidad_libros in autores_ordenados:
                    print(f"Autor: {autor}, Libros escritos en {genero_buscar}: {cantidad_libros}")
            else:
                print(f"No se encontraron autores para el género {genero_buscar}.")

        elif opcion == '4':

            puntaje_minimo = float(input("Ingrese el puntaje mínimo: "))
            generos_deseados = input("Ingrese los géneros deseados separados por coma: ").split(',')
            libros_recomendados = grafo_libros.recomendar_libros_por_puntaje_y_genero(puntaje_minimo, generos_deseados)
            imprimir_libros(libros_recomendados)

        elif opcion == '0':
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, ingrese un número del 0 al 4.")

if __name__ == "__main__":
    main()


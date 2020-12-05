from collections import defaultdict
import sys
import re
import random

# Posibles movimientos que puede hacer el caballero en general
# Si analizamos cuales son los posibles movimientos del caballero podemos ver que en el tablero se veria de la siguiente manera
# Los cuadros rellenados son los posibles movimientos, K es el caballero y los cuadrados vacios son espacios donde el caballero no se puede mover
#       □   ■   □   ■   □
#       ■   □   □   □   ■
#       □   □   K   □   □
#       ■   □   □   □   ■
#       □   ■   □   ■   □
# Cada cuadrado rellenado se puede representar con una coordenada, y así es como se representa aquí
OFFSET_MOVIMIENTOS = (
              (-1, -2), ( 1, -2),
    (-2, -1),                     ( 2, -1),
    (-2,  1),                     ( 2,  1),
              (-1,  2), ( 1,  2),
)

# Checa si es posible los movimientos del caballero en una posicion en especifico
def movimientos_del_caballero(fila, columna, tamaño_del_tablero):
    for fila_offset, columna_offset in OFFSET_MOVIMIENTOS:
        mover_fila, mover_columna = fila + fila_offset, columna + columna_offset
        if 0 <= mover_fila < tamaño_del_tablero and 0 <= mover_columna < tamaño_del_tablero:
            yield mover_fila, mover_columna

# Agrega el posible movimiento en el diccionario
def agregar_posible_movimiento(tablero, vertice_a, vertice_b):
    tablero[vertice_a].add(vertice_b)
    tablero[vertice_b].add(vertice_a)

# Construye un grafo en un diccionario, cada nodo es un espacio en el tablero a simples palabras
# y ese nodo esta conectado a otros nodos, lo que define a que nodo esta conectado es simplemente si el caballero puede moverse
# desde el nodo actual a ese nodo tomando en cuenta sus restricciones de movimiento en el ajedrez que seria moverse como L
def construir_tablero(tamaño_del_tablero):
    tablero = defaultdict(set)
    for fila in range(tamaño_del_tablero):
        for columna in range(tamaño_del_tablero):
            for to_fila, to_columna in movimientos_del_caballero(fila, columna, tamaño_del_tablero):
                agregar_posible_movimiento(tablero, (fila, columna), (to_fila, to_columna))
    return tablero


def primer_verdadero(secuencia):
    for item in secuencia:
        if item:
            return item
    return None


def dfs(tamaño_tablero, tablero):
    total_espacios = tamaño_tablero * tamaño_tablero

    def explorar(camino, vertice_actual):

        # Una vez que se han explorado el total de espacios 
        # Se regresa la solución
        if len(camino) + 1 == total_espacios:
            return camino + [vertice_actual]

        aun_por_visitar = tablero[vertice_actual] - set(camino)
        # Si en el vertice actual no hay otro espacio que se puede visitar
        # Estamos en un camino muerto
        if not aun_por_visitar:
            return False

        # Checamos todos los vertices validos que aun no se visitan
        siguiente_vertice = sorted(aun_por_visitar)
        return primer_verdadero(explorar(camino + [vertice_actual], vertice)
                          for vertice in siguiente_vertice)

    return primer_verdadero(explorar([], vertice_inicial)
                      for vertice_inicial in tablero)


def main():
    tamaño_tablero = 5 #random.randint(5, 15)
    tablero = construir_tablero(tamaño_tablero)
    tablero_matriz = [([0]*tamaño_tablero) for i in range(tamaño_tablero)]
    print(tamaño_tablero)

    dfs_resultado = dfs(tamaño_tablero, tablero)

    print(dfs_resultado)
    for nodo in range(len(dfs_resultado)):
        print(dfs_resultado[nodo])
        tablero_matriz[dfs_resultado[nodo][0]][dfs_resultado[nodo][1]] = nodo

    for i in range(len(tablero_matriz)):
        print(tablero_matriz[i])
main()
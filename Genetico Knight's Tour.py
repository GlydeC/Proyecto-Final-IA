import sys
import re
import random
from collections import deque, defaultdict
import time

poblacion_tamaño = 100000
generaciones_max = 20000
tamaño_tablero = 5
posicion_inicial = (random.randint(0, tamaño_tablero-1), random.randint(0, tamaño_tablero-1))

def checar_repetido_lista(lista, individuo):
    for i in range(len(lista)):
        if lista[i] == individuo:
            return True
    return False

def randomizar_idividuo(p): 

    key1 = "" 

    for i in range(p): 
        temp = str(random.randint(0, 1)) 
        key1 += temp 
    return(key1) 

def dividir_individuo(individuo):
    return [char for char in individuo] 

def juntar_individuo(individuo):
    new = ""
    for x in individuo: 
        new += x    
    return new

def generarPoblacionInicial(tamaño_individuo):
   
    poblacion = list()
    
    for i in range(poblacion_tamaño):
        nuevo_individuo = randomizar_idividuo(tamaño_individuo)
        if not checar_repetido_lista(poblacion, nuevo_individuo):
            poblacion.append(nuevo_individuo)
        else: 
            while checar_repetido_lista(poblacion, nuevo_individuo):
                nuevo_individuo = randomizar_idividuo(tamaño_individuo)
    return poblacion

#   • 4 • 3 •   • 100 • 011 •
#   5 • • • 2   101 • • • 010
#   • • X • •     • • X • •
#   6 • • • 1   110 • • • 001
#   • 7 • 0 •   • 111 • 000 •
def interpretar_movimiento_bits(bits, posicion_actual):
    if bits == '000': # (1,2)
        x = posicion_actual[0] + 1
        y = posicion_actual[1] + 2
    elif bits == '001': # (2,1)
        x = posicion_actual[0] + 2
        y = posicion_actual[1] + 1
    elif bits == '010': # (2,-1)
        x = posicion_actual[0] + 2
        y = posicion_actual[1] - 1
    elif bits == '011': # (1,-2)
        x = posicion_actual[0] + 1
        y = posicion_actual[1] - 2
    elif bits == '100': # (-1,-2)
        x = posicion_actual[0] - 1
        y = posicion_actual[1] - 2
    elif bits == '101': # (-2,-1)
        x = posicion_actual[0] - 2
        y = posicion_actual[1] - 1
    elif bits == '110': # (-2,1)
        x = posicion_actual[0] - 2
        y = posicion_actual[1] + 1
    elif bits == '111': # (-1,2)
        x = posicion_actual[0] - 1
        y = posicion_actual[1] + 2

    return (x,y)

def encontrar_maximo(poblacion, poblacion_valores):
    individuo_maximo_posicion = 0
    valor_maximo = 0
    for x in range(len(poblacion)):
        if poblacion_valores[x] > valor_maximo:
            individuo_maximo_posicion = x
            valor_maximo = poblacion_valores[x]
    
    return individuo_maximo_posicion

def interpretar_individuo(ind):
    posicion_actual = posicion_inicial
    individuo = dividir_individuo(ind)
    z = 3
    lista_movimientos_individuo = list()
    lista_movimientos_individuo.append(posicion_actual)

    while z < len(individuo):
        bits = juntar_individuo(individuo[z] + individuo[z+1] + individuo[z+2])
        posicion_actual = interpretar_movimiento_bits(bits, posicion_actual)
        lista_movimientos_individuo.append(posicion_actual)
        z = z + 3

    return lista_movimientos_individuo
        
    
def cruzar_individuos(i1, i2):
    individuo1 = dividir_individuo(i1)
    individuo2 = dividir_individuo(i2)
    individuo3 = [""]*len(individuo1)

    for x in range(len(individuo1)):
        if individuo1[x] == individuo2[x]:
            individuo3[x] = individuo1[x]
        elif random.randint(1,2) == 1:
            individuo3[x] = individuo1[x]
        else:
            individuo3[x] = individuo2[x]
    return juntar_individuo(individuo3)
            
def mutar_individuo(ind):
    individuo = dividir_individuo(ind)
    nuevo_individuo = [""]*len(individuo)

    for x in range(len(individuo)):
        # 1% de probabilidad de que mute un binario del individuo
        if random.randint(0,100) >= 99:
            if individuo[x] == '1':
                nuevo_individuo[x] = '0'
            else:
                nuevo_individuo[x] = '1'    
        else:
            nuevo_individuo[x] = individuo[x]

    return juntar_individuo(nuevo_individuo)   

def generar_hijos(generacion_anterior, generacion_anterior_valores, gen):
    ganadores = list()
    ganadores_valores = list()
    print(len(generacion_anterior))
    # Seleccionar individuos para cruzar

    # Torneo 1
    for x in range(len(generacion_anterior)):
        # Tomamos el individuo actual y lo comparamos con uno random de la lista
        y = random.randint(0, len(generacion_anterior_valores) -1)
        if generacion_anterior_valores[x] >= generacion_anterior_valores[y]:
            if not checar_repetido_lista(ganadores, generacion_anterior[x]):
                ganadores.append(generacion_anterior[x])
                ganadores_valores.append(generacion_anterior_valores[x])
        else:
            if not checar_repetido_lista(ganadores, generacion_anterior[y]):
                ganadores.append(generacion_anterior[y])
                ganadores_valores.append(generacion_anterior_valores[y])
    # Torneo 2, ganadores
    ganadores_elite = list()
    ganadores_elite_valores = list()
    for x in range(len(ganadores)):
        # Tomamos el individuo actual y lo comparamos con uno random de la lista
        y = random.randint(0, len(ganadores_valores) -1)
        if ganadores_valores[x] >= ganadores_valores[y]:
            if not checar_repetido_lista(ganadores_elite, ganadores[x]):
                ganadores_elite.append(ganadores[x])
                ganadores_elite_valores.append(ganadores_valores[x])
        else:
            if not checar_repetido_lista(ganadores_elite, ganadores[y]):
                ganadores_elite.append(ganadores[y])
                ganadores_elite_valores.append(ganadores_valores[y])

    # Torneo 3, ganadores
    campeones = list()
    campeones_valores = list()
    for x in range(len(ganadores_elite)):
        # Tomamos el individuo actual y lo comparamos con uno random de la lista
        y = random.randint(0, len(ganadores_elite_valores) -1)
        if ganadores_elite_valores[x] >= ganadores_elite_valores[y]:
            if not checar_repetido_lista(campeones, ganadores_elite[x]):
                campeones.append(ganadores_elite[x])
                campeones_valores.append(ganadores_elite_valores[x])
        else:
            if not checar_repetido_lista(campeones, ganadores_elite[y]):
                campeones.append(ganadores_elite[y])
                campeones_valores.append(ganadores_elite_valores[y])
    # Cruzar
    generacion_nueva = list()
    for x in range(len(campeones)):
        # Cruzamos con dos ganadores al azar
        y = random.randint(0, len(campeones) -1)
        z = random.randint(0, len(campeones) -1)

        hijo1 = cruzar_individuos(campeones[x], campeones[y])
        hijo2 = cruzar_individuos(campeones[x], campeones[z])

        if not checar_repetido_lista(generacion_nueva, hijo1):
            generacion_nueva.append(hijo1)
        if not checar_repetido_lista(generacion_nueva, hijo2):
            generacion_nueva.append(hijo2)
    
    # Mutar
    for x in range(len(campeones)):
        mutacion = mutar_individuo(campeones[x])

        if not checar_repetido_lista(generacion_nueva, mutacion):
            generacion_nueva.append(mutacion)

    campeon_maximo = encontrar_maximo(generacion_anterior, generacion_anterior_valores)

    if not checar_repetido_lista(generacion_nueva, generacion_anterior[campeon_maximo]):
            generacion_nueva.append(generacion_anterior[campeon_maximo])

    print(interpretar_individuo(generacion_anterior[campeon_maximo]))

    return generacion_nueva

def checar_dentro_tablero(tupla, tamaño_tablero):
    if tupla[0] >= 0 and tupla[0] < tamaño_tablero:
        if tupla[1] >= 0 and tupla[1] < tamaño_tablero:
            return True
    return False

def checar_repetidos_tuplas(lista_tuplas, individuo_tupla):
    for i in range(len(lista_tuplas)):
        if lista_tuplas[i][0] == individuo_tupla[0]:
            if lista_tuplas[i][1] == individuo_tupla[1]:
                return True
    return False

# se envia el individuo en una lista de tuplas, en otras palabras una lista de movimientos
def evaluar_individuo(individuo, tamaño_tablero): 
    individuo_interpretado = interpretar_individuo(individuo)
    casillas_exploradas_validas = list()
    valor_individuo = 0
    for i in range(len(individuo_interpretado)):
        if checar_dentro_tablero(individuo_interpretado[i], tamaño_tablero):
            if not checar_repetidos_tuplas(casillas_exploradas_validas, individuo_interpretado[i]):
                casillas_exploradas_validas.append(individuo_interpretado[i])
                valor_individuo = valor_individuo + 1  
    return valor_individuo

def se_alcanzo_solucion(poblacion_valores, numero_casillas):
    for i in range(len(poblacion_valores)):
        if poblacion_valores[i] == numero_casillas:
            return True

    return False

def algoritmo_genetico_KT():
    tamaño_individuo = tamaño_tablero*tamaño_tablero*3

    # Ya tenemos una poblacion inicial
    poblacion_inicial = generarPoblacionInicial(tamaño_individuo)
    poblacion_inicial_valores = list()
    for i in range(len(poblacion_inicial)):
        poblacion_inicial_valores.append(evaluar_individuo(poblacion_inicial[i], tamaño_tablero))
    
    generacion_nueva_valores = list()
    individuos_aptos = list()
    individuos_aptos_valor = list()
    generacion_anterior = list(poblacion_inicial)
    generacion_anterior_valores = list(poblacion_inicial_valores)

    max_valor_encontrado = 0
    for gen in range(generaciones_max):
        print(f"Gen {gen+1}")
        generacion_nueva_valores.clear()
        individuos_aptos.clear()
        individuos_aptos_valor.clear()
        # Cruzamos y mutamos para crear una nueva generacion
        generacion_nueva = generar_hijos(generacion_anterior, generacion_anterior_valores, gen)
        # Evaluamos la nueva generacion
        for i in range(len(generacion_nueva)):
            generacion_nueva_valores.append(evaluar_individuo(generacion_nueva[i], tamaño_tablero))
        
        generacion_anterior = list(generacion_nueva)
        generacion_anterior_valores = list(generacion_nueva_valores)

        if se_alcanzo_solucion(generacion_anterior_valores, tamaño_tablero*tamaño_tablero):
            break
        individuo_solucion_posicion = encontrar_maximo(generacion_anterior, generacion_anterior_valores)
        print(f" VALOR MAX DE LA GEN: {generacion_anterior_valores[individuo_solucion_posicion]}")
        if max_valor_encontrado < generacion_anterior_valores[individuo_solucion_posicion]:
             max_valor_encontrado = generacion_anterior_valores[individuo_solucion_posicion]

    individuo_solucion_posicion = encontrar_maximo(generacion_anterior, generacion_anterior_valores)
    print(f" Maximo valor encontrado: {max_valor_encontrado} / {tamaño_tablero*tamaño_tablero}")
    print(f" Con un valor de: {generacion_anterior_valores[individuo_solucion_posicion]}")
    print(interpretar_individuo(generacion_anterior[individuo_solucion_posicion]))

    return interpretar_individuo(generacion_anterior[individuo_solucion_posicion]), tamaño_tablero, max_valor_encontrado

start = time.time()
genetico_resultado, tamaño_tablero, max_valor_encontrado = algoritmo_genetico_KT()
end = time.time()

tablero_matriz = [([0]*tamaño_tablero) for i in range(tamaño_tablero)]

if max_valor_encontrado == tamaño_tablero*tamaño_tablero:
    for nodo in range(len(genetico_resultado)):
        tablero_matriz[genetico_resultado[nodo][0]][genetico_resultado[nodo][1]] = nodo

    for i in range(len(tablero_matriz)):
        print(tablero_matriz[i])
else:
    print(" No se encontro la solucion.")

print(f"Tiempo de ejecucion: {end - start}")
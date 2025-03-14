#Notacion asintotica
#busqueda lineal y busqueda binaria
#Analisis complejidad
#comparamos busqueda lineal con busqueda binaria
import time #permite hacer calculos de tiempo
import random #genera alietoriedad
#mejor caso al inicio
def busquda_lineal(arr, objetivo): #arr es array o vector
    for i, num in enumerate(arr):
        if num == objetivo:
            return i
        
    return -1  #el valor no fueencontrado 
#definios busqueda binaria, peor caso en los etremos, mejor caso en la mitad
def busqueda_binaria (arr, objetivo):
    inicio, fin = 0, len(arr) - 1
    while inicio <= fin:
        medio = int((inicio + fin)/2)
        if arr[medio] == objetivo:
            return medio
        elif arr[medio]< objetivo:
            inicio = medio + 1 
        else:
            fin = medio - 1
            
    return -1 #no se encontro elemento
#😓Generar los datos para la prueba
n = 10**6 #Generar la lista de un millon de elementos
datos = sorted(random.sample(range(n*10), n))#lista para la busqueda ordenar
objetivo = random.choice(datos)#elegimos un valor al azar

#🥪Medicion de tiempo lineal
inicio = time.time()#Inicia cuenta tiempo
busquda_lineal(datos, objetivo)
fin = time.time()#Detenemos el cronometro
tiempo_lineal = fin - inicio # calculo del tiempo lineal

#🍜Medicion de tiempo binario
inicio = time.time()#inicia cuenta tiempo
busqueda_binaria(datos, objetivo)
fin = time.time()#Detenemos el cronometro
tiempo_binario = fin - inicio

#🖨imprimir los resultados
print(f"Busqueda lineal (O(n)): {tiempo_lineal:0.6f} segundos")
print(f"Busqueda binaria (O(log n)): {tiempo_binario:0.6f} segundos")

#Este eejercio tiene como proposito identificar datos procesos y resultados
#Funcion paa calcular el perimetro de un triangulo
def calcular_perimetro(a, b, c):
    return a + b + c
#entradda d los lados del triangulo
lado1 =float(input("Ingrese la ongitud del lado 1: "))
lado2 =float(input("Ingrese la ongitud del lado 2: "))
lado3 =float(input("Ingrese la ongitud del lado 3: "))
#calcuar el perimetro
perimetro = calcular_perimetro(lado1, lado2, lado3)
#mostrar el resultado
print (f"El perimetro del triangulo es: {perimetro}")
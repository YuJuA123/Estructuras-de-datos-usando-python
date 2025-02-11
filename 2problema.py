#indique cual numer es el mayor
def cual_mayor(a, b):
    if a<b:
        print("El segundo numero es mas grande")
    else:
            print("El primer numero es mas grande")
    
    return
num1 = float(input("Ingrese el primer numero: "))
num2 = float(input("Ingrese el segundo numero: "))

nmayor=cual_mayor(num1, num2)
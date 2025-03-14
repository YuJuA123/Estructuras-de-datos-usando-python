#Diccionarios
#Este algortmo mostrara la informacion de una persona, y despues permite cambiar, nombre, edad, id
ditc = {
    "Nombre": "Juan perez",
    "Edad": 14,
    "Id" : 123 
}
print("Los datos del usuario son: ")
for x,y in ditc.items():
    print(x,y)

ditc["Nombre"] = input("\nPor favor escriba su nombre: ")
ditc["Edad"] = input("Por favor escriba su edad: ")
ditc["Id"] = input("Por favor escriba su id: ")
print("\nSus datos de usuario son: ")
for x,y in ditc.items():
    print(x,y)

#Tuplas
#Este algoritmo da la cantidad de elementos en una tupla de comidas, y los muestra.
tupl = ("Pizza", "Perro caliente", "Banderilla", "Gelatina")

print("La cantidad de elementos dentro del menu de comidas es: ",len(tupl))
print("\nLos elementos del menu son: ")
for x in tupl:
    print(x)
print("\n")

#Conjuntos/sets
#Este algoritmo muestra los items, y te permite añadir uno nuevo.
sEt = {"Monitor", "Teclado", "Mouse"}
print("Los elementos para computador son: ")
for x in sEt:
    print(x)
sEt.add(input("\nPor favor añada un nuevo elemnto a la lista de compras: "))
for x in sEt:
    print(x)

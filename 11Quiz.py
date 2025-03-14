#Progrma en python que amacene nombres y edades en un diccionario y luego imprima los datos de tres personas
print("Para el primer usuario: ")

dic1 = {
    "Nombre":input("Por favor ingrese su nombre: "),
    "Edad":input("Pro favor ingrese su edad: ")
}
print("\nPara el segundo usuario: ")
dic2 = {
    "Nombre":input("Por favor ingrese su nombre: "),
    "Edad":input("Pro favor ingrese su edad: ")
}
print("\nPara el tercer usuario: ")
dic3 = {
    "Nombre":input("Por favor ingrese su nombre: "),
    "Edad":input("Pro favor ingrese su edad: ")
}
print("\nLos datos del primer usuario son: ")
for x, y in dic1.items():
    print(x, y)
print("\nLos datos del segundo usuario son: ")
for x, y in dic2.items():
    print(x, y)
print("\nLos datos del tercer usuario son: ")
for x, y in dic3.items():
    print(x, y)


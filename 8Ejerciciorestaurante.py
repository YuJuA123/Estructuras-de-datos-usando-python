"""Escribe un programa en python que solicite al usuario los siguentes datos: nombre tipo string, edad tipo int, 
    total cuenta del restaurante tipo float, porcentaje de la propina a dejar tipo int. El programa debe asegurarse de 
    que los valores ingresados sean validos, debe calcular la cantidad de propina, el total a pagar, cuenta mas propina,
    y un mensaje personalisado según la edad del usuario.
    Brindele al usuario la posibilidad de elegir productos de un menú antes de calcular la propina
    """   
    #Yulieth Juanita Ariza Hernández
#Ingreso de los datos             
nombre = str(input("Por favor digite su nombre: "))
edad = int(input("Por favor digite su edad: "))
porcentajePropina = int(input("Por favor digite el porcentaje de propina que desea dejar (0-100): "))


#crear los datos
totalCuentaRes = float()


#Lssita de platos del restaurante, en listas y tuplas

platos=[
    ("Mojarra frita", 100000),
    ("Pasta con camarones", 125000),
    ("Pasta a la boloñesa", 115000),
    ("Trucha", 150000),
    ("Nuggets de pollo", 130000)
]
#menu del restaurante
print("\nLista de comidas disponibles")
for i, (comida, precio) in enumerate(platos,1):
 #f-string o cadena formateada
    print(f"{i}. {comida} - ${precio}")
    bandeja = [] #La lista va a almacenar las comidas
    comprando= True
    
while comprando:
        opcion = int(input("\nPor favor seleccione el número del producto que desea comprar (0 para salir): "))
        if opcion == 0:
            comprando = False
        elif 1 <= opcion <= len(platos):
             comida, precio = platos[opcion - 1]
             bandeja.append((comida, precio)) #Guardando en la bandeja
             print(f"¡{comida} agregado a la bandeja!")
        else:
            print("Valor no valido, intente nuevamente.")
            
            
#para calcular la cantidad sin la propina
Total_sinpropina = sum(precio for _, precio in bandeja)
print(f"\nLa cantidad a pagar sin la propina es: {Total_sinpropina}")    

#Para pagar con la propina
Propina = (Total_sinpropina/100)*porcentajePropina
totalCuentaRes=Propina+Total_sinpropina

print(f"\nLa cantidad a pagar junto con la propina es: {totalCuentaRes}")

if edad <= 18:
    print("Disfrute ;3")
elif 18 < edad <= 65:
    print("Gracias por su compra.")
else:
    print("Gracias por su compra, disfrute de un merecido descanso.")

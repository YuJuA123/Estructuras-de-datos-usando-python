"""
Descripcion del ejercicio
El usuario debe registrar su informacion personal (nombre, edad, saldo en cuenta)
Se almacenara una lista de productos disponibles en la tienda cada uno con su precio
Se permitira que el usuario agreague porductos a su carrito de compras
Se calculara el total de la copra y se verificara si el saldo del usuario es suficiente
se mostrara un resumen con los productos comprados y el saldo restante
"""
#ingreso datos
nombre = input("Ingrese nombre: ")#str
edad = int(input("Ingrese edad: "))#int
saldo = float(input("Ingrese su saldo: "))#float

#lista de porductos de la tienda
productos=[
    ("Portatil", 1200000.),
    ("Mouse", 45000),
    ("Touchpad", 60000),
    ("Monitor", 100000),
    ("Celular", 500000)
    ]
#Parte 3. Mostrar productos y permitir la compra usando listas y
#diccionarios
#carrito de compra
print("\nLista de productos disponibles: ")
for i, (producto, precio) in enumerate(productos,1):
    #f-string o cadena formateada
    print(f"{i}. {producto} - ${precio}")
    
    carrito = [] #La lista donde va a almacenar los productos
    comprando = True #variable para controlar la compra
    
while comprando:
        opcion = int(input("\nPor favor seleccione el número del producto que desea comprar (0 para salir): "))
        if opcion == 0:
            comprando = False
        elif 1 <= opcion <= len(productos):
             producto, precio = productos[opcion - 1]
             carrito.append((producto, precio)) #Guardando en el carrito de compras
             print(f"¡{producto} agregado al carrito!")
        else:
            print("Valor no valido, intente nuevamente.")
            
    #paso 4 calcular total compra
total_compra =  sum(precio for _, precio in carrito)
print(f"\nEl total de su compra es: ${total_compra}")
    #verificar si al usuario le alcanza
if saldo >= total_compra:
    saldo -= total_compra
    print("\nCompra realizada.")
else:
    print("\nSaldo insuficiente.")
    
print(f"Su saldo restante es: {saldo}")
        
        
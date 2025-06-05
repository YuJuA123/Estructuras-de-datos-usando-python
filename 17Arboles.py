#definimos la clase nodo para representar cada elemento del arbol
class Nodo:
    #asignamos un valor a cada nodo
    def __init__(self, valor):
        #cada nodo tendra un valor
        self.valor = valor
        #Referenciamos izquierda
        self.izquierda = None
        #Referenciamos derecha
        self.derecha = None
    
    #definimos función para iniciar recorrido de izquierda a derecha
def recorrido_inorden(nodo):
    if nodo is not None:
        #Pasamos por el lado izquierdo
        recorrido_inorden(nodo.izquierda)
        print(nodo.valor)
        recorrido_inorden(nodo.derecha)
            
#creamos los valores de los nodos
#Creamos nodo raiz

raiz = Nodo(10)
    #creamos los hijos izq y der

raiz.izquierda = Nodo(5)
raiz.derecha = Nodo(20)
    
    # Agregar mas niveles
raiz.izquierda.izquierda = Nodo(3)
raiz.izquierda.derecha = Nodo(7)
raiz.derecha.derecha = Nodo(25)
raiz.derecha.izquierda = Nodo(15)
print("El recorrido del arbol es: ")
recorrido_inorden(raiz)
def insertar_nodo(raiz,valor):
    if raiz is None:
        return Nodo(valor)
    if valor < raiz.valor:
        raiz.izquierda = insertar_nodo(raiz.izquierda,valor)
    elif valor > raiz.valor:
        raiz.derecha = insertar_nodo(raiz.derecha, valor)
    return raiz
    
def llenado_de_arbol():
    raiz = None
    max_importado = 0
    print("El primer valor sera la raiz.")
    while max_importado < 7:
        entrada = input("Por favor ingrese un valor: ")
        try:
            valor = int(entrada)
            raiz = insertar_nodo(raiz,valor)
            max_importado += 1
        except ValueError:
            print("Entrada incorrecta, por favor ingrese un valor entero.")
    print("El recorrido del arbol es: ")
    recorrido_inorden(raiz)
    
llenado_de_arbol()

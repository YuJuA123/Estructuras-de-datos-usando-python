#cola con listas enlazadas
print("Cola con listas")
print()
class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None #crea puntero
        
class Cola:
    def __init__(self):
        self.frente = None
        self.final = None
        
    def encolar(self, dato):
        nuevo_nodo= Nodo(dato)
        if self.final is None:
            self.frente = self.final= nuevo_nodo
        else:
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo
            
    def desencolar(self):
        if self.frente is None:
            print("La cola esta vacia")
            return None
        dato = self.frente.dato
        self.frente = self.frente.siguiente
        if self.frente is None:
            self.final = None
        return dato
    
    def esta_vacia(self):
        return self.frente is None
    
    
cola = Cola()
cola.encolar(10)
cola.encolar(20)
cola.encolar(30)
print(cola.desencolar())
print(cola.desencolar())
print(cola.desencolar())

#cola con vectores
input()
print()
print("Cola con vector")
print()

class ColaVector:
    def __init__(self):
        self.cola = []
        
    def encolar(self,dato):
        self.cola.append(dato)
        
    def desencolar(self):
        if not self.es_vacio():
            return self.cola.pop(0)
        else:
            return "La cola esta vacía"
        
    def es_vacio(self):
        return len(self.cola) == 0
    
    def tamaño(self):
        return len(self.cola)
    
cola = ColaVector()
cola.encolar(1)
cola.encolar(2)
cola.encolar(3)
print(cola.desencolar())
print(cola.desencolar())
print(f"Tamaño actual: {cola.tamaño()}")

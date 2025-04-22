pila = []
ecuacion = input("Por favor escriba una ecuación: ")
listaecuacion=list(ecuacion)
error = False
for i in listaecuacion:
    if i=="(" or i=="[" or i =="{":
        pila.append(i)
    elif i ==")":
        if not pila or pila[-1]!="(":
            print("No esta correcta la ecuación")
            error = True
            break
        else:
            pila.pop()
    elif i =="]":
        if not pila or pila[-1]!="[":
            print("No esta correcta la ecuación")
            error = True
            break
        else:
            pila.pop()
    elif i =="}":
        if not pila or pila[-1]!="{":
            print("No esta correcta la ecuación")
            error = True
            break
        else:
            pila.pop()
if not error:
    if not pila:
        print("La ecuación está correcta")
    else:
        print("Error: símbolos sin cerrar")

from time import sleep
from typing import List,Any

def validarOpcionNumerica(opt:str,max:int,) -> bool:
    "Verifica que la opción elegida sea válida"
    try: 
        opt_int = int(opt)
        return (opt_int>=1 and opt_int<=max)  
    except ValueError:
        return False 
    
def buscarPorNombre(nombre:str,lista:List) -> Any:
    "Busca un elemento en una lista por su nombre"
    
    # Se buscan todas las coincidencias
    listaCoincidencias = []
    for elemento in lista:
        if nombre.lower() in elemento.nombre.lower():
            listaCoincidencias.append(elemento)
    
    # Se opera según la cantidad de coincidencias
    if len(listaCoincidencias) == 0:
        print(f"\nNo hubieron coincidencias buscando {nombre}")
        return
    elif len(listaCoincidencias) == 1:
        print(f"\nSe encontró 1 coicidencia: {listaCoincidencias[0].nombre}")
        return listaCoincidencias[0]
    
    # Si hay más de un resultado, los listamos y le pedimos al usuario elegir
    else:
        print("Listando coincidencias...")
        sleep(1)

        # Se listan las coincidencias
        for idx, elemento in enumerate(listaCoincidencias):
            print(f"\t{idx+1}) {elemento.nombre}")
        
        opt = input(f"> Elija una opción [1-{len(listaCoincidencias)}]: ")
        if validarOpcionNumerica(opt,len(listaCoincidencias)):
            print(f"\nSe encontró 1 coicidencia: {nombre}")
            return listaCoincidencias[int(opt)-1]
        else:
            print("\nHa ingresado una opción inválida\n")
            return


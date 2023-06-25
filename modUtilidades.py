from typing import List,Any
from simple_term_menu import TerminalMenu

def printMenu(lineas:List[str]) -> int:
    
    # Lista las opciones
    terminal_menu = TerminalMenu([f"{idx}) {opt}" for idx,opt in enumerate(lineas[1:],1)],title=f"\n{lineas[0]}")
    return terminal_menu.show() + 1  # type: ignore
    
def validarOpcionNumerica(opt:str,max:int,) -> bool:
    "Verifica que la opción elegida sea válida"

    return opt.isdigit() and (int(opt)>=1 and int(opt)<=max)  
    
def buscarPorNombre(nombre:str,lista:List[Any]) -> Any:
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
    elif len(listaCoincidencias) == 1 and nombre != "":
        print(f"\nSe encontró 1 coincidencia: {listaCoincidencias[0].nombre}")
        return listaCoincidencias[0]
    
    # Si hay más de un resultado, los listamos y le pedimos al usuario elegir
    else:
        terminal_menu = TerminalMenu([f"{idx}) {opt.nombre}" for idx,opt in enumerate(listaCoincidencias,1)],title="Listando Coincidencias")
        return listaCoincidencias[terminal_menu.show()] # type: ignore


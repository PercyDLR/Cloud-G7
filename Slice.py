import modUtilidades as util
from typing import List

class Slice:
    def __init__(self,nombre:str) -> None:
        self.nombre = nombre

# Lista provisional
listaSlices:List[Slice] = [Slice("xd"),Slice("slice1")]

## Iniciamos el CRUD

def listarSlices():
    "Lista los slices activos"
    for idx,sliceObj in enumerate(listaSlices):
        print(f"\t{idx+1}) {sliceObj.nombre}")

def crearSlice():
    """Crea un slice, preguntando por la topología base, y los
    equipos iniciales"""
    
    nameSlice = input("Ingrese nombre del Slice a crear: ")
    
    # TODO: Código para crear el slice
    print(f"\nCreando slice {nameSlice}...")
    listaSlices.append(Slice(nameSlice))
    print(f"Slice {nameSlice} creado")

def editarSlice():
    nombre = input("Ingrese el nombre de un slice [Por defecto: Listar todos]: ")
    sliceObj:Slice = util.buscarPorNombre(nombre,listaSlices)

    if sliceObj is None:
        return

    while True:
        print("\nAcciones disponibles para realizar:")
        print("\t1) Agregar nodo")
        print("\t2) Agregar enlace")
        print("\t3) Agregar VM")
        print("\t4) Salir")
        
        # Se pide elegir una opción
        opt = input(f"> Elija una opción [1-4]: ")
        if util.validarOpcionNumerica(opt,4):
            print(f"\nEditando slice {sliceObj.nombre}")
        else:
            print("Debe ingresar una opción válida")
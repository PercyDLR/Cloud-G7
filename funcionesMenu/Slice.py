import modUtilidades as util
from typing import List
from dataclasses import dataclass
from funcionesMenu.reglasSeguridad import GrupoSeguridad
from time import sleep

@dataclass
class Slice:
    nombre: str
    topologia: str
    secGroup: str

# Lista provisional
listaSlices:List[Slice] = []



def listarSlices():
    "Lista los slices activos"

    print("")
    for idx,sliceObj in enumerate(listaSlices):
        print(f"\t{idx+1}) {sliceObj.nombre}")

def crearSlice(listaGrupos:List[GrupoSeguridad]) -> None:
    """Crea un slice, preguntando por la topología base, y los
    equipos iniciales"""
    
    # Petición de datos
    nameSlice = input("\n> Ingrese nombre del Slice a crear: ").strip()
    
    # Se elige una topología
    listaTopologias = ["Elija una topologia base para el slice:",
                       "Lineal", "Malla", "Arbol", "Anillo", "Bus"]
    opt = util.printMenu(listaTopologias)
    topologia = listaTopologias[opt]

    # Se crea un nuevo grupo de seguridad
    if len(listaGrupos) == 0:

        print("\nNo existen grupos de seguridad. Creando uno nuevo...")

        while True:
            nombre = input("\n> Ingrese un nombre para el grupo de seguridad: ").strip()

            if nombre != "":
                print("\nCreando Grupo de seguridad...")
                grupo = GrupoSeguridad(nombre,[])
                listaGrupos.append(grupo)
                sleep(1)
                print(f"Grupo {nombre} creado exitosamente!")
                break
            
            else:
                print("\nDebe ingresar un nombre para el grupo")
    
    # Se elije un grupo ya existente
    else:
        nombre = input("> Ingrese el nombre del grupo [default: Listar Todos]: ").strip()
        grupo:GrupoSeguridad = util.buscarPorNombre(nombre,listaGrupos)
    
    # Se crea el Slice
    print(f"\nCreando slice {nameSlice}...")
    sleep(1)

    listaSlices.append(Slice(nameSlice,topologia,grupo.nombre))
    print(f"Slice {nameSlice} creado")

def editarSlice():
    nombre = input("Ingrese el nombre de un slice [Por defecto: Listar todos]: ").strip()
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
        opt = input(f"> Elija una opción [1-4]: ").strip()
        if util.validarOpcionNumerica(opt,4):
            print(f"\nEditando slice {sliceObj.nombre}")


        else:
            print("Debe ingresar una opción válida")
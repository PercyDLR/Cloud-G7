import modUtilidades as util
from typing import List, Dict, Any
from dataclasses import dataclass
from funcionesMenu.reglasSeguridad import GrupoSeguridad
from time import sleep
import json
from random import choices
from funcionesMenu.editSlice import currentSlice

@dataclass
class Slice:
    nombre: str
    topologia: str
    secGroup: str

def mostrarRequest(method:str, body:Dict[str,Any], action:str, razon:str) -> bool:
    print(f"Method: {method}\nURL: https://10.20.17.101/orquestador")

    body["user_token"] = "aidba8hd8g38bd2397gf29323d2"      # info usuario
    body["action"] = action                                 # info acción

    print(f"Body:\n{json.dumps(body,indent=4)}")            # Se imprime el body
    sleep(2)

    # Imprime la respuesta del servidr
    respuesta = choices(["exito","error"],weights=[1,0])[0]
    print(f"Respuesta: {respuesta}")
    if respuesta=="error": 
        print(f"Ha ocurrido un error **{razon}**")
        return False
    return True

def listarSlices(listaSlices:List[Slice]):
    "Lista los slices activos"

    if mostrarRequest("GET",{},"listSlices","Hubo un problema de conexión"):
        print("")
        if len(listaSlices) == 0:
            print("No existe ningún slice")
            return

        for idx,sliceObj in enumerate(listaSlices):
            print(f"\t{idx+1}) {sliceObj.nombre}")

def crearSlice(listaSlices:List[currentSlice],listaGrupos:List[GrupoSeguridad]) -> None:
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

                if mostrarRequest("POST",{"nombre":nombre},"newSecGroup","Error de conexión"):
                    listaGrupos.append(grupo)
                    sleep(1)
                    print(f"Grupo {nombre} creado exitosamente!")
                break
            
            else:
                print("\nDebe ingresar un nombre para el grupo")
    
    # Se elije un grupo ya existente
    else:
        nombre = input("> Ingrese el nombre del grupo [default: Listar Todos]: ").strip()
        while (grupo:= util.buscarPorNombre(nombre,listaGrupos)) == None:
            print("Opción no valida...")
        
        
    
    # Se crea el Slice
    print(f"\nCreando slice {nameSlice}...")
    if mostrarRequest("POST",{"nombre":nameSlice,"topologia":topologia,"secGroup":grupo.nombre},
                      "newSlice", "El servidor no pudo procesar su solicitud. Vuelva a intentarlo más tarde"):
        sleep(1)
        #listaSlices.append(Slice(nameSlice,topologia,grupo.nombre))
        listaSlices.append(currentSlice(nameSlice,topologia,grupo.nombre,"",[],[]))
        print(f"Slice {nameSlice} creado")
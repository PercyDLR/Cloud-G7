import modUtilidades as util
import funcionesMenu.editSlice as editSlice
import funcionesMenu.Slice as s
import funcionesMenu.Imagen as img
import funcionesMenu.reglasSeguridad as r
import clases
import subprocess
import json
import hashlib
import getpass
from typing import Dict, List, Any

def login() -> None:
    "Implementa un logueo básico"

    for intentos in range(3,0,-1):
        
        username = input("\nIngrese su usuario: ").strip()
        password = hashlib.sha256(getpass.getpass("Ingrese su contraseña: ").encode()).hexdigest()
        #password is 12345
        if(username=="grupo7" and 
            password=="5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5"):
            return
        else:
            print(f"\n** El usuario indicado no existe, {intentos-1} intentos restantes")
    
    print("\nEl logueo falló 3 veces. Por favor revise sus credenciales y vuelva a intentarlo más tarde")
    exit()

def obtenerDatos() -> Dict[str, List[Any]]:
    return {"slices":[],"gruposSeguridad":[],"imagenes":[]}

# Función Main
if __name__=="__main__":
    

    # Presentación del Grupo
    print("\n################ Orquestador G7 ################")
    print("--- Elianne P. Ticse Espinoza\t\t20185361")
    print("--- Oliver A. Bustamante Sanchez\t20190981")
    print("--- Percy De La Rosa Vera\t\t20192265")
    print("################################################")

    #login()
    datos = obtenerDatos()
    
    while True:
        opt = util.printMenu(["Opciones disponibles para realizar:",
                              "Listar slices",
                              "Crear slice",
                              "Editar slice",
                              "Configurar Grupos de Seguridad",
                              "Administrar Imágenes de Disco",
                              "Salir"])

        if opt==1:
            s.listarSlices()
        if opt==2:
            s.crearSlice(datos["gruposSeguridad"])
        if opt==3:
            editSlice.start()
        if opt==4:
            r.main(datos["gruposSeguridad"])
        if opt==5:
            img.menuImg(datos["imagenes"])
        if opt==6:
            print("Saliendo del programa...")
            break

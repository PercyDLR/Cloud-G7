from dataclasses import dataclass
from typing import List
import modUtilidades as util
from time import sleep
import time
import requests as req
import variables as var
from tabulate import tabulate
from simple_term_menu import TerminalMenu
from tkinter.filedialog import askopenfilename
from os.path import expanduser

@dataclass
class Imagen:
    nombre:str
    path:str

def menuImg() -> None:
    "Administra imagenes nuevas/existentes"

    IP_GATEWAY = var.dirrecionIP
    headers = {"Content-Type": "application/json", "X-Auth-Token": var.dic["token"]}

    while True: 
        listaImagenes = req.get(f"http://{IP_GATEWAY}:9292/v2/images?sort=name:asc&status=active",headers=headers).json()["images"]
        nombreImg = [img["name"] for img in listaImagenes]
        nombreImg.insert(0,"Salir")
        nombreImg.insert(0,"Agregar Nueva")
        nombreImg.insert(0,"Opciones para Imágenes de Disco:")

        # Se elige una opción
        opt = util.printMenu(nombreImg)

        if opt == 1:
            break

        # Crear Imagen
        elif opt == 0:
            nombreImg = input("\n> Ingrese el nombre de la imagen: ").strip()
            pathImg = askopenfilename(initialdir=expanduser('~'))
            print(pathImg)

            body = {
                "container_format": "bare",
                "disk_format": "raw",
                "name": nombreImg,
                "visibility": "community"
                }
        
            newImg = listaImagenes = req.post(f"http://{IP_GATEWAY}:9292/v2/images",headers=headers,json=body)

            if newImg.status_code == 201:
                header2 = {"Content-Type": "application/octet-stream","X-Auth-Token": var.dic["token"]}
                
                with open(pathImg,"rb") as f:
                    print("\nCreando imagen...")
                    response = req.put(f"http://{IP_GATEWAY}:9292/v2/images/{newImg.json()['id']}/file",headers=header2,data=f)

                if response.status_code == 204:
                    print(f"Se ha agregado la imagen {nombreImg} exitosamente.")
                else:
                    print(f"Hubo un problema al cargar la imagen.")  
            else:
                print(f"Hubo un problema al crear la imagen.")
            return
                
        # Se edita una imagen existente
        imagen = listaImagenes[opt-2]

        opt2 = util.printMenu(["Opciones de la Imagen:", "Eliminar","Salir"])

        # Eliminar la imagen
        if opt2 == 0:
            print("\nEliminando imagen...")
            response = req.delete(f"http://{IP_GATEWAY}:9292/v2/images/{imagen['id']}",headers=headers)
            
            if response.status_code == 204:
                print(f"Se ha eliminado la imagen {imagen['name']} exitosamente.")
            else:
                print("La imagen no pudo ser eliminada")

    
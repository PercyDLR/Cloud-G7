from dataclasses import dataclass
from typing import List
import modUtilidades as util
from time import sleep
from os.path import exists
import json
import random
import time
import math


@dataclass
class Imagen:
    nombre:str
    path:str
    
def mostrarRequest(method,body,action,nombre,path):
    print(f"Method: {method}")
    print("URL: https://10.20.17.101/orquestador")
    body["user_token"] = "aidba8hd8g38bd2397gf29323d2"
    body["action"] = action
    body["name"] = nombre
    body["path"] = path
    
    print(f"Body:\n{json.dumps(body,indent=4)}")
    print("Send and waiting for response")
    time.sleep(2)
    respuesta = random.choices(["exito","error"],weights=[0.67,0.33])[0]
    print(f"Response: {respuesta}")
    if respuesta=="error": 
        if action=="crearImg":
            print(f"\nNo existe imagen de disco en la ruta {path}")    
        else:
            print(f"\nNo se ha podido realizar la eliminación de la imagen.")   
        return True
    return False

def menuImg(listaImagenes: List[Imagen]) -> None:
    "Administra imagenes nuevas/existentes"

    while True:
        opt = util.printMenu(["Configuración de imagenes:",
                            "Listar imagenes",
                            "Importar imagen",
                            "Eliminar imagen",                      
                            "Salir"])
        if opt == 1:
            sleep(1)
            print("")
            if len(listaImagenes) == 0:
                print("No hay imágenes de disco almacenadas")

            for idx, imagen in enumerate(listaImagenes,1):
                print(f"\t{idx}) {imagen.nombre} ({imagen.path})")

        if opt == 2:
            nombreImg = input("\n> Ingrese el nombre de la imagen: ").strip()
            path = input("> Ingrese la ubicación de la imagen [web o local(absoluta)]: ").strip()

            # Si es web, se guarda el link
            # Si es un archivo local, guardamos su ubicación
            print("\nImportando imagen...")
            img = Imagen(nombreImg,path)
            sleep(1)
            error = mostrarRequest("POST",{"name":img.nombre},"crearImagen",img.nombre,img.path)
            time.sleep(2)
            if(error): return
            listaImagenes.append(img)
                
            
        # Se edita un grupo de seguridad existente
        if opt == 3:
            nombre = input("\n> Ingrese un nombre de la imagen: ").strip()
            imagen = util.buscarPorNombre(nombre,listaImagenes)
            #Codigo para eliminar imagen
            print("\nEliminando imagen...")
            sleep(1)
            error = mostrarRequest("POST",{"name":imagen.nombre},"eliminarImg",imagen.nombre,imagen.path)
            time.sleep(2)
            if(error): return
            listaImagenes.remove(imagen)
        
        if opt == 4:
            print("\nSaliendo de la configuración de Imagenes...")
            break

    
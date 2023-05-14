from dataclasses import dataclass
from typing import List
import modUtilidades as util
from time import sleep
from os.path import exists

@dataclass
class Imagen:
    nombre:str
    path:str

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
            if exists(path):
                print("\nImportando imagen...")
                listaImagenes.append(Imagen(nombreImg,path))
                sleep(1)
                print(f"Se ha importando la imagen {nombreImg} exitosamente.")
            else:
                print(f"\nNo existe imagen de disco en la ruta {path}")
            
        # Se edita un grupo de seguridad existente
        if opt == 3:
            nombre = input("\n> Ingrese un nombre de la imagen: ").strip()
            imagen = util.buscarPorNombre(nombre,listaImagenes)
            
            #Codigo para eliminar imagen
            print("\nEliminando imagen...")
            listaImagenes.remove(imagen)
            sleep(2)
            print(f"Se ha eliminado la imagen {nombre} exitosamente.")
        
        if opt == 4:
            print("\nSaliendo de la configuración de Imagenes...")
            break

    
from dataclasses import dataclass
from typing import List
import modUtilidades as util
from time import sleep
from ipaddress import ip_address

@dataclass
class Imagen:
    nombreImg:str
    path:str

def menuImg(listaImagenes):
    "Administra imagenes nuevas/existentes"

    opt = util.printMenu(["Configuración de imagenes:",
                          "Listar imagenes",
                          "Importar imagen",
                          "Eliminar imagen",                      
                          "Salir"])

    while True:
        if opt == 1:
            sleep(1)
            for idx, imagen in enumerate(listaImagenes,1):
                print(f"\t{idx}) {imagen.nombreImg}")

        if opt == 2:
            path = input("> Ingrese dirección de la imagen: ")
            nombreImg = input("> Ingrese el nombre de la imagen: ")
            print("Importando imagen...")
            listaImagenes.append(Imagen(nombreImg,path))
            sleep(2)
            print(f"Se ha importando la imagen {nombreImg} exitosamente.")
            
            
        # Se edita un grupo de seguridad existente
        if opt == 3:
            nombre = input("> Ingrese un nombre de la imagen: ")
            imagen = util.buscarPorNombre(nombre,listaImagenes)
            
            #Codigo para eliminar imagen
            print("Eliminando imagen...")
            listaImagenes.remove(imagen)
            sleep(2)
            print(f"Se ha eliminado la imagen {nombre} exitosamente.")
        
        if opt == 4:
            print("Saliendo de la configuración de Imagenes...")
            break

    
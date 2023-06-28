from dataclasses import dataclass
import modUtilidades as util
import requests as req
import variables as var

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
        
        nombreImg.insert(0,None)
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
            pathImg = util.selectorArchivos([("Imagen de disco",".qcow .qcow2 .img .raw .iso .cso .vdi .vhd .bin"),("Todos los archivos","*")])

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
                    util.printError(f"Hubo un problema al cargar la imagen.")  
            else:
                util.printError(f"Hubo un problema al crear la imagen.")
            return
                
        # Se edita una imagen existente
        imagen = listaImagenes[opt-3]

        opt2 = util.printMenu([f"Opciones de la Imagen {imagen['name']}:", "Eliminar","Salir"])

        # Eliminar la imagen
        if opt2 == 0:
            print("\nEliminando imagen...")
            response = req.delete(f"http://{IP_GATEWAY}:9292/v2/images/{imagen['id']}",headers=headers)
            
            if response.status_code == 204:
                print(f"Se ha eliminado la imagen {imagen['name']} exitosamente.")
            else:
                util.printError(f"La imagen no pudo ser eliminada ({response.status_code})")
                # print(response.json())
import requests as req
import variables as var
import modUtilidades as util

def imprimirTabla(objeto:dict) -> None:
    print(objeto)
    return objeto["id"]


def menuFlavor() -> None:
    
    IP_GATEWAY = var.dirrecionIP
    headers = {"Content-Type": "application/json", "X-Auth-Token": var.dic["token"]}

    while True:
        response = req.get(f"http://{IP_GATEWAY}:8774/v2.1/flavors/detail",headers=headers)
        flavorsList = response.json()["flavors"]

        # Crea el menú de selección de flavors
        menu_items = [f"{flavor['name']}|{['flavor',flavor]}" for flavor in flavorsList]
        # print(menu_items[0].split("|")[1])

        menu_items.insert(0,"Salir")
        menu_items.insert(0,"Agregar Nuevo")
        menu_items.insert(0,"Opciones para Flavors")

        opt = util.printMenu(menu_items, comando="python3 modUtilidades.py {}")
        
        # TODO: Opciones de Flavor

        # Crear flavor
        if opt == 0:
            pass
        
        # Salir
        if opt == 1:
            break

        # Elegir un flavor
        else:
            pass

        
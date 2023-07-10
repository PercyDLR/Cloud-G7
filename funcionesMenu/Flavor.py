import requests as req
import variables as var
import modUtilidades as util

def menuFlavor() -> None:
    
    IP_GATEWAY = var.dirrecionIP
    headers = {"Content-Type": "application/json", "X-Auth-Token": var.dic["token"]}

    while True:
        response = req.get(f"http://{IP_GATEWAY}:8774/v2.1/flavors/detail",headers=headers)
        flavorsList = response.json()["flavors"]

        # Crea el menú de selección de flavors
        menu_items = [f"{flavor['name']}|{['flavor',flavor]}" for flavor in flavorsList]
        # print(menu_items[0].split("|")[1])

        menu_items.insert(0,None)
        menu_items.insert(0,"Salir")
        menu_items.insert(0,"Agregar Nuevo")
        menu_items.insert(0,"Opciones para Flavors")

        opt = util.printMenu(menu_items, comando="python3 modUtilidades.py {}")
        
        # Salir
        if opt == 1:
            break
        # Crear flavor
        elif opt == 0:

            nombre = util.printInput("\nIngrese un nombre para el Flavor: ").strip()

            idx = util.printMenu(["Elija la cantidad de memoria RAM:",
                                  "128 MiB","256 MiB","512 MiB","1 GiB","2 GiB"])
            ram = ["128","256","512","1024","2048"][idx]
            
            while True:
                try:
                    disco = int(util.printInput("Capacidad de Disco (GiB): ").strip())
                    if disco < 1 or disco > 5: 
                        raise ValueError
                    break
                except ValueError:
                    util.printError("La capacidad de disco debe ser un número entero positivo menor igual a 5 GiB")

            while True:
                try:
                    vcpus = int(util.printInput("Cantidad de VCPUs: ").strip())
                    if vcpus < 1 or vcpus > 4: 
                        raise ValueError
                    break
                except ValueError:
                    util.printError("La cantidad de VCPUs debe ser un número positivo menorigual a 4")

            body = {
                "flavor": {
                    "name": nombre,
                    "ram": ram,
                    "vcpus": vcpus,
                    "disk": disco
                }}
            
            newFlavor = req.post(f"http://{IP_GATEWAY}:8774/v2.1/flavors",headers=headers,json=body)

            if newFlavor.status_code == 200:
                util.printSuccess(f"\nSe ha agregado el flavor {nombre} exitosamente")
            else:
                util.printError(f"\nHubo un problema al crear el flavor ({newFlavor.status_code})")
                # print(newFlavor.json())

        # Opciones específicas del flavor
        else:
            flavor = flavorsList[opt-3]

            opt2 = util.printMenu([f"Opciones Flavor {flavor['name']}:","Eliminar","Salir"])

            if opt2 == 0:
                response = req.delete(f"http://{IP_GATEWAY}:8774/v2.1/flavors/{flavor['id']}",headers=headers)

                if response.status_code == 202:
                    util.printSuccess(f"\nEl flavor {flavor['name']} se eliminó exitosamente")
                else:
                    util.printError(f"\nHubo un problema al eliminar el flavor ({response.status_code})")
        
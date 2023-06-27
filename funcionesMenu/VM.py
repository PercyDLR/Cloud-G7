import requests as req
import variables as var
import modUtilidades as util
from colorama import Fore, Back, Style 
from tabulate import tabulate
from simple_term_menu import TerminalMenu


def selectFlavor(IP_GATEWAY,headers):
        
    response = req.get(f"http://{IP_GATEWAY}:8774/v2.1/flavors/detail",headers=headers)
    flavorsList = response.json()["flavors"]
    
    # Crea el menú de selección de flavors
    menu_items = [f"{flavor['name']}|{['flavor',flavor]}" for flavor in flavorsList]
    # print(menu_items[0].split("|")[1])

    menu_items.insert(0,"Salir")
    menu_items.insert(0,"Seleccione un flavor: ")
    
    opt = util.printMenu(menu_items, comando="python3 modUtilidades.py {}")
    if opt == 0:
        return 
    else:
        # Muestra el menú y obtiene la selección del usuario
        selected_flavor = flavorsList[opt-1]
    
    return selected_flavor
        

def selectImage(IP_GATEWAY,headers):
    
    response = req.get(f"http://{IP_GATEWAY}:9292/v2/images?sort=name:asc&status=active",headers=headers)
    imagesList = response.json()["images"]
    
    # Crea el menú de selección de flavors
    menu_items = [image["name"] for image in imagesList]
    menu = TerminalMenu(menu_entries=menu_items, title="Seleccione una imagen: ")

    # Muestra el menú y obtiene la selección del usuario
    selected_index = menu.show()
    selected_image = imagesList[selected_index]
    
    return selected_image

def selectNetwork(IP_GATEWAY,headers):
    print("############## Seleccione una imagen ##############")
    
    res = req.get(f"http://{IP_GATEWAY}:9696/v2.0/subnets",headers=headers)
    subnetsList = res.json()["subnets"]
    
    response = req.get(f"http://{IP_GATEWAY}:9696/v2.0/networks?admin_state_up=true",headers=headers)
    networksList = response.json()["networks"]
    
    subnetsListActive = []
    
    for subnet in subnetsList:
        idNetwork = subnet["network_id"] 
        for network in networksList:
            if(network["id"]==idNetwork):
                subnet["network_name"]=network["name"]
                subnetsListActive.append(subnet)
    
    table_data = []
    for subnet in subnetsListActive:
        flavor_data = [
            subnet["network_name"],
            subnet["name"],
            subnet["cidr"],
        ]
        table_data.append(flavor_data)
    
    # Imprime la tabla
    table = tabulate(table_data, headers=["Network","Subnet", "CIDR"], tablefmt="grid")
    print(table)
    
    
    # Crea el menú de selección de flavors
    menu_items = [f"{subnet['network_name']} - {subnet['name']} - {subnet['cidr']}" for subnet in subnetsListActive]
    menu = TerminalMenu(menu_entries=menu_items, title="Seleccione una subnet: ")

    # Muestra el menú y obtiene la selección del usuario
    selected_index:int = menu.show() # type: ignore
    selected_subnet = subnetsListActive[selected_index] 
    
    return selected_subnet

def selectKeypair(IP_GATEWAY,headers):
    response = req.get(f"http://{IP_GATEWAY}:8774/v2.1/os-keypairs",headers=headers)
    keyList = response.json()["keypairs"]

    # Crea el menú de selección de flavors
    menu_items = [key["keypair"]["name"] for key in keyList]
    menu = TerminalMenu(menu_entries=menu_items, title="Seleccione una key: ")

    # Muestra el menú y obtiene la selección del usuario
    selected_index = menu.show()
    selected_key = keyList[selected_index]
    return selected_key["keypair"]
    

def selectGroup(IP_GATEWAY,headers):
    response = req.get(f"http://{IP_GATEWAY}:9696/v2.0/security-groups",headers=headers)
    sgList = response.json()["security_groups"]
    
    table_data = []
    for sg in sgList:
        flavor_data = [
            sg["name"],
            sg["description"],
        ]
        table_data.append(flavor_data)
    
    # Imprime la tabla
    table = tabulate(table_data, headers=["Name","Description"], tablefmt="grid")
    print(table)
    
    # Crea el menú de selección de flavors
    menu_items = [sg["name"] for sg in sgList]
    menu = TerminalMenu(menu_entries=menu_items, title="Seleccione un grupo de seguridad: ")

    # Muestra el menú y obtiene la selección del usuario
    selected_index = menu.show()
    selected_sg = sgList[selected_index]
    return selected_sg
    
def crearVM():
     
    IP_GATEWAY = var.dirrecionIP
    headers = {"Content-Type": "application/json", "X-Auth-Token": var.dic["token"]}
    
    while((nameVM:=util.printInput("Ingrese nombre de la VM: ").strip())==""):
        print("No puede estar vacio.")
    
    flavorVM = selectFlavor(IP_GATEWAY,headers)
    if flavorVM is None: return 
        
    imageVM = selectImage(IP_GATEWAY,headers)
    print("Imagen seleccionada")
    print("Nombre: ", imageVM["name"] )
    
    networkVM = selectNetwork(IP_GATEWAY,headers)
    print("Red seleccionada")
    print("Network: ", networkVM["network_name"] )
    print("Subnet: ", networkVM["name"] )
    print("CIDR: ", networkVM["cidr"] )

    keyVM = selectKeypair(IP_GATEWAY,headers)
    print("Key seleccionada")
    print("Nombre: ", keyVM["name"] )
    
    sgVM = selectGroup(IP_GATEWAY,headers)
    print("Security Group seleccionado")
    print("Nombre: ",sgVM["name"])
    
    body = {
            "server" : {
                "name": nameVM,
                "imageRef" : imageVM["id"],
                "flavorRef" : flavorVM["id"],
                "key_name": keyVM["name"],
                "networks" : [{
                    "uuid" : networkVM["network_id"],
                }],
                "security_groups": [{
                    "name": sgVM["name"]
                }]
            }
        }
    
    response = req.post(f"http://{IP_GATEWAY}:8774/v2.1/servers",json=body,headers=headers)
    
    if response.status_code == 202:
        print(f"\nRegla agregada exitosamente!")
    else:
        print(f"\nHubo un problema, error {response.status_code}")
    
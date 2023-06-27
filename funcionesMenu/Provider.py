import requests as req
import modUtilidades as util
from ipaddress import ip_network
import variables as var
from tabulate import tabulate
from random import randint

class Red:
    def __init__(self,status_code) -> None:
        self.status_code = status_code

def menuProvider():
    "Muestra opciones de configuración de red provider"
    
    while True:
        IP_GATEWAY = var.dirrecionIP
        headers = {"Content-Type": "application/json", "X-Auth-Token": var.dic["token"]}
        existe = False
        nuevaRed = Red(201)
        red = {}

        # Querys
        response = req.get(f"http://{IP_GATEWAY}:9696/v2.0/networks?admin_state_up=true",headers=headers)
        networksList = response.json()["networks"]

        '''
    networksList = [
    {
        "id":"48b16c1a-82de-4ab6-bc55-48f623717bba",
        "name":"tel141",
        "tenant_id":"bec910e1cbc44629bd718c929328aaa0",
        "admin_state_up":true,
        "mtu":1500,
        "status":"ACTIVE",
        "subnets":[
            "1312d3eb-9368-4ec8-a763-f25b9ae1fc82"
        ],
        "shared":true,
        "availability_zone_hints":[
            
        ],
        "availability_zones":[
            "nova"
        ],
        "ipv4_address_scope":"None",
        "ipv6_address_scope":"None",
        "router:external":true,
        "description":"",
        "port_security_enabled":true,
        "tags":[
            
        ],
        "created_at":"2023-06-03T15:05:32Z",
        "updated_at":"2023-06-03T15:09:22Z",
        "revision_number":2,
        "project_id":"bec910e1cbc44629bd718c929328aaa0",
        "provider:network_type":"flat",
        "provider:physical_network":"provider",
        "provider:segmentation_id":"None"
    },
    ...
    ]
        '''

        res = req.get(f"http://{IP_GATEWAY}:9696/v2.0/subnets",headers=headers)
        
        # Se mapean las subnets según su red
        subnetList:dict[str,list] = {}
        for subnet in res.json()["subnets"]:

            if subnet["network_id"] not in subnetList:
                subnetList[subnet["network_id"]] = []

            subnetList[subnet["network_id"]].append(subnet)
            
        '''
    [
    {
        "id":"1312d3eb-9368-4ec8-a763-f25b9ae1fc82",
        "name":"tel141",
        "tenant_id":"bec910e1cbc44629bd718c929328aaa0",
        "network_id":"48b16c1a-82de-4ab6-bc55-48f623717bba",
        "ip_version":4,
        "subnetpool_id":"None",
        "enable_dhcp":true,
        "ipv6_ra_mode":"None",
        "ipv6_address_mode":"None",
        "gateway_ip":"172.20.15.1",
        "cidr":"172.20.15.0/24",
        "allocation_pools":[
            {
                "start":"172.20.15.101",
                "end":"172.20.15.250"
            }
        ],
        "host_routes":[
            
        ],
        "dns_nameservers":[
            "8.8.4.4"
        ],
        "description":"",
        "service_types":[
            
        ],
        "tags":[
            
        ],
        "created_at":"2023-06-03T15:09:22Z",
        "updated_at":"2023-06-03T15:09:22Z",
        "revision_number":0,
        "project_id":"bec910e1cbc44629bd718c929328aaa0"
    },
    ...
    ]
        '''

        nombreRedes = [f"{red['name']}|" for red in networksList]

        opt = util.printMenu(["Opciones de Configuración de red","Agregar Nueva Red","Salir",None] + nombreRedes)

        if opt == 1: break

        # Creación de red
        elif opt == 0:
            existe = False
            nombreRed = input("\nIngrese un nombre para la red provider: ").strip()

            for red in nombreRedes[4:]:
                if nombreRed.lower() == red.split("|")[0].lower():
                    existe = True
                    break

            if existe:
                util.printError(f"La red {nombreRed} ya existe")
            
            # Se crea la red
            else:
                body = {
                    "network": {
                        "name": nombreRed,
                        "admin_state_up": True,
                        "provider:network_type": "vlan",
                        "provider:physical_network": "provider",
                        "provider:segmentation_id": randint(1,5000)
                    }
                }
                nuevaRed = req.post(f"http://{IP_GATEWAY}:9696/v2.0/networks",headers=headers,json=body)
                
                if nuevaRed.status_code == 201:
                    print(f"Red {nombreRed} creada exitosamente!")
                else:
                    util.printError(f"Hubo un problema creando la red ({nuevaRed.status_code})")
                    # print(nuevaRed.json())
        
        else:
            red = networksList[opt-3]
            subnets = subnetList[red["id"]]

            opt2 = util.printMenu([f"Opciones de la Red {red['name']}:",
                                   "Agregar Subred", "Eliminar Subred",
                                   "Eliminar Red","Salir"])
        continue



        # Se elige y valida el nombre de red
        
        coincidenciasRed = req.get(f"http://{IP_GATEWAY}:9696/v2.0/networks",headers=headers,params={"name": nombreRed}).json()
        if len(coincidenciasRed['networks']) != 0:
            print("Usando red existente...\n")
            existe = True
            red = {"network": coincidenciasRed['networks'][0]}

        # Se elige un nombre de Subred
        nombreSubred = input("Ingrese un nombre para la subred: ").strip()

        # Se especifica y valida el cidr de la subred
        while True:
            try:
                cidr = input("Ingrese el cidr de la subred [a.b.c.d/e]: ").strip()
                ip_network(cidr)
                break
            except ValueError:
                util.printError("El cidr ingresado no es válido!\n")
        
        # Se crea la red
        body = {
            "network": {
                "name": nombreRed,
                "admin_state_up": True,
                "provider:network_type": "vlan",
                "provider:physical_network": "provider",
                "provider:segmentation_id": randint(1,5000)
            }
        }

        if not existe:
            nuevaRed = req.post(f"http://{IP_GATEWAY}:9696/v2.0/networks",headers=headers,json=body)
            red = nuevaRed.json()

        if existe or nuevaRed.status_code == 201:
            print(f"Red {nombreRed} creada exitosamente!")
            
            # Se crea la subred
            body = {
                "subnet": {
                    "network_id": red["network"]["id"],
                    "name": nombreSubred,
                    "ip_version": 4,
                    "cidr": cidr
                }
            }

            nuevaSubred = req.post(f"http://{IP_GATEWAY}:9696/v2.0/subnets",headers=headers,json=body)
            if nuevaSubred.status_code == 201:
                print(f"Subred {nombreSubred} creada exitosamente!")
            else:
                print(f"\nHubo un problemaal crear la subred, error {nuevaSubred.status_code}")
        else:
            print(f"\nHubo un problema al crear la red, error {nuevaRed.status_code}")
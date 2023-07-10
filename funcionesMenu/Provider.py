import requests as req
import modUtilidades as util
from ipaddress import ip_network,ip_address, IPv4Network
import variables as var
from random import randint
from time import sleep

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
        for red in networksList:
            if red["id"] not in subnetList:
                subnetList[red["id"]] = []
            
            for subnet in res.json()["subnets"]:
                if subnet["network_id"] == red["id"]:
                    subnetList[red["id"]].append(subnet)
        
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

        nombreRedes = [f"{red['name']}|{['red_subred',[red,subnetList[red['id']]]]}" for red in networksList]

        opt = util.printMenu(["Opciones de Configuración de red: ","Agregar Nueva Red","Salir",None] + nombreRedes,
                             comando="python3 modUtilidades.py {}")

        if opt == 1: break

        # Creación de red
        elif opt == 0:
            existe = False
            nombreRed = util.printInput("\nIngrese un nombre para la red provider: ").strip()

            for red in networksList:
                if nombreRed.lower() == red["name"].lower():
                    existe = True
                    break

            if existe:
                util.printError(f"La red {nombreRed} ya existe. Cree una red con un nombre distinto.")
            # Se crea la red
            else:
                vlan = req.get(f'http://{IP_GATEWAY}:6700/getAvailableVlan').json()['response']
                body = {
                    "network": {
                        "name": nombreRed,
                        "admin_state_up": True,
                        "provider:network_type": "vlan",
                        "provider:physical_network": "provider",
                        "provider:segmentation_id": vlan
                    }
                }
                
                nuevaRed = req.post(f"http://{IP_GATEWAY}:9696/v2.0/networks",headers=headers,json=body)
                
                if nuevaRed.status_code == 201:
                    temp = req.get(f'http://{IP_GATEWAY}:6700/setAvailableVlan')
                    util.printSuccess(f"Se esta configurando la extensión vxlan entre las zonas de disponibilidad de la red provider...")
                    repVxlan= req.post(f"http://{IP_GATEWAY}:6700/mapVxlan",json={
                        'vlan' : vlan,
                        'leafs' : ['Leaf1','Leaf2'],
                        'interfaces' : ['0-ens3','0-ens4','1-ens3','1-ens4']
                    })

                    sleep(3.5)
                    util.printSuccess(f"Red {nombreRed} creada exitosamente!")
                else:
                    util.printError(f"Hubo un problema creando la red ({nuevaRed.status_code})")
                    #print(nuevaRed.json())
        
        # Menú de la red elegida
        else:
            red = networksList[opt-3]
            subnets = subnetList[red["id"]]

            opt2 = util.printMenu([f"Opciones de la Red {red['name']}:",
                                   "Agregar Subred","Eliminar Subred",
                                   "Eliminar Red","Salir"])
            
            ## TODO: Agregar más opciones al crear subredes

            # Se crea una subred
            if opt2 == 0:
                existe = False
                nombreSubred = util.printInput("\nIngrese un nombre para la red provider: ").strip()

                for subred in subnets:
                    if nombreSubred.lower() == subred["name"].lower():
                        existe = True
                        break
                if existe:
                    util.printError(f"La subred {nombreSubred} ya existe. Cree una subred con un nombre distinto.")

                while True:
                    try:
                        cidr = util.printInput("Ingrese el CIDR de la subred [a.b.c.d/e]: ").strip()
                        ip_network(cidr)
                        break
                    except ValueError:
                        util.printError("El CIDR ingresado no es válido!\n")
                
                nameservers = []
                print()
                while True:
                    try:
                        dns = util.printInput("Ingrese la dirección IP de un servidor DNS [dejar en blanco para terminar]: ").strip()
                        if dns == "": break
                        ip_address(dns)
                        nameservers.append(dns)
                    except ValueError:
                        util.printError("El DNS ingresado no es válido!\n")
                
                descripcion = util.printInput("Ingrese una descripción de la subred: ").strip()
                
                body = {
                    "subnet": {
                        "network_id": red["id"],
                        "name": nombreSubred,
                        "ip_version": 4,
                        "cidr": cidr,
                        "dns_nameservers": nameservers,
                        "description": descripcion
                    }
                }

                network_temp = IPv4Network(cidr)
                # Find the first available IP address
                for ip in network_temp.hosts():
                    first_available_ip = str(ip)
                    break

                # Print the first available IP address with CIDR notation
                gwip = f"{first_available_ip}/{network_temp.prefixlen}"
                vlan = red['provider:segmentation_id']



                nuevaSubred = req.post(f"http://{IP_GATEWAY}:9696/v2.0/subnets",headers=headers,json=body)
                if nuevaSubred.status_code == 201:
                    req.post(f"http://{IP_GATEWAY}:6700/createGateway", json={'vlan':vlan, 'ip':gwip})
                    util.printSuccess(f"Subred {nombreSubred} creada exitosamente!")
                else:
                    util.printError(f"\nHubo un problema al crear la subred ({nuevaSubred.status_code})")
                    # print(nuevaSubred.json())

            # Se elimina un grupo de subredes
            elif opt2 == 1:
                nombreSubredes = [f"{subred['name']}|{['subred',[subred]]}" for subred in subnets]
                idxs:list[int] = util.printMenu(["Seleccione subredes a eliminar:","Cancelar",None] + nombreSubredes,comando="python3 modUtilidades.py {}",multiselect=True) # type: ignore

                # Elimina las subredes seleccionadas
                if 0 not in idxs:
                    for idx in idxs:
                        response = req.delete(f"http://{IP_GATEWAY}:9696/v2.0/subnets/{subnets[idx-2]['id']}",headers=headers)
                        
                        print(f"Eliminando subred {subnets[idx]['name']}...",sep=" ")
                        if response.status_code == 204:
                            util.printSuccess("Éxito!")
                        else:
                            util.printError(f"Error ({response.status_code})")

            # Se elimina la red
            elif opt2 == 2:
                response = req.delete(f"http://{IP_GATEWAY}:9696/v2.0/networks/{red['id']}",headers=headers)
                        
                print(f"Eliminando la red {red['name']}...",sep=" ")
                if response.status_code == 204:
                    util.printSuccess(f"La red {red['name']} fue eliminada exitosamente")
                if response.status_code == 409:
                    util.printError(f"La red {red['name']} está siendo usada aún (Error {response.status_code})")
                else:
                    util.printError(f"Hubo un error al eliminar la red {red['name']} ({response.status_code})")
                    # print(response.json())

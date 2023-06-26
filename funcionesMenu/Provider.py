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
    
    IP_GATEWAY = var.dirrecionIP
    headers = {"Content-Type": "application/json", "X-Auth-Token": var.dic["token"]}
    existe = False
    nuevaRed = Red(201)
    red = {}

    # Querys
    res = req.get(f"http://{IP_GATEWAY}:9696/v2.0/subnets",headers=headers)
    subnetsList = res.json()["subnets"]
    
    response = req.get(f"http://{IP_GATEWAY}:9696/v2.0/networks?admin_state_up=true",headers=headers)
    networksList = response.json()["networks"]



    # Se elige y valida el nombre de red
    nombreRed = input("Ingrese un nombre para la red provider: ").strip()
    
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
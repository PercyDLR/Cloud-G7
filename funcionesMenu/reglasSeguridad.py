from dataclasses import dataclass
import modUtilidades as util
from time import sleep
from ipaddress import ip_address
import requests as req
import modUtilidades as util
from ipaddress import ip_network
import variables as var
from tabulate import tabulate

@dataclass
class Regla:
    nombre: str
    srcIP: str
    dstIP: str
    protocolo: str
    puerto: int
    action: bool
    status: str

    def __str__(self) -> str:
        return f"{self.nombre}: {self.protocolo} {self.srcIP}->{self.dstIP}:({self.puerto}) {'FORWARD' if self.action else 'DROP'} Estado: {self.status}"

@dataclass
class GrupoSeguridad:
    nombre:str
    reglas:list[Regla]

def main() -> None:
    "Genera el submenú de administración de los grupos de seguridad"

    IP_GATEWAY = var.dirrecionIP
    headers = {"Content-Type": "application/json", "X-Auth-Token": str(var.dic["token"])}

    # Se generan las opciones
    listaGrupos = req.get(f"http://{IP_GATEWAY}:9696/v2.0/security-groups",headers=headers).json()
    nombreGrupos = [grupo["name"] for grupo in listaGrupos["security_groups"]]
    nombreGrupos.insert(0,"Agregar Nuevo")
    nombreGrupos.insert(0,"Opciones para Grupos de Seguridad:")

    # Se elige una opción
    opt = util.printMenu(nombreGrupos)

    # Creación de nuevo grupo
    if opt == 0:
        nombre = input("\nIngrese un nombre para el Grupo de Seguridad: ").strip()
        body = {
            "security_group": {
                "name": nombre,
            }
        }
        response = req.post(f"http://{IP_GATEWAY}:9696/v2.0/security-groups",json=body,headers=headers)

        if response.status_code == 201:
            print(f"\nGrupo de seguridad {nombre} creado exitosamente!")
        else:
            print(f"\nHubo un problema, error {response.status_code}")

    # Edición de Reglas
    else:
        grupo = listaGrupos["security_groups"][opt-1]

        # Se generan las opciones
        listaReglas = req.get(f"http://{IP_GATEWAY}:9696/v2.0/security-groups/{grupo['id']}",headers=headers).json()

        # Se muestran las reglas de seguridad existentes
        table_data = []

        for regla in listaReglas["security_group"]["security_group_rules"]:
            table_data.append([
                regla["id"],
                regla["ethertype"],
                regla["protocol"],
                regla["direction"],
                regla["remote_ip_prefix"],
                regla["description"],
            ])
        table = tabulate(table_data, headers=["ID","Eth Type", "Protocolo", "Dirección", "Rango IPs", "Descripción"], tablefmt="grid")
        print(f"\nReglas de Seguridad del grupo {grupo['name']}\n"+table)

        opt2 = util.printMenu(["Opciones Adicionales:","Agregar Regla","Salir"])

        # Se crea una nueva regla
        if opt2 == 0:
            # Se obtiene el protocolo
            protos = ["Elija un protocolo","udp","tcp"]
            opt3 = util.printMenu(protos)
            print(f"Elija un protocolo: {protos[opt3+1]}")

            # Se obtiene el puerto
            while True:
                try:
                    puerto = int(input("> Ingrese un puerto [1-65536]: ").strip())
                    if puerto > 65536 or puerto < 1:
                        raise ValueError
                    break
                except ValueError:
                    print("\nEl puerto debe ser un número entero entre 1 y 65536")

            # Se obtiene el ip
            while True:
                try:
                    ip = input("> Ingrese una dirección IP [Por defecto 0.0.0.0/0]: ").strip()
                    if ip == "":
                        ip = "0.0.0.0/0"
                    else:
                        ip_network(ip)
                    break
                except ValueError:
                    print("\nLa dirección IP ingresada debe tener el formato a.b.c.d/e")

            descripcion = input("> Ingrese una descripción para la regla: ").strip()

            # Se genera el cuerpo del request
            body = {
                    "security_group_rule": {
                        "direction": "ingress",
                        "port_range_min": puerto,
                        "ethertype": "IPv4",
                        "port_range_max": puerto,
                        "protocol": protos[opt3+1],
                        "security_group_id": grupo['id'],
                        "remote_ip_prefix": ip,
                        "description": descripcion
                        }
                    }
            response = req.post(f"http://{IP_GATEWAY}:9696/v2.0/security-group-rules",json=body,headers=headers)

            if response.status_code == 201:
                print(f"\nRegla agregada exitosamente!")
            else:
                print(f"\nHubo un problema, error {response.status_code}")

            ##TODO: Eliminar y Salir
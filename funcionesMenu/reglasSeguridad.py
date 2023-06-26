from dataclasses import dataclass
import modUtilidades as util
import requests as req
import modUtilidades as util
from ipaddress import ip_network
import variables as var
from typing import List

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
    reglas:List[Regla]

def menuSecGroup() -> None:
    "Genera el submenú de administración de los grupos de seguridad"

    IP_GATEWAY = var.dirrecionIP
    headers = {"Content-Type": "application/json", "X-Auth-Token": str(var.dic["token"])}

    while True:
        # Se generan las opciones
        listaGrupos = req.get(f"http://{IP_GATEWAY}:9696/v2.0/security-groups",headers=headers).json()
        nombreGrupos = [f"{grupo['name']}|{['sg_rule',grupo['security_group_rules']]}" for grupo in listaGrupos["security_groups"]]
        
        #print(eval(nombreGrupos[0].split("|")[1])[1])

        nombreGrupos.insert(0,"Salir")
        nombreGrupos.insert(0,"Agregar Nuevo")
        nombreGrupos.insert(0,"Opciones para Grupos de Seguridad:")

        # Se elige una opción
        opt = util.printMenu(nombreGrupos,comando="python3 modUtilidades.py {}")

        if opt == 1:
            break
        # Creación de nuevo grupo
        elif opt == 0:
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
            grupo = listaGrupos["security_groups"][opt-2]

            # Se generan las opciones
            listaReglas = grupo["security_group_rules"]

            opt2 = util.printMenu(["Opciones Adicionales:",
                                   "Agregar Regla","Eliminar Regla","Eliminar Grupo","Salir"])

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
            
            # Se elimina una regla
            elif opt2 == 1:
                
                reglasEliminar = []

                for regla in listaReglas:
                    if regla["protocol"] is not None:
                        reglasEliminar.append({"proto": regla["protocol"], "puerto": regla["port_range_min"], "ip_prefix": regla["remote_ip_prefix"], "id": regla["id"]})                     

                reglasEliminar.insert(0,"Salir")
                reglasEliminar.insert(0,"Elegir reglas a eliminar:")

                seleccion: tuple[int] = util.printMenu(reglasEliminar,multiselect=True) # type: ignore

                for idx in seleccion:

                    if idx == 0: break 

                    regla = reglasEliminar[idx+1]

                    print("Eliminando reglas...", end=" ")
                    response = req.delete(f"http://{IP_GATEWAY}:9696/v2.0/security-group-rules/{regla['id']}",headers=headers)
                
                    if response.status_code == 204:
                        print("Éxito")
                    else:
                        print(f"Error ({response.status_code})")
            
            # Se elimina el grupo
            elif opt2 == 2:

                # Primero se deben eliminar todas las reglas relacionadas a un puerto
                for regla in listaReglas["security_group"]["security_group_rules"]:
                    if regla["port_range_min"] is not None:
                        print(f"Eliminando regla en el puerto {regla['port_range_min']}...", end=" ")
                        response = req.delete(f"http://{IP_GATEWAY}:9696/v2.0/security-group-rules/{regla['id']}",headers=headers)
                        
                        if response.status_code == 204:
                            print("Éxito")
                        else:
                            print(f"Error ({response.status_code})")

                # Luego se procede a eliminar la regla
                response = req.delete(f"http://{IP_GATEWAY}:9696/v2.0/security-groups/{grupo['id']}",headers=headers)

                if response.status_code == 204:
                    print(f"Se ha eliminado el grupo {grupo['name']} exitosamente.")
                else:
                    print(f"El grupo no pudo ser eliminado ({response.json()})")
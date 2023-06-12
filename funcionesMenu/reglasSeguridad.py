from dataclasses import dataclass
from typing import List, Dict, Any
import modUtilidades as util
from time import sleep
from ipaddress import ip_address
from random import choices
import json

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

def mostrarRequest(method:str, body:Dict[str,Any], action:str, razon:str):
    print(f"Method: {method}\nURL: https://10.20.17.101/orquestador")

    body["user_token"] = "aidba8hd8g38bd2397gf29323d2"      # info usuario
    body["action"] = action                                 # info acción

    print(f"Body:\n{json.dumps(body,indent=4)}")            # Se imprime el body
    sleep(2)
    
    respuesta = choices(["exito","error"],weights=[1,0])[0]
    print(f"Respuesta: {respuesta}")
    if respuesta=="error": 
        print(f"Ha ocurrido un error **{razon}**")
        return False
    return True

def main(listaGrupos:List[GrupoSeguridad]) -> None:
    "Administra los grupos de seguridad"

    while True:

        opt = util.printMenu(["Configuración de grupos de seguridad:",
                          "Listar grupos de seguridad",
                          "Crear grupo de seguridad",
                          "Editar grupo de seguridad",
                          "Eliminar grupo de seguridad",
                          "Salir"])

        # Se lista los grupos de seguridad
        if opt == 1:
            sleep(1)
            print("")
            if len(listaGrupos) == 0:
                print("No hay grupos de seguridad creados")

            for idx, grupo in enumerate(listaGrupos,1):
                print(f"\t{idx}) {grupo.nombre}")

        # Se crea un nuevo grupo de seguridad
        if opt == 2:
            nombre = input("\n> Ingrese un nombre para el securityGroup: ").strip()

            # Lista de nombres de security groups
            listaNombres = [grupo.nombre for grupo in listaGrupos]

            if nombre not in listaNombres:
                if mostrarRequest("POST", {"nombre":nombre},"newSecGroup","Error de conexión"):
                    print("\nCreando Grupo de seguridad...")
                    listaGrupos.append(GrupoSeguridad(nombre,[]))
                    sleep(1)
                    print(f"Grupo {nombre} creado exitosamente!")
            else:
                print(f"\nEl nombre {nombre} ya existe, elija otro\n")

        # Se edita un grupo de seguridad existente
        if opt == 3:
            nombre = input("> Ingrese el nombre del grupo [default: Listar Todos]: ").strip()

            # Se escoge el grupo de seguridad
            grupo:GrupoSeguridad = util.buscarPorNombre(nombre,listaGrupos)

            while True:
                try: 
                    opt2 = util.printMenu([f"Configuración del grupo {grupo.nombre}:",
                                "Listar Reglas", "Crear Reglas", "Eliminar Regla", "Salir"])
                except AttributeError:
                    break

                if opt2 == 1:
                    sleep(1)
                    print("")

                    if mostrarRequest("GET", {"secGroup":grupo.nombre},"listSecRules","Error de conexión"):
                        print("")
                        for regla in grupo.reglas:
                            print(f"\t{regla}") 
                            
                    if len(grupo.reglas) == 0:
                        print("No hay reglas creadas para este grupo")
                
                elif opt2 == 2:
                    nombre = input("\n> Ingrese un nombre para la regla: ").strip()

                    # Lista de nombres de security groups
                    listaNombres = [regla.nombre.lower() for regla in grupo.reglas]

                    if nombre.strip() == "":
                        print("\nDebe ingresar un nombre")

                    elif nombre.lower() not in listaNombres:
                        dictProto = {"ssh": 22, "http":80, "https": 443, "mysql": 3306}

                        # Valida las IPs de origen y destino
                        try:
                            srcIP = input("> Ingrese la IP de origen: ").strip()
                            ip_address(srcIP)
                            dstIP = input("> Ingrese la IP de destino: ").strip()
                            ip_address(dstIP)
                        except ValueError:
                            print("\nIngrese una dirección IP válida")
                            continue

                        # Se elige el protocolo y puerto a usar
                        protocolo = input("> Ingrese el protocolo [ssh,http,mysql,...,tcp]: ").strip()

                        if protocolo.lower() in dictProto:
                            puerto = dictProto[protocolo.lower()]

                        elif protocolo.lower() == "tcp":
                            try:
                                puerto = int(input("> Ingrese el puerto tcp personalizado: ").strip())
                                if puerto <= 0 or puerto > 65535:
                                    raise ValueError
                            except ValueError:
                                print("El puerto debe ser un número entero positivo menor a 65535")
                                continue
                        else:
                            print("El protocolo ingresado no es válido")
                            continue

                        print("\nCreando regla de seguridad...")
                        
                        body = {"secGroup":grupo.nombre,"nombre":nombre,"srcIP":srcIP,"dstIP":dstIP,"protocolo":protocolo.lower(),"puerto":puerto}
                        
                        if mostrarRequest("POST", body,"newSecRule","Error de conexión"):
                            sleep(1)
                            grupo.reglas.append(Regla(nombre,srcIP,dstIP,protocolo.lower(),puerto,True,"Activo"))
                            print(f"Regla {nombre} creada exitosamente!")
                    else:
                        print(f"\nEl nombre {nombre} ya existe, elija otro\n")
                
                elif opt2 == 3:
                    nombre = input("> Ingrese la regla de seguridad [default: Listar Todas]: ").strip()
                    
                    regla:Regla = util.buscarPorNombre(nombre,grupo.reglas)
                    
                    print("\nEliminando regla de seguridad...")
                    
                    if mostrarRequest("POST", {"secGroup":grupo.nombre,"nombre":regla.nombre},"rmSecRule","Error de conexión"):
                        sleep(1)
                        grupo.reglas.remove(regla)
                        print(f"La regla {regla.nombre} ha sido eliminada")

                elif opt2 == 4:
                    break
            
        if opt == 4:
            nombre = input("> Ingrese el nombre del securityGroup [default: Listar Todos]: ").strip()

            # Se escoge el grupo de seguridad
            grupo:GrupoSeguridad = util.buscarPorNombre(nombre,listaGrupos)
            
            # Se elimina
            print("\nEliminando Grupo de seguridad...")
            if mostrarRequest("POST",{"secGroup":grupo.nombre},"rmSecGroup","Error de conexión"):
                sleep(1)
                listaGrupos.remove(grupo)
                print(f"Grupo {grupo.nombre} eliminado exitosamente!")

        if opt == 5:
            print("Saliendo de la configuración de Grupos de Seguridad...")
            break
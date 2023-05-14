from dataclasses import dataclass
from typing import List
import modUtilidades as util
from time import sleep
from ipaddress import ip_address

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
                print("\nCreando Grupo de seguridad...")
                listaGrupos.append(GrupoSeguridad(nombre,[]))
                sleep(1)
                print(f"Grupo {nombre} creado exitosamente!")
            else:
                print(f"\nEl nombre {nombre} ya existe, elija otro\n")

        # Se edita un grupo de seguridad existente
        if opt == 3:
            nombre = input("> Ingrese un nombre para el securityGroup [default: Listar Todos]: ").strip()

            # Se escoge el grupo de seguridad
            grupo:GrupoSeguridad = util.buscarPorNombre(nombre,listaGrupos)

            while True:
                try: 
                    opt2 = util.printMenu([f"Configuración del grupo {grupo.nombre}:",
                                "Listar Reglas", "Editar Reglas", "Eliminar Regla", "Salir"])
                except AttributeError:
                    break

                if opt2 == 1:
                    sleep(1)
                    print("")
                    if len(grupo.reglas) == 0:
                        print("No hay reglas creadas para este grupo")

                    for regla in grupo.reglas:
                        print(f"\t{regla}") 
                
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

                        print("\nCreando Grupo de seguridad...")
                        sleep(1)
                        grupo.reglas.append(Regla(nombre,srcIP,dstIP,protocolo.lower(),puerto,True,"Activo"))
                        print(f"Grupo {nombre} creado exitosamente!")
                    else:
                        print(f"\nEl nombre {nombre} ya existe, elija otro\n")
                
                elif opt2 == 3:
                    nombre = input("> Ingrese la regla de seguridad [default: Listar Todas]: ").strip()
                    
                    regla:Regla = util.buscarPorNombre(nombre,grupo.reglas)
                    
                    print("\nEliminando regla de seguridad...")
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
            sleep(1)
            listaGrupos.remove(grupo)
            print(f"Grupo {nombre} eliminado exitosamente!")

        if opt == 5:
            print("Saliendo de la configuración de Grupos de Seguridad...")
            break
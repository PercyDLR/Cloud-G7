from dataclasses import dataclass
from typing import List
import modUtilidades as util
from time import sleep

@dataclass
class Regla:
    nombre: str
    srcIP: str
    dstIP: str
    protocolo: str
    rangoPuertos: str
    action: bool
    status: str

    def __str__(self) -> str:
        return f"{self.nombre}: {self.protocolo} ({self.rangoPuertos}) {self.srcIP}->{self.dstIP} {self.action} Estado: {self.status}"

@dataclass
class GrupoSeguridad:
    nombre:str
    reglas:List[Regla]

def main(listaGrupos:List[GrupoSeguridad]) -> List[GrupoSeguridad]:
    "Administra los grupos de seguridad"

    opt = util.printMenu(["Configuración de grupos de seguridad:",
                          "Listar grupos de seguridad",
                          "Crear grupo de seguridad",
                          "Editar grupo de seguridad",
                          "Salir"])

    while True:
        # Se lista los grupos de seguridad
        if opt == 1:
            sleep(1)
            for idx, grupo in enumerate(listaGrupos,1):
                print(f"\t{idx}) {grupo.nombre}")

        # Se crea un nuevo grupo de seguridad
        if opt == 2:
            nombre = input("> Ingrese un nombre para el securityGroup: ")

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
            nombre = input("> Ingrese un nombre para el securityGroup: ")

            # Se escoge el grupo de seguridad
            grupo:GrupoSeguridad = util.buscarPorNombre(nombre,listaGrupos)

            while True:
                opt2 = util.printMenu([f"Configuración del grupo {grupo.nombre}:",
                                "Listar Reglas", "Editar Reglas", "Eliminar Regla", "Salir"])
                
                if opt2 == 1:
                    sleep(1)
                    for regla in grupo.reglas:
                        print(regla) 
                
                if opt2 == 2:
                    nombre = input("> Ingrese un nombre para la regla: ")

                    # Lista de nombres de security groups
                    listaNombres = [regla.nombre.lower() for regla in grupo.reglas]

                    if nombre.lower() not in listaNombres:
                        dictProto = {"ssh": 22, "http":80, "https": 443, "mysql": 3306}

                        protocolo = input("> Ingrese el protocolo [ssh,http,mysql,...,tcp]: ")

                        if protocolo in dictProto:
                            puerto = dictProto[protocolo]
                        elif protocolo == "tcp":
                            
                            input("> Ingrese el puerto tcp personalizado: ") 


                        print("\nCreando Grupo de seguridad...")
                        sleep(1)
                        print(f"Grupo {nombre} creado exitosamente!")
                    else:
                        print(f"\nEl nombre {nombre} ya existe, elija otro\n")
            

        if opt == 4:
            print("Saliendo de la configuración de Grupos de Seguridad...")
            break

    return listaGrupos
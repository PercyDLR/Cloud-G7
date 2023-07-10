from dataclasses import dataclass

import modUtilidades as util
from login import IngresarCredenciales
import requests as req
import variables as var
from time import sleep

@dataclass
class Slice:
    nombre: str
    topologia: str
    secGroup: str

def seleccionarProyecto(slice:dict):
    data = {
        "auth": {
            "identity": {
                "methods": [
                    "token"
                ],
                "token": {
                    "id": var.dic['token']
                }
            },
            "scope": {
                "project": {
                    "domain": {
                        "id": "default"
                    },
                    "name": slice['name']
                }
            }
        }
    }

    response = req.post(f"http://{var.dirrecionIP}:5000/v3/auth/tokens",params={"domain_id":"default"},json=data)

    if response.status_code == 201:
        var.dic["token"] = response.headers["X-Subject-Token"]
        var.dic['expiration'] = response.json()["token"]["expires_at"]
        var.dic['project'] = slice['name']
        var.dic['projectID'] = slice['id']
        var.dic['zonasElegidas'] = ["Worker1","Worker2","Worker3"]

        with open("credencial.txt","w") as f:
            f.write(f"{var.dic['token']}\n{var.dic['expiration']}\n{var.dic['project']}\n{var.dic['projectID']}\n{['Worker1','Worker2','Worker3']}")
        
    else:
        util.printError(f"No se ha podido autenticar al usuario {response.status_code}")
        # print(response.json())
        exit()

def crearSlice(listaSlices:list,listaGrupos:list):
    """Crea un slice, preguntando por la topología base, y los equipos iniciales"""
    
    # Petición de datos
    nameSlice = util.printInput("\n> Ingrese nombre del Slice a crear: ").strip()
    
    # Se elige una topología
    listaTopologias = ["Elija una topologia base para el slice:",
                       "Lineal", "Malla", "Arbol", "Anillo", "Bus"]
    opt = util.printMenu(listaTopologias)
    topologia = listaTopologias[opt]

    # Se crea un nuevo grupo de seguridad
    if len(listaGrupos) == 0:

        print("\nNo existen grupos de seguridad. Creando uno nuevo...")

        while True:
            nombre = input("\n> Ingrese un nombre para el grupo de seguridad: ").strip()

            if nombre != "":
                print("\nCreando Grupo de seguridad...")
                # grupo = GrupoSeguridad(nombre,[])

                # if mostrarRequest("POST",{"nombre":nombre},"newSecGroup","Error de conexión"):
                    # listaGrupos.append(grupo)
                    # print(f"Grupo {nombre} creado exitosamente!")
                break
            
            else:
                print("\nDebe ingresar un nombre para el grupo")
    
    # Se elije un grupo ya existente
    else:
        nombre = input("> Ingrese el nombre del grupo [default: Listar Todos]: ").strip()
        while (grupo:= util.buscarPorNombre(nombre,listaGrupos)) == None:
            print("Opción no valida...")
        
    # Se crea el Slice
    print(f"\nCreando slice {nameSlice}...")
    # if mostrarRequest("POST",{"nombre":nameSlice,"topologia":topologia,"secGroup":grupo.nombre},
    #                  "newSlice", "El servidor no pudo procesar su solicitud. Vuelva a intentarlo más tarde"):
    
    # listaSlices.append(currentSlice(nameSlice,topologia,grupo.nombre,"",[],[]))
    print(f"Slice {nameSlice} creado")

def eliminarSlice(slice:dict):

    headers = {"Content-Type": "application/json", "X-Auth-Token": var.dic["token"]}
  
    # Se pone un mensaje de confirmación
    opt = util.printMenu([f"Está seguro de querer eliminar el slice {slice['name']}?",'Sí','No'])
    if opt == 1: return

    # Se crea el request
    response = req.delete(f"http://{var.dirrecionIP}:5000/v3/projects/{slice['id']}",headers=headers)

    # Se verifica el resultado del request
    if response.status_code == 204:
        util.printSuccess(f"\nSlice {slice['name']} eliminado exitosamente. Cambiando de grupo...\n")
        
        with open("credencial.txt","w") as f:
            f.write("")

        IngresarCredenciales()
    else:
        util.printError(f"\nHubo un problema, error {response.status_code}")

    # Crear grupos para probar
    # openstack project create prueba
    # openstack role add --user admin --project <uuid> admin

def menuSlice(login:bool):
    "Muestra el menú de gestión de slices"
    headers = {"Content-Type": "application/json", "X-Auth-Token": var.dic["token"]}
    
    listaProyectos = req.get(f"http://{var.dirrecionIP}:5000/v3/auth/projects",params={"domain_id":f"{var.username}"},headers=headers).json()['projects']
    nombreProyectos = [project['name'] for project in listaProyectos]

    opt = util.printMenu(["Seleccione un slice:","Crear Nuevo","Cancelar",None] + nombreProyectos)

    # Se crea un slice
    if opt == 0:
        while (nombre:= util.printInput("\n> Ingrese nombre del Slice: ")) == "" or nombre in nombreProyectos:
                print("\nDebe ingresar un nombre para el slice que no sea repetido")
        
        topo = util.printMenu(["Elija una topologia base para el slice:","Lineal", "Malla", "Arbol", "Anillo", "Bus"])

        proyecto_crear=  {'project': {'name': nombre, 'enabled': True , 'domain_id' : "default"}}

        response = req.post('http://' + var.dirrecionIP + ':5000/v3/projects', headers=headers, json=proyecto_crear).json()


        responseRole = req.put('http://' + var.dirrecionIP + f':5000/v3/projects/{response["project"]["id"]}/users/{var.userid}/roles/1b7359c3207348cba2a71315f1a2f575', headers=headers)


        #print(responseRole,f"\n{response['project']['id']}")


        project_id = response['project']['id']

        util.printSuccess(f"\nSlice {nombre} creado exitosamente. Cambiando de grupo...\n")



        seleccionarProyecto(response["project"])

    # Cancelar
    elif opt == 1:
        util.printError("\nCancelando Operacion...")
        
        if login: exit()
        else: return
 
    # En la vista de logueo, solo se selecciona un Slice
    elif login:
        seleccionarProyecto(listaProyectos[opt-3])
    
    # En la vista de gestión de slices, se tienen varias opciones por slice
    elif not login:
        currentSlice = listaProyectos[opt-3]

        if currentSlice['name'] != 'admin':
            opt2 = util.printMenu(['Opciones del Slice:','Configurar Slice','Eliminar Slice','Cancelar'])
        else:
            opt2 = util.printMenu(['Opciones del Slice:','Configurar Slice','Cancelar'])

        # Cambiar de Slice
        if opt2 == 0:
            seleccionarProyecto(currentSlice)

        # Eliminar Slice
        elif currentSlice['name'] != 'admin' and opt2 == 1:
            eliminarSlice(currentSlice)

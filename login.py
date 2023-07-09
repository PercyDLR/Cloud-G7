import getpass
from colorama import Fore,Style
import requests
import variables
import datetime
from modUtilidades import printError,printSuccess,printInput,printMenu

auth_url=f"http://{variables.dirrecionIP}:5000/v3"

def verificarCredencialesExistentes():
    try:
        with open("credencial.txt","r") as f:
            token = f.readline().rstrip()
            expiracion = f.readline().rstrip()
            project = f.readline().rstrip()
            projectID = f.readline().rstrip()

        # print(f"{datetime.datetime.utcnow()=}\n {datetime.datetime.strptime(expiracion,'%Y-%m-%dT%H:%M:%S.%fZ')=}")
        # print(f"{datetime.datetime.utcnow() < datetime.datetime.strptime(expiracion,'%Y-%m-%dT%H:%M:%S.%fZ')}")

        if token != "" and datetime.datetime.utcnow() < datetime.datetime.strptime(expiracion,"%Y-%m-%dT%H:%M:%S.%fZ"):
            variables.dic["token"] = token
            variables.dic["expiration"] = expiracion
            variables.dic["project"] = project
            variables.dic["projectID"] = projectID
            return True
        
    except FileNotFoundError as e:
        pass
    return False

def seleccionarProyecto(token):
    headers = {"Content-Type": "application/json", "X-Auth-Token": token}

    listaProyectos = requests.get(f"{auth_url}/auth/projects",params={"domain_id":"default"},headers=headers).json()['projects']
    nombreProyectos = [project['name'] for project in listaProyectos]

    opt = printMenu(["Seleccione el slice a trabajar:","Cancelar",None] + nombreProyectos)

    if opt == 0: 
        printError("\nCancelando Operacion...")
        exit()
    
    data = {
        "auth": {
            "identity": {
                "methods": [
                    "token"
                ],
                "token": {
                    "id": token
                }
            },
            "scope": {
                "project": {
                    "domain": {
                        "id": "default"
                    },
                    "name": listaProyectos[opt-2]['name']
                 }
            }
        }
    }

    response = requests.post(f"{auth_url}/auth/tokens",params={"domain_id":"default"},json=data)

    if response.status_code == 201:
        variables.dic["token"] = response.headers["X-Subject-Token"]
        variables.dic['expiration'] = response.json()["token"]["expires_at"]
        variables.dic['project'] = listaProyectos[opt-2]['name']
        variables.dic['projectID'] = listaProyectos[opt-2]['id']
        printSuccess("\nAutenticación exitosa")

        with open("credencial.txt","w") as f:
            f.write(f"{variables.dic['token']}\n{variables.dic['expiration']}\n{variables.dic['project']}\n{variables.dic['projectID']}")
        
    else:
        printError(f"No se ha podido autenticar al usuario {response.status_code}")
        print(response.json())
        exit()

def IngresarCredenciales(skip=False):
    if not skip and verificarCredencialesExistentes():
        return
    
    while((user:=printInput("Ingrese su usuario: "))==""):
        printError("No puede ser vacio")
    while((password:=getpass.getpass(prompt=f"{Fore.CYAN}{Style.BRIGHT}Ingrese su contraseña: {Style.RESET_ALL}"))==""):
        printError("No puede ser vacio")

    data = {
        "auth": {
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "domain": {
                            "name": "Default"
                        },
                        "name": user,
                        "password": password
                    }
                }
            },
            "scope": {
                "project": {
                    "domain": {
                        "name": "default"
                    },
                    "name": "admin"
                }
            }
        }
    }

    global auth_url
    url = f"{auth_url}/auth/tokens?nocatalog"
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=data, headers=headers)
    
    status_code = response.status_code

    if status_code == 201:
        # print(f"Su token es: {token}")
        # print(f"Su token expira en: {expiration}")

        seleccionarProyecto(response.headers["X-Subject-Token"])
        
    else:
        printError(f"No se ha podido autenticar al usuario ({response.status_code})")
        exit()

if __name__ == '__main__':
    IngresarCredenciales()
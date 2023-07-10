import getpass
from colorama import Fore,Style
import requests
import variables
import datetime
from modUtilidades import printError,printSuccess,printInput,printMenu
import funcionesMenu.Slice as s

auth_url=f"http://{variables.dirrecionIP}:5000/v3"

def verificarCredencialesExistentes():
    try:
        with open("credencial.txt","r") as f:
            token = f.readline().rstrip()
            expiracion = f.readline().rstrip()
            project = f.readline().rstrip()
            projectID = f.readline().rstrip()
            zonas = eval(f.readline().rstrip())

        # print(f"{datetime.datetime.utcnow()=}\n {datetime.datetime.strptime(expiracion,'%Y-%m-%dT%H:%M:%S.%fZ')=}")
        # print(f"{datetime.datetime.utcnow() < datetime.datetime.strptime(expiracion,'%Y-%m-%dT%H:%M:%S.%fZ')}")

        if token != "" and datetime.datetime.utcnow() < datetime.datetime.strptime(expiracion,"%Y-%m-%dT%H:%M:%S.%fZ"):
            variables.dic["token"] = token
            variables.dic["expiration"] = expiracion
            variables.dic["project"] = project
            variables.dic["projectID"] = projectID
            variables.dic['zonasElegidas'] = zonas
            return True
        
    except FileNotFoundError as e:
        pass
    return False

def IngresarCredenciales(skip=False):
    if not skip and verificarCredencialesExistentes():
        return
    
    while((user:=printInput("Ingrese su usuario: "))==""):
        printError("No puede ser vacio")
    
    variables.username = user


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
        printSuccess("\nAutenticación exitosa")

        # print(f"Su token es: {token}")
        # print(f"Su token expira en: {expiration}")

        variables.dic['token'] = response.headers["X-Subject-Token"]
        variables.userid=response.json()["token"]["user"]["id"]
        s.menuSlice(login=True)
        
    else:
        printError(f"No se ha podido autenticar al usuario ({response.status_code})")
        exit()

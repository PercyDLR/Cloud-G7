import getpass
from colorama import Fore,Style
import requests
from variables import dirrecionIP
import variables
import datetime
from modUtilidades import printError,printSuccess,printInput

auth_url=f"http://{dirrecionIP}:5000/v3"

def verificarCredencialesExistentes():
    try:
        with open("credencial.txt","r") as f:
            token = f.readline().rstrip()
            expiracion = f.readline().rstrip()

        # print(f"{datetime.datetime.utcnow()=}\n {datetime.datetime.strptime(expiracion,'%Y-%m-%dT%H:%M:%S.%fZ')=}")
        # print(f"{datetime.datetime.utcnow() < datetime.datetime.strptime(expiracion,'%Y-%m-%dT%H:%M:%S.%fZ')}")

        if token != "" and datetime.datetime.utcnow() < datetime.datetime.strptime(expiracion,"%Y-%m-%dT%H:%M:%S.%fZ"):
            variables.dic["token"] = token
            variables.dic["expiration"] = expiracion
            return True
        
    except FileNotFoundError as e:
        pass
    return False

def IngresarCredenciales():
    if verificarCredencialesExistentes():
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

    try:
        response = requests.post(url, json=data, headers=headers)
    except Exception:
        printError("No se ha podido autenticar al usuario")
        exit()
    
    status_code = response.status_code
    response_content = response.json()

    if status_code == 201:
        token = response.headers["X-Subject-Token"]
        variables.dic["token"] = token
        expiration = response_content["token"]["expires_at"]
        printSuccess("\nAutenticación exitosa")
        # print(f"Su token es: {token}")
        # print(f"Su token expira en: {expiration}")

        with open("credencial.txt","w") as f:
            f.write(f"{token}\n{expiration}")
        
    else:
        printError("No se ha podido autenticar al usuario")
        exit()

if __name__ == '__main__':
    IngresarCredenciales()
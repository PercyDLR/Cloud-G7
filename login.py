import getpass
import requests
import os
from variables import dirrecionIP
import variables
import datetime
from modUtilidades import printError

auth_url=f"http://{dirrecionIP}:5000/v3"
compute_url=f"http://{dirrecionIP}:8774/v2.1"

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
    
    while((user:=input("Ingrese su usuario: "))==""):
        printError("No puede ser vacio")
    while((password:=getpass.getpass(prompt="Ingrese su contraseña: "))==""):
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
        print("Autenticación exitosa")
        # print(f"Su token es: {token}")
        # print(f"Su token expira en: {expiration}")

        with open("credencial.txt","w") as f:
            f.write(f"{token}\n{expiration}")
        
    else:
        printError("No se ha podido autenticar al usuario")
        exit()

def createKeypair(token):
    while((keyname:=input("Ingrese el nombre de la llave: "))==""):
        printError("No puede ser vacio")
    
    key: str
    path= ""
    while(True):
        path=input("Ingrese la ruta de la llave: ")
        if not os.path.isfile(path):
            printError("Error: File does not exist.")
        elif os.path.getsize(path) == 0:
            printError("Error: File is empty.")
        else:
            with open(path, "r") as file:
                key = file.read()
            break

    data = {
        "keypair": {
            "name": keyname,
            "public_key": key
        }
    }

    headers = {"Content-Type": "application/json", "X-Auth-Token": token}

    response = requests.post(compute_url + "/os-keypairs", json=data, headers=headers)

    if response.status_code == 200:
        printError("Keypair created successfully: " + response.text)
    else:
        printError("Keypair creation failed: " + response.text)


if __name__ == '__main__':
    IngresarCredenciales()
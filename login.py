import getpass
import requests
import os
from variables import dirrecionIP
import variables

auth_url=f"http://{dirrecionIP}:5000/v3"
compute_url=f"http://{dirrecionIP}:8774/v2.1"

def IngresarCredenciales():
    while((user:=input("Ingrese su usuario: "))==""):
        print("No puede ser vacio")
    while((password:=getpass.getpass(prompt="Ingrese su contraseña: "))==""):
        print("No puede ser vacio")

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
            }
        }
    }

    global auth_url
    url = f"{auth_url}/auth/tokens?nocatalog"
    headers = {"Content-Type": "application/json"}


    try:
        response = requests.post(url, json=data, headers=headers)
    except Exception:
        print("No se ha podido autenticar al usuario")
        return 1
    
    status_code = response.status_code
    response_content = response.json()

    global token,expiration
    if status_code == 201:
        token = response.headers["X-Subject-Token"]
        variables.dic["token"] = token
        expiration = response_content["token"]["expires_at"]
        print("Autenticación exitosa")
        print(f"Su token es: {token}")
        print(f"Su token expira en: {expiration}")

        return token
        # Process the token and expiration as needed
    else:
        print("No se ha podido autenticar al usuario")
        return 1

def createKeypair(token):
    while((keyname:=input("Ingrese el nombre de la llave: "))==""):
        print("No puede ser vacio")
    
    key: str
    path= ""
    while(True):
        path=input("Ingrese la ruta de la llave: ")
        if not os.path.isfile(path):
            print("Error: File does not exist.")
        elif os.path.getsize(path) == 0:
            print("Error: File is empty.")
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
        print("Keypair created successfully:", response.text)
    else:
        print("Keypair creation failed:", response.text)


if __name__ == '__main__':  
    IngresarCredenciales();
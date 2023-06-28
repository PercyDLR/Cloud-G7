import getpass
from colorama import Fore,Style
import requests
import os
from variables import dirrecionIP
import variables
import datetime
from modUtilidades import printError,printSuccess,printInput

def createKeypair(token):

    compute_url=f"http://{dirrecionIP}:8774/v2.1"

    while((keyname:=printInput("Ingrese el nombre de la llave: "))==""):
        printError("No puede ser vacio")
    
    while(True):
        path=printInput("Ingrese la ruta de la llave: ")

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
        printSuccess("Par de llaves creado exitosamente")
    else:
        printError(f"Hubo un error creando el par de llaves ({response.status_code})")
        # print(response.json())
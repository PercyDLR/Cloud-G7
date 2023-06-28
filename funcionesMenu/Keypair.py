import requests
import variables as var
import modUtilidades as util

def menuKeypair():

    compute_url=f"http://{var.dirrecionIP}:8774/v2.1"
    headers = {"Content-Type": "application/json", "X-Auth-Token": var.dic['token']}

    while((keyname:=util.printInput("Ingrese el nombre de la llave: "))==""):
        util.printError("No puede ser vacio")
    
    path = util.selectorArchivos([("LLave pública",".pub"),("Todos los archivos","*")])

    with open(path, "r") as file:
        key = file.read()
       
        data = {
            "keypair": {
                "name": keyname,
                "public_key": key
            }
        }

        response = requests.post(compute_url + "/os-keypairs", json=data, headers=headers)

        if response.status_code == 200:
            util.printSuccess("Par de llaves creado exitosamente")
        else:
            util.printError(f"Hubo un error creando el par de llaves ({response.status_code})")
            # print(response.json())
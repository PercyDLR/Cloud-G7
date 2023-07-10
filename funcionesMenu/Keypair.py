import requests
import variables as var
import modUtilidades as util

def menuKeypair() -> dict:

    compute_url=f"http://{var.dirrecionIP}:8774/v2.1"
    headers = {"Content-Type": "application/json", "X-Auth-Token": var.dic['token']}

    while((keyname:=util.printInput("\nIngrese el nombre de la llave: "))==""):
        util.printError("No puede ser vacio")
    
    path = util.selectorArchivos([("LLave pública",".pub"),("Todos los archivos","*")])
    util.printInfo("Llave a agregar: " + path)

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
            util.printSuccess("\nPar de llaves agregado exitosamente")
            return response.json()['keypair']
        else:
            util.printError(f"\nHubo un error agregando el par de llaves ({response.status_code})")
            # print(response.json())
            return {}
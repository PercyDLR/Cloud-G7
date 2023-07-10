import requests as req
import variables as var
import modUtilidades as util
import funcionesMenu.Keypair as key
from time import sleep

def selectFlavor(IP_GATEWAY,headers):
        
    response = req.get(f"http://{IP_GATEWAY}:8774/v2.1/flavors/detail",headers=headers)
    flavorsList = response.json()["flavors"]
    
    # Crea el menú de selección de flavors
    menu_items = [f"{flavor['name']}|{['flavor',flavor]}" for flavor in flavorsList]
    # print(menu_items[0].split("|")[1])
    
    opt = util.printMenu(["Seleccione un flavor:"] + menu_items, 
                         comando="python3 modUtilidades.py {}")
  
    selected_flavor = flavorsList[opt]
    
    return selected_flavor

def selectAvailabilityZone(IP_GATEWAY:str, flavor:dict):
    listaZonas = req.get(f"http://{IP_GATEWAY}:6700/getStatistics").json()['hosts']

    #print(listaZonas)
    best_worker = {'host': '','data':{'cpu': 0, 'disk': 0, 'memory': 0, 'vms': 10000}}

    # Se analizan los recursos de cada availability zone
    for zona in listaZonas:
        if zona['host'] in var.dic['zonasElegidas']:
            try:       # Si está en las zonas elegidas
                resources = zona['data']                
                # Se analiza si una máquina de ese flavor puede entrar en esa zona
                if  resources['cpu'] >= flavor['vcpus'] and resources['disk'] >= flavor['disk'] and \
                    resources['memory'] >= flavor['ram']:
                    
                    puntaje = 0
                    best_resources = best_worker['data']

                    # Se analiza la zona con más recursos y menos máquinas
                    if resources['cpu'] > best_resources['cpu']:
                        puntaje += 1
                    
                    if resources['disk'] > best_resources['disk']:
                        puntaje += 1

                    if resources['memory'] > best_resources['memory']:
                        puntaje += 1
                    
                    if resources['vms'] < best_resources['vms']:
                        puntaje += 1
                    
                    if puntaje >= 2:
                        best_worker = zona

                    #print((best_worker['host'],puntaje))
            except Exception as e:
                pass

    if best_worker['host'] != '':
        util.printSuccess(f"\nEl mejor worker es {best_worker['host']}")
        return best_worker, flavor
    else:
        util.printError(f"Ninguna de las zonas elegidas puede albergar una VM de estas características")
        return None,None

def selectImage(IP_GATEWAY,headers):
    
    response = req.get(f"http://{IP_GATEWAY}:9292/v2/images?sort=name:asc&status=active",headers=headers)
    imagesList = response.json()["images"]
    
    # Crea el menú de selección de flavors
    menu_items = [image["name"] for image in imagesList]

    # Muestra el menú y obtiene la selección del usuario
    selected_index = util.printMenu(["Seleccione una imagen:","Cancelar",None] + menu_items)
        
    if selected_index == 0: return

    selected_image = imagesList[selected_index-2]
    return selected_image

def selectNetwork(IP_GATEWAY,headers):
    res = req.get(f"http://{IP_GATEWAY}:9696/v2.0/subnets",headers=headers)
    subnetsList = res.json()["subnets"]
    
    response = req.get(f"http://{IP_GATEWAY}:9696/v2.0/networks?admin_state_up=true",headers=headers)
    networksList = response.json()["networks"]
    
    subnetsListActive = []
    
    for subnet in subnetsList:
        idNetwork = subnet["network_id"] 
        for network in networksList:
            if(network["id"]==idNetwork):
                subnet["network_name"]=network["name"]
                subnetsListActive.append(subnet)
    
    # Crea el menú de selección de flavors
    menu_items = [f"{subnet['name']}|{['subred_list',subnet]}" for subnet in subnetsListActive]
    #print(eval(menu_items[0].split('|')[1])[1])

    selected_index = util.printMenu(["Seleccione una subnet:","Cancelar",None] + menu_items,
                         comando="python3 modUtilidades.py {}")

    if selected_index == 0: return

    selected_subnet = subnetsListActive[selected_index-2] 
    return selected_subnet

def selectKeypair(IP_GATEWAY,headers):
    response = req.get(f"http://{IP_GATEWAY}:8774/v2.1/os-keypairs",headers=headers)
    keyList = response.json()["keypairs"]

    # Crea el menú de selección de flavors
    menu_items = [key["keypair"]["name"] for key in keyList]

    # Muestra el menú y obtiene la selección del usuario
    selected_index = util.printMenu(["Seleccione un Par de llaves:","Agregar","Cancelar",None] + menu_items)
    
    if selected_index == 1: return

    elif selected_index == 0:
        return key.menuKeypair()

    selected_key = keyList[selected_index-3]
    return selected_key["keypair"]
    
def selectGroup(IP_GATEWAY,headers):
    sgList = req.get(f"http://{IP_GATEWAY}:9696/v2.0/security-groups",headers=headers).json()["security_groups"]
    menu_items = [f"{grupo['name']}|{['sg_rule',grupo['security_group_rules']]}" for grupo in sgList]
    
    # Muestra el menú y obtiene la selección del usuario
    selected_index = util.printMenu(["Seleccione un Grupo de Seguridad:","Cancelar",None] + menu_items,
                         comando="python3 modUtilidades.py {}")

    if selected_index == 0: return

    selected_sg = sgList[selected_index-2]
    return selected_sg
    
def crearVM(IP_GATEWAY:str, headers:dict[str,str]):
    
    while((nameVM:=util.printInput("Ingrese nombre de la VM: ").strip())==""):
        util.printError("No puede estar vacio.")
    
    flavorVM = selectFlavor(IP_GATEWAY,headers)
    if flavorVM is None: return 
    
    host, resources = selectAvailabilityZone(IP_GATEWAY,flavorVM)
    if host is None: return

    imageVM = selectImage(IP_GATEWAY,headers)
    if imageVM is None: return 
    
    networkVM = selectNetwork(IP_GATEWAY,headers)
    if networkVM is None: return

    keyVM = selectKeypair(IP_GATEWAY,headers)
    if keyVM is None: return

    sgVM = selectGroup(IP_GATEWAY,headers)
    if sgVM is None: return
    
    body = {
            "server" : {
                "name": nameVM,
                "imageRef" : imageVM["id"],
                "flavorRef" : flavorVM["id"],
                "key_name": keyVM["name"],
                "networks" : [{
                    "uuid" : networkVM["network_id"],
                }],
                "security_groups": [{
                    "name": sgVM["name"]
                }],
                "host":host['host']
            }
        }
    
    headers2 = {"X-OpenStack-Nova-API-Version": "2.87", "Content-Type": "application/json", "X-Auth-Token": var.dic["token"]}
    response = req.post(f"http://{IP_GATEWAY}:8774/v2.1/servers",json=body,headers=headers2)


    if response.status_code == 202:
        responseUpdateWorker = req.post(f"http://{IP_GATEWAY}:6700/updateWorkerResources", json={
            "worker": host['host'][-1],
            "resources":{
                "action": "add",
                "memory" : resources['ram'],
                'disk' : resources['disk'],
                'cpu': resources['vcpus'],
                'name': nameVM
            }
        })
        print(responseUpdateWorker.json())


        util.printSuccess(f"\nVM creada exitosamente! Esta podría tardarse unos segundos en iniciar.")
        sleep(5)
    else:
        util.printError(f"\nHubo un problema, error {response.status_code}")
        print(response.json())

def menuVM():

    IP_GATEWAY = var.dirrecionIP
    headers = {"Content-Type": "application/json", "X-Auth-Token": var.dic["token"]}

    while True:
        headers2 = {"X-OpenStack-Nova-API-Version": "2.73", "Content-Type": "application/json", "X-Auth-Token": var.dic["token"]}
        listaVMs = req.get(f"http://{IP_GATEWAY}:8774/v2.1/servers/detail",headers=headers2).json()['servers']

        listaImagenes = req.get(f"http://{IP_GATEWAY}:9292/v2/images",headers=headers).json()["images"]

        # Le agrega un nombre a cada imagen
        imgCache = {}
        for vm in listaVMs:
            imgId = vm["image"]["id"]

            if imgId in imgCache:
                vm["image"]["name"] = imgCache[imgId]
                continue

            for img in listaImagenes:
                if img['id'] == imgId:
                    vm["image"]["name"] = img['name']
                    imgCache[imgId] = img['name']
                    break

        nombreVMs = [f"{vm['name']}|{['vm',vm]}" for vm in listaVMs]

        opt = util.printMenu(["Opciones de Gestión de VMs:","Crear Nueva","Salir",None] + nombreVMs,
                            comando = "python3 modUtilidades.py {}")

        if opt == 0:
            crearVM(IP_GATEWAY,headers)
        elif opt == 1:
            break
        else:
            vm = listaVMs[opt-3]

            opt2 = util.printMenu([f"Opciones de la VM {vm['name']}:",
                                   "Encender VM" if vm['status'] == 'SHUTOFF' else "Detener VM",
                                   "Acceso Consola VNC","Reiniciar VM","Eliminar VM","Salir"])
                        
            # Encender
            if opt2 == 0:
                action = "os-start" if vm['status'] == 'SHUTOFF' else "os-stop"

                response = req.post(f"http://{IP_GATEWAY}:8774/v2.1/servers/{vm['id']}/action",json={action: None},headers=headers)

                if response.status_code == 202:
                    util.printSuccess(f"\nLa VM {vm['name']} se está {'encendiendo' if action == 'os-start' else 'deteniendo'}. Esto podría tardar algunos segundos en completarse")
                    sleep(3)
                else:
                    util.printError(f"\nHubo un problema, error {response.status_code}")
                    # print(response.json())
            
            elif opt2 == 1:
                response = req.post(f"http://{IP_GATEWAY}:8774/v2.1/servers/{vm['id']}/action",json={"os-getVNCConsole":{"type": "novnc"}},headers=headers)
                
                if response.status_code == 200:
                    
                    url:str = response.json()['console']['url']
                    url = url.replace("controller",IP_GATEWAY)

                    util.printSuccess(f"\nPor favor conectarse a la VM usando el siguiente enlace:")
                    print(url)
                else:
                    util.printError(f"\nHubo un problema, error {response.status_code}")
                    # print(response.json())


            # Reiniciar VM
            elif opt2 == 2:
                tipo = "SOFT" if vm['status'] == 'ACTIVE' else "HARD"
                response = req.post(f"http://{IP_GATEWAY}:8774/v2.1/servers/{vm['id']}/action",json={"reboot": {"type": tipo}},headers=headers)

                if response.status_code == 202:
                    util.printSuccess(f"\nLa VM {vm['name']} se está reiniciando ({tipo} reboot). Esto podría tardar algunos segundos en completarse")
                    sleep(5)
                else:
                    util.printError(f"\nHubo un problema, error {response.status_code}")
                    # print(response.json())

            # Eliminar VM
            elif opt2 == 3:
                response = req.delete(f"http://{IP_GATEWAY}:8774/v2.1/servers/{vm['id']}",headers=headers)

                if response.status_code == 204:
                    util.printSuccess(f"\nLa VM {vm['name']} esta siendo eliminada. Esto podría tardar algunos minutos en completarse")
                    sleep(4)
                    #print(vm)
                    #print(vm.get("OS-EXT-SRV-ATTR:hypervisor_hostname"))
                    responseUpdateWorker = req.post(f"http://{IP_GATEWAY}:6700/updateWorkerResources", json={
                                "worker": vm["OS-EXT-SRV-ATTR:hypervisor_hostname"][-1],
                                'resources':{
                                "action": "remove",
                            'name': vm['name']
                            }
                        })

                    
                        
                    #print(responseUpdateWorker.json())

                else:
                    util.printError(f"\nHubo un problema, error {response.status_code}")
                    # print(response.json()) 

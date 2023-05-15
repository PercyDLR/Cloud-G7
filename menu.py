import modUtilidades as util
import funcionesMenu.editSlice as editSlice
import funcionesMenu.Slice as s
import funcionesMenu.Imagen as img
import funcionesMenu.reglasSeguridad as r
import clases
import subprocess
import json
import hashlib
import getpass
from typing import Dict, List, Any
from clases.VM import VM
from tabulate import tabulate
from funcionesMenu.Imagen import Imagen
from funcionesMenu.reglasSeguridad import GrupoSeguridad,Regla
import time
import random
from dataclasses import dataclass, asdict

def mostrarRequest(method,body,action,body_resp):
    print(f"Method: {method}")
    print("URL: https://10.20.17.101/orquestador")
    body["action"] = action
    print(f"Body:\n{json.dumps(body,indent=4)}")
    print("Send and waiting for response")
    time.sleep(2)
    respuesta = random.choices(["exito","error"],weights=[0.75,0.25])[0]
    print(f"Response: {respuesta}")
    razon=""
    if respuesta=="error": 
        razon="Se termino la comunicacion con el servidor de forma inesperada"
        print(f"Ha ocurrido un error **{razon}**")
        return True
    print(f"Body:\n{json.dumps(body_resp,indent=4)}")
    return False

def mostrarRequestafter(method,body,action,body_resp):
    print(f"Method: {method}")
    print("URL: https://10.20.17.101/orquestador")
    body["user_token"] = "aidba8hd8g38bd2397gf29323d2"
    body["action"] = action
    print(f"Body:\n{json.dumps(body,indent=4)}")
    print("Send and waiting for response")
    time.sleep(2)
    respuesta = random.choices(["exito","error"],weights=[0.9,0.10])[0]
    print(f"Response: {respuesta}")
    razon=""
    if respuesta=="error": 
        razon="Se termino la comunicacion con el servidor de forma inesperada"
        print(f"Ha ocurrido un error **{razon}**")
        return True
    print(f"Body:\n{json.dumps(body_resp,indent=4)}")
    return False

def login() -> None:
    "Implementa un logueo básico"
    for intentos in range(3,0,-1):
        username = input("\nIngrese su usuario: ").strip()
        password = hashlib.sha256(getpass.getpass("Ingrese su contraseña: ").encode()).hexdigest()
        #password is 12345
        if(username=="grupo7" and 
            password=="5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5"):
            if(mostrarRequest("POST",{"username":username,"password":password},"login",{"user_token": "aidba8hd8g38bd2397gf29323d2","estado":"exito"})):
                print("Por favor intentelo mas tarde")
            else:
                return
        else:
            if(mostrarRequest("POST",{"username":username,"password":password},"login",{"estado":"no_encontrado"})):
                print("Por favor intentelo mas tarde")
                return
            print(f"\n** El usuario indicado no existe, {intentos-1} intentos restantes")
     
    print("\nEl logueo falló 3 veces. Por favor revise sus credenciales y vuelva a intentarlo más tarde")
    exit()

datos_sesion = {"slices":[],"gruposSeguridad":[],"imagenes":[]}



def updateSlice(sliceSave : editSlice.currentSlice):
    datos_sesion["slices"]= [x if x.nombre != sliceSave.nombre else sliceSave for x in datos_sesion["slices"]]

def obtenerDatos() -> Dict[str, List[Any]]:
    global datos_sesion
    datos_sesion={"slices":[],"gruposSeguridad":[],"imagenes":[Imagen("Cirros0.61","/home/ubuntu/cirros"),Imagen("Ubuntu22.02","/home/ubuntu/Ubuntu")
                                                                ,Imagen("CentOS","/home/ubuntu/centos")]}
    datos_sesion["gruposSeguridad"] = [GrupoSeguridad("Grupo1",[])]
    datos_sesion["slices"]= [editSlice.currentSlice(
    "SliceG7",
    "Anillo",
    "Grupo1",
    "192.168.100.0/24",
    [VM("vm1","Ubuntu22.02",5901,1024,51232,2,"ON"),
     VM("localServer","CentOS",5903,1024,20128,2,"OFF"),
     VM("vm2","CentOS",5903,2024,20128,1,"OFF"),
     VM("web_app","Ubuntu22.02",5904,1024,51232,2,"ON")],
     [("vm1","vm2"),("vm2","localServer"),("localServer","web_app"),("web_app","vm1")])]
    return datos_sesion


# Función Main
if __name__=="__main__":
    # Presentación del Grupo
    print("\n################ Orquestador G7 ################")
    print("--- Elianne P. Ticse Espinoza\t\t20185361")
    print("--- Oliver A. Bustamante Sanchez\t20190981")
    print("--- Percy De La Rosa Vera\t\t20192265")
    print("################################################")
    #login()
    print("Obteniendo datos")
    datos = obtenerDatos()
    datos_sesion_dict={}

    while True: 
        opt = util.printMenu(["Opciones disponibles para realizar:",
                              "Listar slices",
                              "Crear slice",
                              "Editar slice",
                              "Configurar Grupos de Seguridad",
                              "Administrar Imágenes de Disco",
                              "Salir"])
        if opt==1:
            list_slices = [[x.nombre] for x in datos["slices"]]
            if(len(list_slices)==0): print("No hay slices creados...")
            headers = ["Nombre del slice"]
            while(inp1:=input("Desea buscar un Slice (1) o listar todo (2): ")) not in ["1","2"]:
                print("No es una opcion valida")
            if(inp1=="1"):
                while(inp2:=input("Ingrese el nombre: ").strip()) =="":
                    print("Tiene que indicar un nombre**")
                print(f"Mostrando slices que contienen {inp2}")
                list_find = [[list_slices[x][0]] for x in [list_slices.index(x) for x in list_slices if inp2 in x[0]]]
                print(tabulate(list_find,headers=headers, tablefmt="fancy_grid"))
            else: 
                print(f"Mostrando todos los slices")
                print(tabulate(list_slices,headers=headers, tablefmt="fancy_grid"))
        if opt==2:
            s.crearSlice(datos["slices"],datos["gruposSeguridad"])
        if opt==3:
            list_slices_names = [x.nombre for x in datos["slices"]]
            if(len(list_slices_names)!=0):
                while(inp1:=input("Ingrese el nombre el slice:")) not in list_slices_names:
                    print("El nombre del Slice no exite...")
                idx = list_slices_names.index(inp1)
                editSlice.changeCurrent(datos["slices"][idx], datos["imagenes"],datos["gruposSeguridad"],datos["slices"])
                print("Ingresado al menu de Editar Slice")
                editSlice.start()
            else:
                print("No hay slices creados")
        if opt==4:
            r.main(datos["gruposSeguridad"])
        if opt==5:
            img.menuImg(datos["imagenes"])
        if opt==6:
            print("Saliendo del programa...")
            break
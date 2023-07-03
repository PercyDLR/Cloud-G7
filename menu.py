import modUtilidades as util
import funcionesMenu.VM as vm
import funcionesMenu.editSlice as editSlice
import funcionesMenu.Slice as s
import funcionesMenu.Imagen as img
import funcionesMenu.Flavor as flavor
import funcionesMenu.reglasSeguridad as sec
import funcionesMenu.Provider as prov
import funcionesMenu.Keypair as key
from login import IngresarCredenciales

from typing import Dict, List, Any
from tabulate import tabulate
from colorama import Fore, Style

from clases.VM import VM
from funcionesMenu.Imagen import Imagen
from funcionesMenu.reglasSeguridad import GrupoSeguridad



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

    print(f"""\n{Fore.RED}################################################
  ________                            _________ 
 /  _____/______ __ ________   ____   \\______  \\
/   \\  __\\_  __ \\  |  \\____ \\ /  _ \\      /    /
\\    \\_\\  \\  | \\/  |  /  |_> >  <_> )    /    / 
 \\______  /__|  |____/|   __/ \\____/    /____/  
        \\/            |__|                      
################################################{Fore.CYAN}
--- Elianne P. Ticse Espinoza\t\t20185361
--- Oliver A. Bustamante Sanchez\t20190981
--- Percy De La Rosa Vera\t\t20192265
{Fore.RED}################################################{Style.RESET_ALL}""")

    # Logueo
    IngresarCredenciales()
    datos = obtenerDatos()
    datos_sesion_dict={}

    # Se muestra el menú
    while True: 
        opt = util.printMenu(["Opciones disponibles para realizar:",
                              "Listar slices",
                              "Crear slice",
                              "Editar slice",
                              "Administrar Redes Provider",
                              "Administrar Keypairs",
                              "Administrar Flavors",
                              "Administrar Grupos de Seguridad",
                              "Administrar Imágenes de Disco",
                              "Gestión de VM",
                              "Salir"])
        if opt == 0:
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

        elif opt == 1:
            s.crearSlice(datos["slices"],datos["gruposSeguridad"])

        elif opt == 2:
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

        elif opt == 3:
            prov.menuProvider()
        
        elif opt == 4:
            key.menuKeypair()
        
        elif opt == 5:
            flavor.menuFlavor()

        elif opt == 6:
            sec.menuSecGroup()

        elif opt == 7:
            img.menuImg()
            
        elif opt == 8:
            vm.menuVM()
        else:
            print("\nSaliendo del programa...")
            break
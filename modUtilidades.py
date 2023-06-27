from colorama import Fore, Back, Style
from typing import List,Any
from simple_term_menu import TerminalMenu
from sys import argv
from tabulate import tabulate

def printMenu(lineas:List[str],multiselect:bool = False,comando:str|None = None,) -> int:
    "Imprime un menú para la interacción del usuario"
    
    try:
        idxEspacio = lineas.index(None) # type: ignore

        opciones = lineas[1:(idxEspacio+1)]
        opciones += [f"{idx}) {opt}" for idx,opt in enumerate(lineas[(idxEspacio+1):],1)]
    except ValueError:
        opciones = [f"{idx}) {opt}" for idx,opt in enumerate(lineas[1:],1)]

    # Lista las opciones
    terminal_menu = TerminalMenu(opciones,
                                 title=f"\n{lineas[0]}",
                                 clear_menu_on_exit=False,
                                 menu_cursor_style = ("fg_cyan", "bold"),
                                 menu_highlight_style = ("bg_cyan","bold"),
                                 multi_select_cursor_style = ("fg_red","bold"),
                                 multi_select_cursor_brackets_style = ("fg_gray",),
                                 search_highlight_style = ("bg_red", "bold"),
                                 multi_select=multiselect,
                                 preview_title="Detalle",
                                 # preview_title=f"{Style.BRIGHT}Detalle{Style.RESET_ALL}",
                                 preview_size=0.5,
                                 preview_command=comando)
    return terminal_menu.show()  # type: ignore
    
def validarOpcionNumerica(opt:str,max:int,) -> bool:
    "Verifica que la opción elegida sea válida"

    return opt.isdigit() and (int(opt)>=1 and int(opt)<=max)  

def printError(msg:str):
    print(f"{Fore.RED}{Style.BRIGHT}{msg}{Style.RESET_ALL}")

def printInput(msg:str):
    return input(f"{Fore.CYAN}{Style.BRIGHT}{msg}{Style.RESET_ALL}")
    
def buscarPorNombre(nombre:str,lista:List[Any]) -> Any:
    "Busca un elemento en una lista por su nombre"

    # Se buscan todas las coincidencias
    listaCoincidencias = []
    for elemento in lista:
        if nombre.lower() in elemento.nombre.lower():
            listaCoincidencias.append(elemento)
    
    # Se opera según la cantidad de coincidencias
    if len(listaCoincidencias) == 0:
        print(f"\nNo hubieron coincidencias buscando {nombre}")
        return
    elif len(listaCoincidencias) == 1 and nombre != "":
        print(f"\nSe encontró 1 coincidencia: {listaCoincidencias[0].nombre}")
        return listaCoincidencias[0]
    
    # Si hay más de un resultado, los listamos y le pedimos al usuario elegir
    else:
        terminal_menu = TerminalMenu([f"{idx}) {opt.nombre}" for idx,opt in enumerate(listaCoincidencias,1)],title="Listando Coincidencias")
        return listaCoincidencias[terminal_menu.show()] # type: ignore

def previewTable(tipo:str, info:dict):
    "Genera una tabla para la vista previa del menú"
    
    table_data = data = encabezado = []
    
    if tipo == "flavor":
        encabezado = ["ID","Name", "RAM", "vCPUs", "Disk"]
        data = [
            info["id"],
            info["name"],
            info["ram"],
            info["vcpus"],
            info["disk"],
        ]
        table_data.append(data)

    elif tipo == "red_subred":
        table_data2 = []

        print(f"{Fore.CYAN}Información de la Red:{Style.RESET_ALL}")
        encabezado = ["Nombre","Tipo","VLAN ID","Estado"]
        data = [
            info[0]["name"],
            info[0]["provider:network_type"],
            info[0]["provider:segmentation_id"] if info[0]["provider:network_type"] == "vlan" else "---",
            info[0]["status"]
        ]
        table_data.append(data)

        encabezado = [f"{Style.BRIGHT}{Fore.RED}{elemento}{Style.RESET_ALL}" for elemento in encabezado]
        print(tabulate(table_data, headers=encabezado))

        print(f"\n{Fore.CYAN}Información de las Subredes:{Style.RESET_ALL}")
        encabezado = ["Nombre","Versión","Gateway","CIDR","Pool","DNS"]
        table_data.clear()

        for subred in info[1]:
            data = [
                subred["name"],
                "IPv4" if subred["ip_version"] == 4 else "IPv6",
                subred["gateway_ip"],
                subred["cidr"],
                f"{subred['allocation_pools'][0]['start']}-{subred['allocation_pools'][0]['end']}",
                ",".join(subred["dns_nameservers"])
            ]
            table_data.append(data)

        encabezado = [f"{Style.BRIGHT}{Fore.RED}{elemento}{Style.RESET_ALL}" for elemento in encabezado]
        print(tabulate(table_data, headers=encabezado))
        return

    elif tipo == "sg_rule":
        encabezado = ["Eth Type", "Protocolo", "Puerto", "Dirección", "Rango IPs", "Descripción"]
        for regla in info:
            fila = [
                regla["ethertype"],
                regla["protocol"] if regla["protocol"] is not None else "Todos",
                regla["port_range_min"] if regla["port_range_min"] is not None else "---",
                regla["direction"],
                regla["remote_ip_prefix"] if regla["remote_ip_prefix"] is not None else "0.0.0.0/0",
                regla["description"]
            ]
            table_data.append(fila)

    encabezado = [f"{Style.BRIGHT}{Fore.RED}{elemento}{Style.RESET_ALL}" for elemento in encabezado]
    table = tabulate(table_data, headers=encabezado)
    print(table)

if __name__ == "__main__":

    info = eval(argv[1])
    previewTable(info[0],info[1])
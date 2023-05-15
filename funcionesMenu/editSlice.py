from dataclasses import dataclass,asdict
from tabulate import tabulate
from clases.VM import VM
from dataclasses import dataclass
import json
import random
import time
import math
from tabulate import tabulate
from funcionesMenu.Imagen import Imagen
from funcionesMenu.reglasSeguridad import GrupoSeguridad
import string


@dataclass
class currentSlice:
    nombre : str
    topologia : str
    grupo_seguridad : str
    red_cidr : str
    lista_vm : list[VM]
    conexiones : list[tuple[str,str]]

def generate_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def mostrarRequest(method,body,action):
    print(f"Method: {method}")
    print("URL: https://10.20.17.101/orquestador")
    body["user_token"] = "aidba8hd8g38bd2397gf29323d2"
    body["action"] = action
    body["slice_name"] = editingSlice.nombre
    print(f"Body:\n{json.dumps(body,indent=4)}")
    print("Send and waiting for response")
    time.sleep(2)
    respuesta = random.choices(["exito","error"],weights=[0.8,0.2])[0]
    print(f"Response: {respuesta}")
    razon=""
    if respuesta=="error": 
        razon="Hay una sobrecarga con el servidor"
        print(f"Ha ocurrido un error **{razon}**")
        return True
    return False


lista_imagenes :list[str]
lista_grupos:list[str]
editingSlice : currentSlice
list_slices : list[currentSlice]
def changeCurrent(slice_env,imagenes_env,grupos_env,slices_env):
    global editingSlice,lista_imagenes,lista_grupos,list_slices
    editingSlice = slice_env
    lista_imagenes= [x.nombre for x in imagenes_env]
    lista_grupos=[x.nombre for x in grupos_env]
    list_slices = slices_env

CLOSE = False

class Menu():
    def show_menu(self,opciones : list, funciones: list):
        global CLOSE
        if(len(opciones)!=len(funciones)): print("Error los parametros no tienen mismas cantidad de opciones."); return
        for i in range(len(opciones)): print(f"\t{i+1}) {opciones[i]}")
        print(f"\t{len(opciones)+1}) salir")
        while True:
            inp1 = input("Seleccione una opcion: ")
            if(inp1 == str(len(opciones)+1)): return
            if(inp1 in [str(x) for x in range(1,len(opciones)+1)]):
                funciones[int(inp1)-1]()
                if(CLOSE): return
                for i in range(len(opciones)): print(f"{i+1}) {opciones[i]}")
                print(f"{len(opciones)+1}) Salir")
            else:
                print("No es una opcion valida...")

    def show(self):
        global list_slices
        opcionesMain = ["Listar VMs","Listar conexiones","Cambiar Grupo de seguridad" ,"Iniciar/Detener VM", "Añadir VM", "Eliminar Slice"]
        funcionesMain = [self.listVMs, self.mostrarConexiones, self.cambiarGrupoS,self.ini_det_vm, self.add_vm, self.delete_self]
        self.show_menu(opcionesMain, funcionesMain)
        print("Saliendo de la edición de slice...")
    def listVMs(self):
        global editingSlice
        inp1=""
        while True:
            inp1= input("Desea buscar(1) o listar todo(2)?: ")
            if(inp1 in ["1","2"]): break
            else : print("No es una opcion valida: ")
        if(inp1=="1"):
            inp2=""
            while True:
                inp2=input("Ingrese el nombre: ").strip()
                if(inp2==""):
                    print("No ha ingresado un nombre valido*")
                else: break
            vm_prelist = [vm for vm in editingSlice.lista_vm if inp2 in vm.nombreVM]
            vm_list = [list(vars(vm).values()) for vm in vm_prelist]
            headers = ["Nombre", "OS", "VNC", "Memoria", "Storage", "VCPUs", "Estado"]
            if(mostrarRequest("POST",{"busqueda_tipo":"filtro", "buscar": inp2 },"listar_vms")): return
            print(f"Mostrando coincidencias para {inp2}")
            print(tabulate(vm_list,headers=headers, tablefmt="fancy_grid"))
        else:        
            vm_list = [list(vars(vm).values()) for vm in editingSlice.lista_vm]
            headers = ["Nombre", "OS", "VNC", "Memoria", "Storage", "VCPUs", "Estado"]
            if(mostrarRequest("POST",{"busqueda_tipo":"todo"},"listar_vms")): return
            print(tabulate(vm_list,headers=headers, tablefmt="fancy_grid"))
    def cambiarGrupoS(self):
        global editingSlice
        global lista_grupos
        if(mostrarRequest("POST",{"busqueda_tipo":"todo"},"listar_grupos")): return
        actualName = editingSlice.grupo_seguridad
        print("Mostrando grupos de seguridad: ")
        lista_tabla = [[x,"Actual" if x==actualName else "***"] for x in lista_grupos]
        headers = ["Grupo de seguridad","Activado"]
        print(tabulate(lista_tabla,headers=headers, tablefmt="fancy_grid"))
        while(inp1:=input("Ingrese el nombre del grupo: ").strip()) not in lista_grupos:
            print("No ha ingresado un grupo existente**")
        if(inp1==actualName): print("No se ha seleccionado un nuevo grupo..."); return
        print("Cambiando grupo...")
        time.sleep(1)
        if(mostrarRequest("POST",{"grupo":inp1},"updategrupo")): return
        print("Se ha cambiado el grupo exitosamente")

    def ini_det_vm(self):
        global editingSlice
        inp1=""
        vm_list =[]
        while True:
            inp1= input("Ingrese el nombre de la vm que desea iniciar/detener: ").strip()
            if(inp1==""): print("No es un nombre valido")
            else: break
        vm_list = [vm for vm in editingSlice.lista_vm if (inp1 == vm.nombreVM)]
        if(len(vm_list)!=1): print("No se ha encontrado la vm indicado"); return
        vm = vm_list[0]
        if(vm.estado.lower()== "on"):
            print("Apagando equipo...")
            time.sleep(2)
            error=mostrarRequest("POST",{"vm_nombre":vm.nombreVM},"apagar")
            time.sleep(2)
            if(error): return
            vm.estado="OFF"
            print(f"La vm {vm.nombreVM} se ha apagado")
        else:
            print("Encendiendo equipo...")
            time.sleep(2)
            error=mostrarRequest("POST",{"vm_nombre":vm.nombreVM},"encender")
            time.sleep(2)
            if(error): return
            vm.estado="ON"
            print(f"La vm {vm.nombreVM} se ha encendido")
            
    def add_vm(self):
        global lista_imagenes
        global editingSlice
        while(name := input("Ingrese el nombre de la vm: ").strip()) in [vm.nombreVM for vm in editingSlice.lista_vm] or name=="" or " " in name:
            print("No puede repetir el nombre de otra vm, incluir espacios o estar vacio*")
        print("Seleccione una imagen para la vm")
        for i in range(len(lista_imagenes)): 
            print(f"{i+1}) {lista_imagenes[i]}")
        while(imagen := input("Indique la imagen: ").strip()) not in [str(x) for x in range(1,len(lista_imagenes)+1)]:
            print("Opción no valida")
        imagen = lista_imagenes[int(imagen)-1]
        while((memoria := input("Indique la memoria RAM en MB(max 1400): ").strip()).isdigit()==False or int(memoria)>1400):
            print("No ha ingresado un valor aceptable:")
        memoria = int (memoria)
        while(storage := input("Indique el storage en MB(max 5200): ").strip()).isdigit()==False or int(storage)>5200:
            print("No ha ingresado un valor aceptable:")
        storage = int (storage)
        while(vcpus := input("Indique los vcpu que necesitara su vm(max 2): ").strip()).isdigit()==False or int(vcpus)>2:
            print("No ha ingresado un valor aceptable:")
        print("Creando vm...")
        time.sleep(1)
        vcpus = int (vcpus)
        vnc = max([x.puertoVNC for x in editingSlice.lista_vm])+1
        estado = "ON"
        vm=VM(name,imagen,vnc,memoria,storage,vcpus,estado)
        error= mostrarRequest("POST",asdict(vm),"crear_vm")
        time.sleep(2)
        if(error): return
        editingSlice.lista_vm.append(vm)
        print("Su vm se ha creado con exito")
        vm_list = [list(vars(vm).values())]
        self.instalarConexion(name)
        headers = ["Nombre", "OS", "VNC", "Memoria", "Storage", "VCPUs", "Estado"]
        print(tabulate(vm_list,headers=headers, tablefmt="fancy_grid"))
        print(f"Si desea conectarse a su VM puede realizar una conexion VNC a la direccion 10.20.17.101 en el puerto {vnc}")
        print(f"Su contraseña para conectarse es {generate_password()}, guardela dado que esta no se volvera a proveer")

    def instalarConexion(self,vm_name):
        global editingSlice
        if(editingSlice.topologia.lower()=="arbol"):
            cant =len(editingSlice.lista_vm)
            vm_num = cant+1
            vm_cnidx=  math.floor(vm_num/2)
            vm_cn= editingSlice.lista_vm[vm_cnidx-1]
            conexion = (vm_cn.nombreVM, vm_name)
            editingSlice.conexiones.append(conexion)
        elif(editingSlice.topologia.lower()=="anillo"):
            editingSlice.conexiones.pop()
            conexion1 = (editingSlice.lista_vm[0].nombreVM, vm_name)
            conexion2 = (editingSlice.lista_vm[-2].nombreVM, vm_name)
            editingSlice.conexiones.append(conexion1)
            editingSlice.conexiones.append(conexion2)
        elif(editingSlice.topologia.lower()=="lineal"):
            editingSlice.conexiones.append((editingSlice.lista_vm[-1].nombreVM,vm_name))

    def mostrarConexiones(self):
        global editingSlice
        conexiones =  editingSlice.conexiones
        if(mostrarRequest("POST",{"listar_conextions":"all"},"listar_conexiones")): return
        list_vm = [x.nombreVM for x  in editingSlice.lista_vm]
        if(list_vm==0): print("No hay vms creadas aun...");return
        list_cons=[]
        for x in list_vm:
            cont = 0
            vms =""
            for y,z in conexiones:
                if(y == x):
                    vms+= (z) if cont==0 else (","+z)
                    cont+=1
                elif(z == x):
                    vms+= (y) if cont==0 else (","+y)
                    cont+=1
            if(editingSlice.nombre.lower()=="bus"):
                cont=1; vms="Todas"
            if(editingSlice.nombre.lower()=="malla"):
                vms="Todas"; cont=len(list_vm)-1
            list_cons.append([x,str(cont),vms])
        headers = ["VM Nombre", "Cant Conexiones","Equipos conectados"]
        print(f"Topologia del slice: {editingSlice.topologia.title()}")
        print(tabulate(list_cons,headers=headers, tablefmt="fancy_grid"))
    def delete_self(self):
        global CLOSE
        global editingSlice
        global list_slices
        inp1=input("Estas seguro de querer borrar el slice presente?:\nEscriba: si, quiero borrar el slice\n")
        if inp1=="si, quiero borrar el slice":
            print("Borrando slice...")
            error=mostrarRequest("POST", {},"eliminar_slice")
            if(error): return
            time.sleep(1)
            print("El slice ha sido borrado")
            time.sleep(1)
            list_slices.remove(editingSlice)
            CLOSE=True
        else:
            print("Se cancela la operacion...")

def start():
    menu=Menu()
    menu.show()

if __name__ == "__main__":
    start()
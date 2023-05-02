import subprocess
import json

# Muestra las opciones, pide eñegir una y lo valida
def menuPrincipal() -> int:
    print("\n###################### Menu ####################")
    print("\nAcciones disponibles para realizar:")
    # TODO: Esto está sujeto a cambios
    print("\t1) Listar slices disponibles")
    print("\t2) Crear slice")
    print("\t3) Editar slices disponibles")
    print("\t4) Eliminar slice")
    print("\t5) Importar imagen a VM")
    print("\t6) Eliminar imagen de VM")
    print("\t7) Configuración de red (VMs)")
    print("\t8) Salir")

    # Se pide elegir una opción
    try:
        opt = int(input("> Elija una opción [1-8]: "))  # Se verifica que sea un número
        print()
        if opt>=1 and opt<=7:                           # Se verifica que sea una opción válida
            return opt
        else:
            print("Debe ingresar una opción válida")
    except ValueError:
        print("Debe ingresar una opción válida")

def listSlices():
    pass

def createSlice():
    nameSlice = input("\nIngrese nombre del Slice a crear:")
    

def editSlice():
    while(True):
        listSlices()
        slice = input("\nSeleccione un slice: ")
        print("\nAcciones disponibles para realizar:")
        print("\t1) Agregar nodo")
        print("\t2) Agregar enlace")
        print("\t3) Agregar VM")
        print("\t4) Salir")
        
        # Se pide elegir una opción
        try:
            opt = int(input("> Elija una opción [1-4]: "))  # Se verifica que sea un número
            print()
            if opt>=1 and opt<=4:                           # Se verifica que sea una opción válida
                if opt==1:
                    pass
                if opt==2:
                    pass
                if opt==3:
                    pass
                if opt==4:
                    print("Regresando al menu principal...")
                    break
            else:
                print("Debe ingresar una opción válida")
        except ValueError:
            print("Debe ingresar una opción válida")



    
# Función Main
if __name__=="__main__":
    
    # Presentación del Grupo
    print("\n################ Orquestador G7 ################")
    print("--- Elianne P. Ticse Espinoza\t\t20185361")
    print("--- Oliver A. Bustamante Sanchez\t20190981")
    print("--- Percy De La Rosa Vera\t\t20192265")
    print("################################################")

    while True:
        opt = menuPrincipal() # Se muestra el menu principal y se elije una opción

        # Se trabaja la opción:
        if opt==1:
            pass
        if opt==2:
            pass
        if opt==3:
            pass
        if opt==4:
            pass
        if opt==5:
            pass
        if opt==6:
            pass
        if opt==7:
            pass
        if opt==8:
            print("Saliendo del programa...")
            break

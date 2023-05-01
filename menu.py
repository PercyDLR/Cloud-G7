import subprocess
import json

# Muestra las opciones, pide eñegir una y lo valida
def menuPrincipal() -> int:
    print("\nAcciones Disponibles para realizar:")
    # TODO: Esto está sujeto a cambios
    print("\t1) CRUD VMs")
    print("\t2) CRUD Redes")
    print("\t3) CRUD Bridges")
    print("\t4) CRUD VMs")
    print("\t5) Salir")

    # Se pide elegir una opción
    try:
        opt = int(input("> Elija una opción [1-5]: "))  # Se verifica que sea un número
        print()
        if opt>=1 and opt<=5:                           # Se verifica que sea una opción válida
            return opt
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
            print("Saliendo del programa...")
            break

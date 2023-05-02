import modUtilidades as util
import Slice as s
import subprocess
import json

def menuPrincipal() -> int:
    "Muestra las opciones, pide elegir una y lo valida"
    
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
    opt = input(f"> Elija una opción [1-8]: ")
    if util.validarOpcionNumerica(opt,8):
        print()
        return int(opt)
    else:
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
            s.listarSlices()
        if opt==2:
            s.crearSlice()
        if opt==3:
            s.editarSlice()
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

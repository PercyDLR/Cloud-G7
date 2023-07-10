import modUtilidades as util
import funcionesMenu.VM as vm
import funcionesMenu.Slice as s
import funcionesMenu.Imagen as img
import funcionesMenu.Flavor as flavor
import funcionesMenu.reglasSeguridad as sec
import funcionesMenu.Provider as prov
import funcionesMenu.Keypair as key
from login import IngresarCredenciales
import variables as var
from colorama import Fore, Style

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

    # Se muestra el menú
    while True: 
        opt = util.printMenu([f"Opciones del Slice {var.dic['project']}:",
                              "Gestión de Slices",
                              "Elegir Zonas de Disponibilidad",
                              "Administrar Redes Provider",
                              "Administrar Keypairs",
                              "Administrar Flavors",
                              "Administrar Grupos de Seguridad",
                              "Administrar Imágenes de Disco",
                              "Gestión de VM",
                              "Salir"])
        if opt == 0:
            s.menuSlice(login=False)

        elif opt == 1:
            zonas = ["Worker1","Worker2","Worker3"]

            preselect = [int(zona[6:7])+1 for zona in var.dic['zonasElegidas']]

            idxs = util.printMenu(["Elegir zonas de disponibilidad","Cancelar",None]+zonas,multiselect=True,
                                  preselect=preselect) #type: ignore
            
            if 0 in idxs: continue # type:ignore

            zonasElegidas = []
            print(idxs)
            for idx in idxs: # type: ignore
                zonasElegidas.append(zonas[idx-2])
            
            var.dic['zonasElegidas'] = zonasElegidas

            print(zonasElegidas)
            
            # Se modifica la última línea para tener las zonas de disponibilidad deseadas
            lines = open("credencial.txt", 'r').readlines()
            lines[-1] = str(zonasElegidas)
            open("credencial.txt", 'w').writelines(lines)

            util.printSuccess("\nZonas de disponibilidad actualizadas!")

        elif opt == 2:
            prov.menuProvider()
        
        elif opt == 3:
            key.menuKeypair()
        
        elif opt == 4:
            flavor.menuFlavor()

        elif opt == 5:
            sec.menuSecGroup()

        elif opt == 6:
            img.menuImg()
            
        elif opt == 7:
            vm.menuVM()
        else:
            util.printError("\nSaliendo del programa...")
            break

# Cloud-G7
Proyecto orientado a la administración y orquestación de recursos virtuales por medio de Openstack. 

### Integrantes
Los integrantes del grupo son:
| Nombres y Apellidos          |  Código  |
| ---------------------------- |:--------:|
| Elianne P. Ticse Espinoza    | 20185361 |
| Oliver A. Bustamante Sanchez | 20190981 |
| Percy De La Rosa Vera        | 20192265 |

### Consideraciones
- Debido a la dependencia `simple_term_menu`, el script **solo puede ser usado en entornos Linux** (Nativo o WSL).
- La dependencia `tkinter`, usada para desplegar el selector de archivos no funciona en todos los entornos:
    - **Ubuntu:** Ejecutar `sudo apt install python3-tkinter`.
    - **Fedora:** Ninguna acción necesaria.
    - **ArchLinux:** Ejecutar `sudo pacman -S tk`.
    - **WSL:** Ademaś del paso de Ubuntu, es necesario habilitar la ejecución de GUI, como se indica [aquí](https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps).
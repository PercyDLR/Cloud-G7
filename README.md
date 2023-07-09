# Cloud-G7
Proyecto orientado a la administración y orquestación de recursos virtuales por medio de Openstack. 

### Desarrolladores
Los integrantes del grupo y desarrolladores del proyecto son:
| Nombres y Apellidos          |  Código  |
| ---------------------------- |:--------:|
| Elianne P. Ticse Espinoza    | 20185361 |
| Oliver A. Bustamante Sanchez | 20190981 |
| Percy De La Rosa Vera        | 20192265 |

### Consideraciones Importantes
- Debido a la dependencia `simple_term_menu`, el script **solo puede ser usado en entornos Linux** (Nativo o WSL).
- La dependencia `tkinter`, usada para desplegar el selector de archivos no funciona en todos los entornos:
    - **Ubuntu:** Ejecutar `sudo apt install python3-tkinter`.
    - **Fedora:** Ninguna acción necesaria.
    - **ArchLinux:** Ejecutar `sudo pacman -S tk`.
    - **WSL:** Ademaś del paso de Ubuntu, es necesario habilitar la ejecución de GUI, como se indica [aquí](https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps).

### Uso
1. Clonar el repositorio
2. Ingresar al directorio `Cloud-G7`
3. Crear el entorno virtual: `python3 -m venv .venv/`
4. Ingresar al entorno virtual:

- **Entorno Windows:** `tutorial-env\Scripts\activate.bat`
- **Entorno Linux:** `. ./venv/bin/activate`

5. Instalar las dependencias necesarias: `pip install -r requirements.txt`
6. Modificar el archivo `variables.py`:

```python
# Ingresar la IP del controlador Openstack
dirrecionIP = "1.2.3.4"
```

7. Iniciar el programa: `python3 menu.py`
8. Loguearse y administrar distintos proyectos de Openstack
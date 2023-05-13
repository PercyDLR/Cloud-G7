from dataclasses import dataclass

@dataclass
class VM:
    nombreVM :str
    nombreImg : str
    puertoVNC : int
    memoria : int
    storage : int
    vcpus : int
    estado : str
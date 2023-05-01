from clases.EnlaceTAPBridge import EnlaceTAPBridge
from clases.EnlaceBridges import EnlaceBridges
from clases.LinuxBridge import LinuxBridge
from clases.VM import VM
from typing import List

class TopologiaBridges:
    def __init__(self, idTopologia:str, listaVM:List[VM], listaBr:List[LinuxBridge], listaEnlaceTAP:List[EnlaceTAPBridge], listaEnlaceBr: List[LinuxBridge]) -> None:
        self.idTopologia = idTopologia
        self.listaVM = listaVM
        self.listaBr = listaBr
        self.listaEnlaceTAP = listaEnlaceTAP
        self.listaEnlaceBr = listaEnlaceBr

    def print_topology(self) -> dict:
        return(self.__dict__)
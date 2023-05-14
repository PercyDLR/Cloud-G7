from clases.EnlaceTAPOVS import EnlaceTAPOVS
from clases.DHCP import DHCP
from clases.OvS import OvS
from clases.VM import VM
from typing import List

class TopologiaOvS:
    def __init__(self, idTopologia:str, listaVM:List[VM], ovs:OvS, listaEnlaceTAP:List[EnlaceTAPOVS], dhcp:DHCP) -> None:
        self.idTopologia = idTopologia
        self.listaVM = listaVM
        self.ovs = ovs
        self.listaEnlaceTAP = listaEnlaceTAP
        self.dhcp = dhcp
    
    def print_topology(self) -> dict:
        return(self.__dict__)
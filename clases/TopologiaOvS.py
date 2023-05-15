from clases.EnlaceTAPOVS import EnlaceTAPOVS
from clases.DHCP import DHCP
from clases.OvS import OvS
from clases.VM import VM
from dataclasses import dataclass


@dataclass
class TopologiaOvS:
    idTopologia = str
    listaVM = list[VM]
    ovs = OvS
    listaEnlaceTAP = list[EnlaceTAPOVS]
    dhcp = DHCP

    def print_topology(self) -> dict:
        return(self.__dict__)
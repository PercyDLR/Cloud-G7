from dataclasses import dataclass

@dataclass
class EnlaceTAPOVS:
    nombrVM= str
    nombreOVS = str
    vxlan_vni = int

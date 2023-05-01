class DHCP:
    def __init__(self, idSubred:str, red:str, ip:str, rangoIPs:str) -> None:
        self.idSubred = idSubred
        self.red = red
        self.ip = ip
        self.rangoIPs = rangoIPs
from typing import List

class VM:
    def __init__(self, parametros:List[str]) -> None:
        self.nombreVM = parametros[0]
        self.nombreImg = parametros[1]
        self.puertoVNC = parametros[2]
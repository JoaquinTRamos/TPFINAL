from FabricaPaquete import FabricaPaquetes
from Paquete import *

class PaqueteManager():
    def __init__(self) -> None:
        self.fabricaPaquete = FabricaPaquetes()
        
    def contarTicksFabricaPaquete(self, tiempoPorTick:int) -> None:
        self.fabricaPaquete.contarTicks(tiempoPorTick)
    
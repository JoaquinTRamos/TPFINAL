import random as r
from Paquete import *

# Esta .py se encargara de la produccion de paquetes, simulando entrada de los mismos
class FabricaPaquetes():
    
    def __init__(self) -> None:
        self.tiempoParaProxPaquete: int = 0
        self.n_paquetes: int = 0
    
    def tiempo_aleatorio(self, mu: int, sigma: int) -> int:
        return round(r.normalvariate(mu, sigma))
    
    def __tiempoEntrePaquetes(self) -> None: # Esto devolvera la cantidad de tiempo para que llegue un nuevo paquete
        self.tiempoParaProxPaquete = self.tiempo_aleatorio(self)
     
    def __descontarTiempo(self, tiempoPorTick:int) -> None: # Esta funcion ajusta la cantidad de tiempo entre c/tick
        self.tiempoParaProxPaquete -= tiempoPorTick
        pass

    def contarTicks(self, tiempoPorTick:int) -> None: # Esta funcion se encarga de contar los ticks y descontar tiempo
    
        if(self.tiempoParaProxPaquete > 1):
            self.__descontarTiempo(tiempoPorTick)
            return None
    # TODO Esta funcion llama a RouterManager para que luego llame a fabricarPaquete
    
    def fabricarPaquete(self) -> Paquete: # Esta seria la funcion que se callea por tick
    
        nuevoPaquete = Paquete(Id = self.n_paquetes) 
        self.n_paquetes += 1

        self.__tiempoEntrePaquetes() 
        return nuevoPaquete
    
    
    def __str__(self) -> str:
        return f"Tiempo entre paquetes: {self.tiempoParaProxPaquete}, Cantidad de paquetes: {self.n_paquetes}"
    

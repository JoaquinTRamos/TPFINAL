import random as r
from Paquete import *

# Esta .py se encargara de la produccion de paquetes, simulando entrada de los mismos
class FabricaPaquetes():
    
    def __init__(self) -> None:
        self.tiempoParaProxPaquete: int = 0
        self.n_paquetes: int = 0
        self.mu = 2
        self.sigma = 1
    
    def __tiempo_aleatorio(self) -> int:
        return round(r.normalvariate(self.mu, self.sigma), 0)
    
    def __tiempoEntrePaquetes(self) -> None: # Esto devolvera la cantidad de tiempo para que llegue un nuevo paquete
        self.tiempoParaProxPaquete = self.__tiempo_aleatorio()
     
    def __descontarTiempo(self, tiempoPorTick:int) -> None: # Esta funcion ajusta la cantidad de tiempo entre c/tick
        self.tiempoParaProxPaquete -= tiempoPorTick
        pass

    def contarTicks(self, tiempoPorTick:int) -> None: # Esta funcion se encarga de contar los ticks y descontar tiempo
    
        if(self.tiempoParaProxPaquete > 1):
            self.__descontarTiempo(tiempoPorTick)
            return None
        
        from RoutingSim import instance
        instance.routerManager.requestPaquete()
    
    def fabricarPaquete(self, origen: int) -> Paquete:
        
        # Selecciona una coordenada al azar que no sea la misma que el origen
        from RoutingSim import instance

        destino:int = instance.routerManager.getRandomAvailableRouter().coordenada
        while destino == origen:
            destino = instance.routerManager.getRandomAvailableRouter().coordenada
        
        nuevoPaquete = Paquete(id = self.n_paquetes, metadata= Metadata(origen=origen,destino=destino)) 
        self.n_paquetes += 1

        self.__tiempoEntrePaquetes() 
        return nuevoPaquete
    
    def set_timer(self, mu: int, sigma:int) -> None:
        self.mu = mu
        self.sigma = sigma
    
    
    def __str__(self) -> str:
        return f"Tiempo entre paquetes: {self.tiempoParaProxPaquete}, Cantidad de paquetes: {self.n_paquetes}"
    

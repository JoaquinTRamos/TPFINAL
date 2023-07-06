import random as r
from Router import *

# Esta .py se encargara de la produccion de routers, simulando entrada de los mismos
class FabricaRouters():
    
    def __init__(self) -> None:
        self.tiempoParaProxRouter: int = 0
        self.n_routers: int = 0

    def tiempo_aleatorio(mu: int, sigma: int) -> int:
        return round(r.normalvariate(mu, sigma))
    
    def __tiempoEntreRouters(self) -> None: # Esto devolvera la cantidad de tiempo para que llegue un nuevo router
        self.tiempoParaProxRouter = self.tiempo_aleatorio()
     
    def __descontarTiempo(self, tiempoPorTick:int) -> None: # Esta funcion ajusta la cantidad de tiempo entre c/tick
        self.tiempoParaProxRouter -= tiempoPorTick
        pass

    def contarTicks(self, tiempoPorTick:int) -> None: # Esta funcion se encarga de contar los ticks y descontar tiempo
    
        if(self.tiempoParaProxRouter > 1):
            self.__descontarTiempo(tiempoPorTick)
            return None
    # TODO Esta funcion llama a RouterManager para que luego llame a fabricarRouter
    
    def fabricarRouter(self) -> Router: # Esta seria la funcion que se callea por tick
    
        nuevoRouter = Router(self.n_routers)
        self.n_routers += 1

        self.__tiempoEntreRouters() 
        return nuevoRouter
    
    
    def __str__(self) -> str:
        return f"Tiempo entre routers: {self.tiempoParaProxRouter}, Cantidad de routers: {self.n_routers}"
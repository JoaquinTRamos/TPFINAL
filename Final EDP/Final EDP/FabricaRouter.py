import random as r
from Router import *
from tenacity import retry

# Esta .py se encargara de la produccion de routers, simulando entrada de los mismos
class FabricaRouters():
    
    def __init__(self) -> None:
        self.tiempoParaProxRouter: int = 0
        self.n_routers: int = 0

    def __tiempo_aleatorio(self, mu: int = 2, sigma: int = 1) -> int:
        return abs(round(r.normalvariate(mu, sigma), 0))
    
    def __tiempoEntreRouters(self) -> None: # Esto devolvera la cantidad de tiempo para que llegue un nuevo router
        self.tiempoParaProxRouter = self.__tiempo_aleatorio() #TODO poner mu y sigma acordes
     
    def __descontarTiempo(self, tiempoPorTick:int) -> None: # Esta funcion ajusta la cantidad de tiempo entre c/tick
        self.tiempoParaProxRouter -= tiempoPorTick
        pass

    @retry
    def contarTicks(self, tiempoPorTick:int) -> None: # Esta funcion se encarga de contar los ticks y descontar tiempo
        
        if(self.tiempoParaProxRouter > 1):
            self.__descontarTiempo(tiempoPorTick)
            return None
    
        from RoutingSim import instance
        instance.routerManager.addRouter(self.fabricarRouter())

    def fabricarRouter(self) -> Router: # Esta seria la funcion que se callea por tick
    
        coordenada = r.randint(1,10) #TODO Implementar cantidad de routers por parametro
        nuevoRouter = Router(coordenada = coordenada)
        self.n_routers += 1

        self.__tiempoEntreRouters() 
        return nuevoRouter
    
    
    def __str__(self) -> str:
        return f"Tiempo entre routers: {self.tiempoParaProxRouter}, Cantidad de routers: {self.n_routers}"
    
    
#TESTING -- TESTING -- TESTING
if __name__ == "__main__":

    fabrica = FabricaRouters()
    for i in range(100):
        fabrica.contarTicks(1)
        print(fabrica, i)
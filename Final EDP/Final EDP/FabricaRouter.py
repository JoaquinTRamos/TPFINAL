import random as r
from Router import *
from tenacity import retry

# Esta .py se encargara de la produccion de routers, simulando entrada de los mismos
class FabricaRouters():
    
    def __init__(self) -> None:
        self.tiempoParaProxRouter: int = 0
        self.n_routers: int = 0
        self.mu = 0
        self.sigma = 0
        self.limiteRouters:int = 100000

    def set_limite_routers(self, limite_routers:int) -> None:
        self.limiteRouters = limite_routers

    def __tiempo_aleatorio(self) -> int:
        return abs(round(r.normalvariate(self.mu, self.sigma), 0))
    
    def __tiempoEntreRouters(self) -> None: # Esto devolvera la cantidad de tiempo para que llegue un nuevo router
        self.tiempoParaProxRouter = self.__tiempo_aleatorio()
     
    def __descontarTiempo(self, tiempoPorTick:int) -> None: # Esta funcion ajusta la cantidad de tiempo entre c/tick
        self.tiempoParaProxRouter -= tiempoPorTick
        pass

    @retry
    def contarTicks(self, tiempoPorTick:int) -> None: # Esta funcion se encarga de contar los ticks y descontar tiempo
        
        if(self.tiempoParaProxRouter > 1):
            self.__descontarTiempo(tiempoPorTick)
            return None
        
        if(self.mu == 0 and self.sigma == 0): # Si ambos son 0 entonces NO PRODUCE NUEVOS ROUTERS!!!
            return None
    
        from RoutingSim import instance
        from RouterManager import DuplicateRouterException

        try:
            newRouter = self.fabricarRouter()
            instance.routerManager.addRouter(newRouter)
            newRouter.set_estado(RouterEstado.AGREGADO)            
            newRouter.set_estado(RouterEstado.ACTIVO)            
        except DuplicateRouterException:
            pass
    @retry
    def fabricarRouter(self) -> Router: # Esta seria la funcion que se callea por tick
        coordenada = r.randint(1,self.limiteRouters+2) # TO DO: si se inicia con 0 routers el limite se rompe
                                                           #: cachear la excepcion de router duplicado
        nuevoRouter = Router(coordenada = coordenada)
        self.n_routers += 1

        self.__tiempoEntreRouters() 
        return nuevoRouter
    
    def set_routers(self, cant_routers:int) -> None:
        for i in range(cant_routers):
            self.buildRouter()
        self.__tiempoEntreRouters()

    @retry
    def buildRouter(self):

            coordenada = r.randint(1,self.limiteRouters+2)
            nuevoRouter = Router(coordenada = coordenada)
            self.n_routers += 1
            
            from RoutingSim import instance
            from RouterManager import DuplicateRouterException
            try:
                instance.routerManager.addRouter(nuevoRouter)
                nuevoRouter.set_estado(RouterEstado.AGREGADO)            
                nuevoRouter.set_estado(RouterEstado.ACTIVO)            

            except DuplicateRouterException:
                pass

    def set_timer(self, mu: int, sigma:int) -> None:
        self.mu = mu
        self.sigma = sigma

    
    
    def __str__(self) -> str:
        return f"Tiempo entre routers: {self.tiempoParaProxRouter}, Cantidad de routers: {self.n_routers}"
    
    
#TESTING -- TESTING -- TESTING
if __name__ == "__main__":

    fabrica = FabricaRouters()
    for i in range(100):
        fabrica.contarTicks(1)
        print(fabrica, i)
from TimeManager import TimeManager
from PaqueteManager import PaqueteManager
from RouterManager import RouterManager

# Esta clase representa la simulacion entera, y ante cualquier consulta sobre los managers debera pasar por la instancia "instance".
class RoutingSim():
    def __init__(self) -> None:
        self.timeManager = TimeManager()
        self.paqueteManager = PaqueteManager()
        self.routerManager = RouterManager()
        # Atributo de tiempo de inicio de simulacion
        self.suscribir_acciones()
        pass

    def suscribir_acciones(self) -> None: # Aca se establece el orden para el evento de on_tick
        self.timeManager.subscribir_accion(self.routerManager.contarTicksFabricaRouter)
        self.timeManager.subscribir_accion(self.paqueteManager.contarTicksFabricaPaquete)
        self.timeManager.subscribir_accion(self.routerManager.checkearCaidaTick)
        self.timeManager.subscribir_accion(self.routerManager.enviarMensajesTick)

    # Metodo para reiniciar la simulacion
    def reset(self) -> None:
        pass

    def iniciar(self, cant_routers:int, mu_router: int, sigma_router: int, mu_paquete: int, sigma_paquete: int, tiempo: int,\
                    porcentaje_caida_router:int) -> None:
        # Set-up <-- Cantidad de routers para arrancar simulacion, mu sigma de paquete y router, tiempo simulacion, % caida routers
        self.timeManager.set_tiempo_simulacion(tiempo*10)
        self.routerManager.fabricaRouter.set_timer(mu_router,sigma_router)
        self.routerManager.fabricaRouter.set_routers(cant_routers)
        

        # Agarra el tiempo
        while self.timeManager.get_tiempo_simulacion() >= 0:
            self.timeManager.next_tick()
        
        # Recoleccion / Visualizacion de Informacion

instance = RoutingSim()

instance.iniciar(cant_routers=4, tiempo=10) # Comienza la simulacion <- Temporal para probar implementacion de tiempo
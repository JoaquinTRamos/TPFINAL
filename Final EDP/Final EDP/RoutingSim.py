from TimeManager import TimeManager
from PaqueteManager import PaqueteManager
from RouterManager import RouterManager
from SystemLogs import SystemLogs

# Esta clase representa la simulacion entera, y ante cualquier consulta sobre los managers debera pasar por la instancia "instance".
class RoutingSim():
    def __init__(self) -> None:
        self.timeManager = TimeManager()
        self.paqueteManager = PaqueteManager()
        self.routerManager = RouterManager()
        self.systemLogs = SystemLogs()
        
        self.suscribir_acciones()
        pass

    def suscribir_acciones(self) -> None: # Aca se establece el orden para el evento de on_tick
        self.timeManager.subscribir_accion(self.routerManager.contarTicksFabricaRouter)
        self.timeManager.subscribir_accion(self.paqueteManager.contarTicksFabricaPaquete)
        self.timeManager.subscribir_accion(self.routerManager.enviarMensajesTick)
        self.timeManager.subscribir_accion(self.routerManager.checkearCaidaTick)
        self.timeManager.subscribir_accion(self.routerManager.rehabilitacionRoutersTick)

    # Metodo para reiniciar la simulacion
    def reset(self) -> None:
        pass

    def iniciar(self, cant_routers:int, mu_router: int, sigma_router: int, mu_paquete: int, sigma_paquete: int, tiempo: int,\
                    porcentaje_caida_router:int) -> None:
        # Set-up <-- Cantidad de routers para arrancar simulacion, mu sigma de paquete y router, tiempo simulacion, % caida routers
        self.timeManager.set_tiempo_simulacion(tiempo*10)
        self.routerManager.fabricaRouter.set_timer(mu_router*10,sigma_router*10)
        self.routerManager.fabricaRouter.set_limite_routers(cant_routers*10000)
        self.routerManager.fabricaRouter.set_routers(cant_routers)
        self.paqueteManager.fabricaPaquete.set_timer(mu_paquete*10,sigma_paquete*10)
        self.routerManager.set_prob_caida(porcentaje_caida_router)
        self.timeManager.set_tiempo_inicio() # Esta tiene que ser el ultima set up
        # Agarra el tiempo
        print("COMIENZA_SIMULACION")
        while self.timeManager.get_tiempo_simulacion() >= 0:
            self.timeManager.next_tick()
        
        print("SIMULACION TERMINADA\n")
        # Recoleccion / Visualizacion de Informacion
        self.systemLogs.exportLogs()
        self.routerManager.exportAllRouterLogs()

instance = RoutingSim()


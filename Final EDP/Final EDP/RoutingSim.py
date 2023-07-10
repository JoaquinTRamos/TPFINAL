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
        self.timeManager.subscribir_accion(self.routerManager.checkearCaidaTick)
        self.timeManager.subscribir_accion(self.routerManager.enviarMensajesTick)

    # Metodo para reiniciar la simulacion
    def reset(self) -> None:
        pass

    def iniciar(self, cant_routers:int, mu_router: int, sigma_router: int, mu_paquete: int, sigma_paquete: int, tiempo: int,\
                    porcentaje_caida_router:int) -> None:
        # Set-up <-- Cantidad de routers para arrancar simulacion, mu sigma de paquete y router, tiempo simulacion, % caida routers
        self.timeManager.set_tiempo_simulacion(tiempo*10)
        print("SET_TIEMPO_SIMULACION HECHO")
        self.routerManager.fabricaRouter.set_timer(mu_router*10,sigma_router*10)
        print("SET_FABRICA_ROUTER_TIMER HECHO")
        self.routerManager.fabricaRouter.set_routers(cant_routers)
        print("SET_FABRICA_ROUTER_ROUTERS HECHO")
        self.paqueteManager.fabricaPaquete.set_timer(mu_paquete*10,sigma_paquete*10)
        print("SET_FABRICA_PAQUETE_TIMER HECHO")
        self.routerManager.set_prob_caida(porcentaje_caida_router)
        print("SET_PROB_CAIDA HECHO")
        self.timeManager.set_tiempo_inicio() # Esta tiene que ser el ultima set up
        print("SET_TIEMPO_INICIO HECHO")
        # Agarra el tiempo
        print("COMIENZA_SIMULACION")
        while self.timeManager.get_tiempo_simulacion() >= 0:
            self.timeManager.next_tick()
        
        print("SIMULACION TERMINADA")
        # Recoleccion / Visualizacion de Informacion
        self.systemLogs.exportLogs()
        self.routerManager.exportLogs()

instance = RoutingSim()


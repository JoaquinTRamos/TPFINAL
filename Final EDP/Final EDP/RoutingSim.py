from TimeManager import TimeManager
from PaqueteManager import PaqueteManager
from RouterManager import RouterManager

# Esta clase representa la simulacion entera, y ante cualquier consulta sobre los managers debera pasar por la instancia "instance".
class RoutingSim():
    def __init__(self) -> None:
        self.timeManager = TimeManager()
        self.paqueteManager = PaqueteManager()
        self.routerManager = RouterManager()

        self.suscribir_acciones()
        pass

    def suscribir_acciones(self) -> None: # Aca se establece el orden para el evento de on_tick
        self.timeManager.subscribir_accion(self.paqueteManager.contarTicksFabricaPaquete)

    # Metodo para reiniciar la simulacion
    def reset(self) -> None:
        pass

    def iniciar(self) -> None:
        while self.timeManager.get_tiempo_simulacion() >= 0:
            self.timeManager.next_tick()

instance = RoutingSim()
instance.timeManager.set_tiempo_simulacion(100) # Cantidad de ticks en la simulacion

instance.iniciar() # Comienza la simulacion <- Temporal para probar implementacion de tiempo
from events import Events
from typing import Callable
from datetime import *

# Esta clase representa una instancia de tiempo denominado tick, donde 1 tick = 100ms o 1/10 seg
class Tick(Events):
    __events__ = ("on_tick")

    def __init__(self) -> None:
        super().__init__()
        self.tiempoPorTick = 1
        pass

    def __str__(self) -> str:
        return f"Tiempo por tick: {self.tiempoPorTick}"

# Esta clase se encargara de la simulacion del tiempo.
class TimeManager():
    def __init__(self) -> None:
        self._tick: Tick = Tick()
        self._tiempo_simulacion: int = 0
        self._tiempo_total: int = 0
        pass

    def subscribir_accion(self, accion: Callable[[int],None]) -> None: # Cambiar typing de accion si necesitamos Input/Output distintos
        self._tick.on_tick += accion

    def set_tiempo_simulacion(self, cantidad_ticks: int) -> None:
        self._tiempo_simulacion = cantidad_ticks
        self._tiempo_total = cantidad_ticks

    def get_tiempo_simulacion(self) -> int:
        return self._tiempo_simulacion

    def get_current_tick(self) -> int:
        return self._tiempo_total - self._tiempo_simulacion

    def next_tick(self) -> None:
        print(f"Next tick was called, time left in ticks:{self._tiempo_simulacion}")
        self._tiempo_simulacion -= self._tick.tiempoPorTick
        self._tick.on_tick(self._tick.tiempoPorTick) # Si quiero que haya algun input para el evento entonces debemos pasar aca eso

    def get_tiempoPaquete(self, tiempoinicio = datetime.now()) -> datetime:
        tiempoPaquete = tiempoinicio + timedelta(milliseconds = (self.get_current_tick * 100))
        return tiempoPaquete.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
     

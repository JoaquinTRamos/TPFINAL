from Cola import ColaTransmitir, Cola
from enum import Enum
from Paquete import Paquete
from typing import Callable
from random import randint

class RouterEstado(Enum):
    AGREGADO = 0
    ACTIVO = 1
    INACTIVO = 2
    EN_RESET = 3
    FALTA_CHECK = 4


class Router():
    def __init__(self, coordenada):
            self.coordenada:int = coordenada
            self.estado:RouterEstado = RouterEstado.FALTA_CHECK
            self.cola_propios:Cola = Cola()
            self.cola_transmitir: Cola = Cola()
            self.logsMensajes:dict = {}
            self._timer: int = 0
            self.propiosProcesados: int = 0
            self.transmicionProcesados : int = 0

            # Se vuelve a llamar a set_estado para automaticamente pasar a estado activo 
            # El estado agregado es algo momentaneo cuando se crea el router y pasa en el mismo momento a activo
            

    def get_coordenada(self):
        return self.coordenada
    def get_estado(self):
        return self.estado
    def get_cola_propios(self):
        return self.cola_propios
    def get_cola_retransmitir(self):
        return self.cola_retransmitir

    def set_estado(self, estado: RouterEstado) -> None:
        self.estado = estado
        from RoutingSim import instance
        instance.systemLogs.addLog(estado, self, instance.timeManager.get_timestamp())

    def requestPaquete(self) -> None:
        # Solicitar un paquete con origen propio para enviar a otro router -> Es un NUEVO paquete
        from RoutingSim import instance
        self.enqueuePaquete(instance.paqueteManager.fabricaPaquete.fabricarPaquete(self.coordenada))
        pass

    def enqueuePaquete(self, paquete: Paquete) -> None:
    # Encolar un paquete -> Si el paquete es propio se encola en la cola de propios y se guarda el log.
    #                       Si es para retransmitir se encola en la cola de retransmitir y se guarda el log
    #                       Si es un mensaje para el router se guarda el log

        if paquete.metadata.origen == self.coordenada:
            self.cola_propios.encolar(paquete)
        elif paquete.metadata.destino != self.coordenada:
            # al ser un mensaje recibido, tiene que guardar el log
            self.cola_transmitir.encolar(paquete)

        self.addLogPaquete(paquete)
    
    def dequeuePaquete(self) -> (Paquete|None):
    # Desencola el proximo paquete a enviar -> Si la cola de retransmitir esta vacia se desencola de la cola de propios
        if len(self.cola_transmitir) == 0:
            try:
                paquete = self.cola_propios.desencolar()
                self.propiosProcesados += 1
                return paquete
            except Exception:
                return None
        else:
            try:
                paquete = self.cola_transmitir.desencolar()
                self.transmicionProcesados += 1
                return paquete
            except Exception:
                return None

    def desactivarRouter(self, callback: Callable[["Router"],None]) -> None:

        # Uso la funcion SET_ESTADO para tener un metodo unificado de cambiar los estados de los routers
        # Esto facilita el guardado de logs

        self.set_estado(RouterEstado.INACTIVO)
        self._timer = randint(50,100)
        callback(self)


    # FUNCIONES PARA MANTENER LOS LOGS DE MENSAJES RECIBIDOS
    def addLogPaquete(self, paquete: Paquete) -> None:
        # Almacenar el historial de paquetes recibidos -> Se almacena solo los datos relevantes para armar el archivo de logs
        self.logsMensajes[paquete.id] = [paquete.mensaje, paquete.metadata.origen, paquete.metadata.destino]
    
    def exportLogs(self):
        # Exportar los logs de mensajes recibidos a un archivo de 

        with open("Final EDP/Final EDP/Logs/routerLogs/ROUTER_{}.txt".format(self.coordenada), "w") as f:
            for values in self.logsMensajes.values():
                f.write("ROUTER_" + str(values[1]) + "  -   " + str(values[2]) + "  -   "+ str(values[0]) + "\n")

    def __str__(self):
        return "Coordenada: " + str(self.coordenada) + "\nEstado: " + str(self.estado) + "\nCola Propios: " + str(self.cola_propios) + "\nCola Retransmitir: " + str(self.cola_retransmitir) + "\n"


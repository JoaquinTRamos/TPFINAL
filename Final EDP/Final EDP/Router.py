from Cola import ColaTransmitir, Cola
from enum import Enum
from Paquete import Paquete

class RouterEstado(Enum):
    AGREGADO = 0
    ACTIVO = 1
    INACTIVO = 2
    EN_RESET = 3


class Router():
    def __init__(self, coordenada):
            self.coordenada:int = coordenada
            self.estado:RouterEstado = RouterEstado.AGREGADO
            self.cola_propios:Cola = Cola()
            self.cola_transmitir: ColaTransmitir = ColaTransmitir()
            self.logsMensajes:dict = {}

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


    def requestPaquete(self) -> None:
        # Solicitar un paquete con origen propio para enviar a otro router -> Es un NUEVO paquete
        from RoutingSim import instance
        self.cola_propios.encolar(instance.paqueteManager.fabricaPaquete.fabricarPaquete())
        pass
    def enqueuePaquete(self, Paquete: Paquete) -> None:
    # Encolar un paquete -> Si el paquete es propio se encola en la cola de propios.
    #                       Si es para retransmitir se encola en la cola de retransmitir y se guarda el log
    #                       Si es un mensaje para el router se guarda el log

        if Paquete.metadata.origen == self.coordenada:
            self.cola_propios.encolar(Paquete)
        elif Paquete.metadata.destino == self.coordenada:
            # El paquete llego a destino -> Solo guardo el log
            self.addLogPaquete(Paquete)
        else:
            # al ser un mensaje recibido, tiene que guardar el log
            self.addLogPaquete(Paquete)
            self.cola_transmitir.encolar(Paquete)
    def dequeuePaquete(self) -> Paquete:
    # Desencola el proximo paquete a enviar -> Si la cola de retransmitir esta vacia se desencola de la cola de propios
        if len(self.cola_transmitir) == 0:
            return self.cola_propios.desencolar()
        else:
            return self.cola_transmitir.desencolar()


    # FUNCIONES PARA MANTENER LOS LOGS DE MENSAJES RECIBIDOS
    def addLogPaquete(self, Paquete: Paquete) -> None:
        # Almacenar el historial de paquetes recibidos -> Se almacena solo los datos relevantes para armar el archivo de logs
        self.logsMensajes[Paquete.metadata.id] = [Paquete.mensaje, Paquete.metadata.origen]
    def exportLogs(self):
        # Exportar los logs de mensajes recibidos a un archivo de 
        with open("ROUTER_{}.txt".format(self.coordenada), "w") as f:
            for values in self.logsMensajes.values():
                f.write(str(values.origen) + "-" + str(values.mensaje) + "\n")



    def __str__(self):
        return "Coordenada: " + str(self.coordenada) + "\nEstado: " + str(self.estado) + "\nCola Propios: " + str(self.cola_propios) + "\nCola Retransmitir: " + str(self.cola_retransmitir) + "\n"


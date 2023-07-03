from Cola import ColaTransmitir, Cola
from enum import Enum

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
            self.cola_transmitir = ColaTransmitir()

    def get_coordenada(self):
        return self.coordenada
    def get_estado(self):
        return self.estado
    def get_cola_propios(self):
        return self.cola_propios
    def get_cola_retransmitir(self):
        return self.cola_retransmitir

    def set_estado(self, estado) -> None:
        self.estado = estado


    def __str__(self):
        return "Coordenada: " + str(self.coordenada) + "\nEstado: " + str(self.estado) + "\nCola Propios: " + str(self.cola_propios) + "\nCola Retransmitir: " + str(self.cola_retransmitir) + "\n"
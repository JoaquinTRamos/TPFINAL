# crear la clase paquete con los siguientes atributos: Timestamp, metadata (objeto de la clase metadata), y el mensaje
from Metadata import Metadata


class Paquete():
    def __init__(self, timestamp, metadata:Metadata, mensaje:str):
        self.timestamp = timestamp
        self.metadata:Metadata = metadata
        self.mensaje:str = mensaje

    def __str__(self):
        return f"Paquete: {self.timestamp}, {self.metadata}, {self.mensaje}"

    
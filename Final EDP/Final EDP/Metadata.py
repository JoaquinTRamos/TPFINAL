# Contiene toda la informacion de un paquete
class Metadata():

    def __init__(self, timestamp: int, origen:int, destino: int) -> None:
        self.timestamp = timestamp
        self.origen = origen
        self.destino = destino
        
    
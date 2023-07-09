# Contiene toda la informacion de un paquete
class Metadata():

    def __init__(self, origen:int, destino: int) -> None:
        from RoutingSim import instance
        self.timestamp = instance.timeManager.get_tiempoPaquete()
        self.origen = origen
        self.destino = destino
        

        

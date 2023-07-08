# Contiene toda la informacion de un paquete
class Metadata():

    def __init__(self, timestamp: int, origen:int, destino: int) -> None:
        self.timestamp = timestamp
        self.origen = origen
        self.destino = destino
        
    # Definir una funcion que devuelva el tiempo en el que se creo el paquete teniendo en cuenta los Ticks para asignarselo a timestamp
    def tiempoPaquete(self) -> int:
        pass
        
    
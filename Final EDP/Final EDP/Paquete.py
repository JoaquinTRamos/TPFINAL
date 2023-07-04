# crear la clase paquete con los siguientes atributos: Timestamp, metadata (objeto de la clase metadata), y el mensaje
from Metadata import Metadata
from lorem_text import lorem
from random import randint


class Paquete():
    def __init__(self, id: int, metadata: (Metadata|None)):
        self.id = id
        self.metadata:Metadata = metadata
        self.mensaje:str = lorem.words(randint(1,25))

    def __str__(self):
        return f"Paquete {self.id}:, {self.metadata}, {self.mensaje}"


# TESTING - TESTING - TESTING
if __name__ == "__main__":
    
    for i in range(3):
        print(Paquete(i,None))
    
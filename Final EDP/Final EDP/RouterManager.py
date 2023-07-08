# implement a linked list
from Router import Router
from random import randint

from FabricaPaquete import *
from FabricaRouter import *


class DuplicateRouterException(Exception):
    def __init__(self, coord: int, message:str ="Ya existe un router en la coordenada: "):
        super().__init__(message + str(coord))
class NonExistingRouterException(Exception):
    def __init__(self, coord: int, message:str ="No existe un router en la coordenada: "):
        super().__init__(message + str(coord))


class Node():
    def __init__(self, router:Router):
        self.Router:Router = router
        self.next = None
        self.prev = None

class RouterManager():
    def __init__(self) -> None:
        self.head = None
        self.routersCoordenates = set()
        self.fabricaRouter = FabricaRouters()
        self.fabricaPaquete = FabricaPaquetes()

    def addRouter(self, nuevoRouter:Router) -> None:
        print("Agregando router: " + str(nuevoRouter.coordenada) + " a la lista de routers")
        newNode = Node(nuevoRouter)
        if nuevoRouter.coordenada in self.routersCoordenates:
            print("Ya existe un router en la coordenada: " + str(nuevoRouter.coordenada))
            raise DuplicateRouterException(nuevoRouter.coordenada)
        else:
            self.routersCoordenates.add(newNode.Router.coordenada)
            print("Cantidad de routers: " + str(len(self.routersCoordenates)))

        if self.head is None:
            self.head = newNode
        else:
            current = self.head
            while current.next is not None and current.Router.coordenada < nuevoRouter.coordenada:
                current = current.next
            if current.Router.coordenada < nuevoRouter.coordenada:
                current.next = newNode
                current.next.prev = current
            else:
                current.prev.next = newNode
                current.prev.next.next = current
                current.prev.next.prev = current.prev
                current.prev = newNode
    def removeRouter(self, bajaRouter:Router) -> None:
        if bajaRouter.coordenada not in self.routersCoordenates:
            raise NonExistingRouterException(bajaRouter.coordenada)
        else:
            self.routersCoordenates.remove(bajaRouter.coordenada)

            current = self.head
            while current.Router.coordenada != bajaRouter.coordenada:
                current = current.next

            if current.prev is None:
                self.head = current.next
                self.head.prev = None
            elif current.next is None:
                current.prev.next = None
            else:
                current.prev.next = current.next
                current.next.prev = current.prev

    def contarTicksFabricaRouter(self, tiempoPorTick:int) -> None:
        self.fabricaRouter.contarTicks(tiempoPorTick)
    def requestPaquete(self) -> None:       
        self.getRandomAvailableRouter.requestPaquete()
    
    def getRandomAvailableRouter(self) -> Router:
        # funcion que devuelve un router al azar de entre los existentes
        
        #cantidad de routers existentes
        cantidadRouters = len(self.routersCoordenates)

        #numero random entre 1 y la cantidad de routers
        x = randint(1,cantidadRouters)

        current = self.head
        for i in range(0,x):
            current = current.next

        return current.Router
        

#TESTING -- TESTING -- TESTING
if __name__ == "__main__":

    def imprimirLista():
        #recorrer la linked list e imprimir los resultados
        current = lista.head
        while current != None: 
            print(current.Router.coordenada)
            current = current.next
        print("-----")

    lista = RouterManager()
    prueba = [1,4,5,3,2,23,42,21,22]

    for i in prueba:
        lista.addRouter(Router(i))

    imprimirLista()

    lista.removeRouter(lista.head.Router)
    lista.removeRouter(Router(42))

    imprimirLista()


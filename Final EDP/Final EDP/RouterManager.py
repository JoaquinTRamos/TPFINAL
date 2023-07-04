# implement a linked list
from Router import Router

class Node():
    def __init__(self, router:Router):
        self.Router:Router = router
        self.next = None
        self.prev = None

class LinkedList():
    def __init__(self):
        self.head = None
        self.routersCoordenates = set()

    def addRouter(self, nuevoRouter:Router):
        newNode = Node(nuevoRouter)
        if nuevoRouter.coordenada in self.routersCoordenates:
            raise DuplicateRouterException(nuevoRouter.coordenada)
        else:
            self.routersCoordenates.add(newNode.Router.coordenada)

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


class DuplicateRouterException(Exception):
    def __init__(self, coord: int, message:str ="Ya existe un router en la coordenada: "):
        super().__init__(message + str(coord))

#TESTING -- TESTING -- TESTING
if __name__ == "__main__":
    lista = LinkedList()
    prueba = [1,4,5,3,2,23,42,21,22]

    for i in prueba:
        lista.addRouter(Router(i))
    #recorrer la linked list e imprimir los resultados
    current = lista.head
    while current != None: 
        print(current.Router.coordenada)
        current = current.next


# implement a linked list
from re import I
from Router import Router
from random import randint
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
        self.routersInactivos = dict()
        self.fabricaRouter = FabricaRouters()
        self.prob_caida = 10

    def contarTicksFabricaRouter(self, tiempoPorTick:int) -> None:
        self.fabricaRouter.contarTicks(tiempoPorTick)
    
    #Check si el router existe
    def checkRouterExists(self,coordenates)->bool:
        if coordenates in self.routersCoordenates:
            return True
        
        for key in self.routersInactivos.keys():
            if coordenates == key.coordenada:
                return True
        return False


    # agregar y sacar routers
    def addRouter(self, nuevoRouter:Router) -> None:
        newNode = Node(nuevoRouter)
        #if nuevoRouter.coordenada in self.routersCoordenates or nuevoRouter.coordenada in self.routersInactivosCoordenates:
        if self.checkRouterExists(nuevoRouter.coordenada) == True:
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
                newNode.prev = current
            else:
                if current.prev is not None:
                    current.prev.next = newNode
                    newNode.next = current
                    newNode.prev = current.prev
                    current.prev = newNode
                else:
                    current.prev = newNode
                    newNode.next = current
                    self.head = newNode               
    def removeRouter(self, bajaRouter:Router) -> None:
        if bajaRouter.coordenada not in self.routersCoordenates:
            raise NonExistingRouterException(bajaRouter.coordenada)
        else:
            self.routersCoordenates.remove(bajaRouter.coordenada)
            #self.routersInactivosCoordenates.add(bajaRouter.coordenada)

            current = self.head
            while current.Router.coordenada != bajaRouter.coordenada:
                current = current.next

            if current.prev is None:
                if current.next is None:
                    #lista vacia
                    self.head = None
                else:
                    #saco el primero
                    self.head = current.next
                    self.head.prev = None
            elif current.next is None:                
                #saco el ultimo
                current.prev.next = None
            else:
                current.prev.next = current.next
                current.next.prev = current.prev

    # simulacion de pedidos de paquetes
    def requestPaquete(self) -> None:
        if(len(self.routersCoordenates) > 1):
            self.getRandomAvailableRouter().requestPaquete()

    # simulacion de caidas
    def checkearCaidaTick(self, tiempoPorTick:int) -> None:
        if(randint(1,self.prob_caida) < 2):
            # Hace una tirada, si se cumple, pide un router al azar y lo desactiva
            # Para desactivarlo, lo saca de la lista de routers activos y lo agrega a la lista de routers inactivos
            # El router inactivo tiene un timer que se decrementa cada tick, cuando llega a 0, se rehabilita

            router = self.getRandomAvailableRouter()
            if router is not None:
                router.desactivarRouter(self.removeRouter)
                self.routersInactivos[router] = router._timer
                
    def set_prob_caida(self, prob_caida:int) -> None:
        self.prob_caida = prob_caida

    def rehabilitacionRoutersTick(self, tiempoPorTick:int) -> None:
        # Por cada tick que pasa, decrementa el timer de cada router inactivo
        # Si el timer llega a 0, rehabilita el router y lo agrega a la lista de routers activos

        if(len(self.routersInactivos) == 0):
            return None
        listaPop = []
        for router,timer in self.routersInactivos.items():
            self.routersInactivos[router] -=1
            if router.estado == RouterEstado.INACTIVO:
                router.set_estado(RouterEstado.EN_RESET)
            if timer == 0:
                listaPop.append(router)

        for router in listaPop:
            self.routersInactivos.pop(router)
            self.addRouter(router)
            router.set_estado(RouterEstado.ACTIVO)

    # obtener router al azar
    def getRandomAvailableRouter(self) -> Router:
        # funcion que devuelve un router al azar de entre los existentes
        
        #cantidad de routers existentes
        cantidadRouters = len(self.routersCoordenates)

        #numero random entre 1 y la cantidad de routers
        
        if cantidadRouters == 0:
            return None
        elif cantidadRouters == 1:
            return self.head.Router
        else:    
            x = randint(1,cantidadRouters)

        current = self.head
        for i in range(x-1):
            if(current.next == None):
                break
            current = current.next
            

        return current.Router

    # envio de mensajes
    def enviarMensajesTick(self, tiempoPorTick:int)-> None:
        #Funcion que debe ser ejecutada una vez por tick
        # recorre todos los routers y envia el proximo mensaje de la cola de cada uno

        current = self.head
        while current != None:
            # Le pido al current router el proximo paquete a enviar

            paquete = current.Router.dequeuePaquete()

            # Si el paquete es None, significa que no hay paquetes en la cola de ese router
            if paquete != None:

                try:
                    # Si el paquete tiene como destino una coordenada mayor lo paso al next router (Router de la derecha)
                    if paquete.metadata.destino > current.Router.coordenada:
                        current.next.Router.enqueuePaquete(paquete)
                        current = current.next
                        continue
                    # Si el paquete tiene como destino una coordenada menor lo paso al prev router (Router de la izquierda)
                    elif paquete.metadata.destino < current.Router.coordenada:
                        current.prev.Router.enqueuePaquete(paquete)
                except AttributeError:
                    # es el error que sigifica que next o prev son None
                    # solo puede ocurrir si un router esta tratando de enviar un mensaje a otro router 
                    # siendo el router al que se le quiere enviar el mensaje el destino del paquete
                    # y ademas el router destino esta desactivado
                    current.Router.reEnqueuePaquete(paquete)
            
            # Continuo el ciclo
            current = current.next
    
    def exportAllRouterLogs(self) -> None:
        current = self.head
        while current != None:
            current.Router.exportLogs()
            current = current.next

        for key in self.routersInactivos.keys():
            key.exportLogs()

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

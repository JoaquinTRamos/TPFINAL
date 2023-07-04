from RouterManager import * 

lista = LinkedList()
prueba = [1,1,4,5,3,2,23,42,21,22]

for i in prueba:
    try:
        lista.addRouter(Router(i))
    except duplicateRouterException as e:
        print(e)
        continue
    #recorrer la linked list e imprimir los resultados
current = lista.head
while current != None:
    print(current.Router.coordenada)
    current = current.next
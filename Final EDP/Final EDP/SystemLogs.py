from Router import Router, RouterEstado
import csv
from datetime import *

class Log():
    def __init__(self, estado:RouterEstado, router:Router, tick: datetime):
        self.estado = estado
        self.router = router
        self.tick = tick

class SystemLogs():
    def __init__(self):
        self.logs: list[Log] = []

    def addLog(self, estado:RouterEstado, router:Router, tick:datetime):
        self.logs.append(Log(estado,router,tick))

    def exportLogs(self):
        #crear un archivo csv con todos los logs de la simulacion
        # el nombre del archivo debe ser SystemLogs.csv
        # el archivo debe tener 3 columnas: estado, router, tick

        with open('Final EDP/Final EDP/Logs/system_log.csv', 'w', newline='') as csvfile:
            fieldnames = ['Router', 'Timestamp', 'Estado']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for log in self.logs:
                router = 'ROUTER_{}'.format(log.router.coordenada)

                # TO DO --> Cambiar el tick por el tiempo transcurrido desde el inicio de la simulacion
                #           Hay que tomar el timestamp cuando arranco la simulacion y sumar los ticks


                writer.writerow({'Router':router, 'Timestamp': str(log.tick), 'Estado': str(log.estado.name)})


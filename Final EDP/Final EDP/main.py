from RoutingSim import instance
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

class App():
    def __init__(self) -> None:
        self.cant_routers = 0
        self.mu_router = 0
        self.sigma_router = 0
        self.mu_paquete = 0 
        self.sigma_paquete = 0
        self.tiempo = 0
        self.porcentaje_caida_router = 0

        self.resultadoDict = 0
        pass


    def start(self) -> None:
        print("-------\nBienvenido a RoutingSim!\n-------\n")
        print("Comenzar Simulacion? Y/N")
        if input("-> ").capitalize() == "Y":
            os.system("cls")
            self.setUpSim()
            
        else:
            pass
    
    def setUpSim(self) -> None:
        print("Ingresar cantidad de routers al inicio de la simulacion:")
        response = input("-> ")

        while response.isnumeric() == False:
            print("Error: Porfavor ingrese un numero entero")
            response = input("-> ")

        self.cant_routers = int(response)
        os.system("cls")

        print("Si ingresa en las proximas dos variables 0, no se generaran nuevos routers durante la simulacion")
        print("Ingresar tiempo, en segundos, promedio entre generacion de cada router:")
        response = input("-> ")

        while response.isnumeric() == False:
            print("Error: Porfavor ingrese un numero entero")
            response = input("-> ")

        self.mu_router = int(response)
        os.system("cls")

        print("Ingresar tiempo, en segundos, de desvio de la media entre generacion de cada router:")
        response = input("-> ")

        while response.isnumeric() == False:
            print("Error: Porfavor ingrese un numero entero")
            response = input("-> ")

        self.sigma_router = int(response)
        os.system("cls")

        print("Si ingresa en las proximas dos variables 0, se generaran nuevos paquetes cada 100ms durante la simulacion")
        print("Ingresar tiempo, en segundos, promedio entre generacion de cada paquete:")
        response = input("-> ")

        while response.isnumeric() == False:
            print("Error: Porfavor ingrese un numero entero")
            response = input("-> ")

        self.mu_paquete = int(response)
        os.system("cls")

        print("Ingresar tiempo, en segundos, de desvio de la media entre generacion de cada paquete:")
        response = input("-> ")

        while response.isnumeric() == False:
            print("Error: Porfavor ingrese un numero entero")
            response = input("-> ")

        self.sigma_paquete = int(response)
        os.system("cls")

        print("Ingresar tiempo, en segundos, de la simulacion:")
        response = input("-> ")

        while (response.isnumeric() == False or int(response) <= 0):
            print("\nError: Porfavor ingrese un numero mayor a 0")
            response = input("-> ")

        self.tiempo = int(response)
        os.system("cls")

        print("Ingresar el denominador del porcentaje de que se caiga un router cada 100ms:")
        response = input("Formato: 1/x -> ")

        while (response.isnumeric() == False or int(response) <= 0):
            print("\nError: Porfavor ingrese un numero mayor a 0")
            response = input("Formato: 1/x -> ")

        self.porcentaje_caida_router = int(response)
        os.system("cls")

        self.checkRespuestas()

    def checkRespuestas(self) -> None:
        print("Usted ingreso: ")
        print(f"Cantidad de routers: {self.cant_routers}")
        print(f"Mu (Promedio) de tiempo entre generacion de router: {self.mu_router} segundos")
        print(f"Sigma (Desvio) de tiempo entre generacion de router: {self.sigma_router} segundos")
        print(f"Mu (Promedio) de tiempo entre generacion de paquete: {self.mu_paquete} segundos")
        print(f"Sigma (Desvio) de tiempo entre generacion de paquete: {self.sigma_paquete} segundos")
        print(f"Tiempo de simulacion total: {self.tiempo} segundos")
        print(f"Porcentaje de caida de router: {(1/self.porcentaje_caida_router)*100}% - 1/{self.porcentaje_caida_router}")
        print("\nEsto es correcto? Y/N")

        response = input("-> ").capitalize()

        while response != "Y" or response != "N":
            if  response == "Y":
                os.system("cls")
                try:
                    self.resultadoDict = instance.iniciar(cant_routers=self.cant_routers, mu_router=self.mu_router, sigma_router=self.sigma_router, mu_paquete= self.mu_paquete,\
                                sigma_paquete=self.sigma_paquete, tiempo=self.tiempo, porcentaje_caida_router= self.porcentaje_caida_router)
                except Exception:
                    print("Error: No se pudo iniciar la simulacion. Porfavor intente de nuevo.")
                    sys.exit()

                print("Para encontrar los resultados de la simulacion, dirigase a la carpeta Logs.")
                
                self.resultadoDict = np.sort(self.resultadoDict, order="routerCoord")
                
                self.visualizarTasas()
                self.visualizarGrafico()
                sys.exit()
            
            elif response == "N":
                os.system("cls")
                self.setUpSim()
    
    def visualizarGrafico(self) -> None:

        coordenadas = tuple([str(i) for i in list(self.resultadoDict["routerCoord"])])
        totalReenviados = list(self.resultadoDict["transmiciones"])
        totalRecibidoFinal = list(self.resultadoDict["recibidos"])
        totalEnviados = list(self.resultadoDict["propios"])

        data = pd.DataFrame({
            "Enviados": totalEnviados,
            "Recibidos": totalRecibidoFinal,
            "Transmitidos": totalReenviados
        }, index= coordenadas)

        plt.bar(data.index, data.Enviados + data.Recibidos + data.Transmitidos, label="Enviados")
        plt.bar(data.index, data.Recibidos + data.Transmitidos, label="Recibidos")
        plt.bar(data.index, data.Transmitidos, label="Transmitidos")

        plt.xticks(rotation = -45)

        plt.legend(loc="best")
        
        plt.show()
    
    def visualizarTasas(self) -> None:

        totalReenviados = self.resultadoDict["transmiciones"].sum()
        totalRecibidoFinal = self.resultadoDict["recibidos"].sum()
        
        for i in range(len(self.resultadoDict)):
            print(f"ROUTER_{self.resultadoDict[i][0]} = Reenviados: {self.resultadoDict[i][1]}, {round(self.resultadoDict[i][1]/totalReenviados*100,2)}%; Recepcion Final: {self.resultadoDict[i][2]}, {round(self.resultadoDict[i][2]/totalRecibidoFinal*100,2)}%")


app = App()

app.start()

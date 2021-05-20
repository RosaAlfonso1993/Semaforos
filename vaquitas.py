import os
import random
import time
import threading

inicioPuente = 10
largoPuente = 20
semaforoVaquita = threading.Semaphore(1)
cantVacas = 5

class Vaca(threading.Thread):
    def __init__(self):
        super().__init__()
        self.posicion = 0
        self.velocidad = random.uniform(0.1, 0.9)

    def avanzar(self):
        time.sleep(1-self.velocidad)
        self.posicion += 1

    def dibujar(self):
        print(' ' * self.posicion + '🐮') # si no funciona, cambiá por 'V'

    def run(self):
        while(True):
            #semaforoVaquita.acquire()
            #try:
            #    self.avanzar()
            #finally:
            #    semaforoVaquita.release()
            self.avanzar()
            while self.posicion == inicioPuente:
                semaforoVaquita.acquire()
                self.avanzar()
            while self.posicion == (largoPuente + 10):
                semaforoVaquita.release()
                self.avanzar()
            if self.posicion == 50:
                self.posicion = 0

vacas = []
for i in range(cantVacas):
    v = Vaca()
    vacas.append(v)
    v.start() # si la clase hereda de Thread, el .start() siempre corre run() de la clase.

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def dibujarPuente():
    print(' ' * inicioPuente + '=' * largoPuente)

while(True):
    cls()
    print('Apretá Ctrl + C varias veces para salir...')
    print()
    dibujarPuente()
    for v in vacas:
        v.dibujar()
    dibujarPuente()
    time.sleep(0.2)
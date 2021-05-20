import threading
import time
import logging
import random

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

class Cocinero(threading.Thread):
    def __init__(self, num):
        super().__init__()
        self.name = f'Cocinero {num}'

    def run(self):
        global platosDisponibles
        while (True):
            semaforoCocinero.acquire()
            try:
                logging.info('Reponiendo los platos...')
                platosDisponibles = 3 
            finally:
                semaforoPlato.release()
                time.sleep(random.randint(1,3))

class Comensal(threading.Thread):
    def __init__(self, numero):
        super().__init__()
        self.name = f'Comensal {numero}'

    def run(self):
        comensales.acquire()
        try:
            global platosDisponibles
            semaforoPlato.acquire()
            try:
                while platosDisponibles == 0:
                    semaforoCocinero.release()
                    semaforoPlato.acquire()
                platosDisponibles -= 1
                logging.info(f'¡Qué rico! Quedan {platosDisponibles} platos')
            finally:
                semaforoPlato.release()
        finally:
            comensales.release()

platosDisponibles = 3

comensales = threading.Semaphore(2)

semaforoCocinero = threading.Semaphore(0)
semaforoPlato = threading.Semaphore(1)

for i in range(2):
    Cocinero(i).start()
    

for i in range(38):
    Comensal(i).start()

from multiprocessing.managers import BaseManager
from multiprocessing import Queue
import sys


#  herite base manager
#  ouvrie un server sur le port avec mot de passe 
#  fourni des accesseur aux task queue et result queue 

class QueueManager(BaseManager):
    pass

class QueueClient():
    def __init__(self, host, port, authkey):
        self.host = host
        self.port = port
        self.authkey = authkey
        
    def start_server(self, task_queue, result_queue):
        QueueManager.register('get_task_queue', callable=lambda: task_queue)
        QueueManager.register('get_result_queue', callable=lambda: result_queue)

        manager = QueueManager(address=(self.host, self.port), authkey=self.authkey)
        server = manager.get_server()
        print(f"Server started on {self.host}:{self.port}")
        server.serve_forever()

    def connect_to_server(self):
        QueueManager.register('get_task_queue')
        QueueManager.register('get_result_queue')

        manager = QueueManager(address=(self.host, self.port), authkey=self.authkey)
        manager.connect()
        self.task_queue = manager.get_task_queue()
        self.result_queue = manager.get_result_queue()
        print(f"Connected to server on {self.host}:{self.port}")



#  Queue Client 

#  travail se connecter aux serveurs partage port et mdp avec Queue MAneger
# lance serveur ouvre port et on attend

if __name__ == "__main__":
    

    HOST = '127.0.0.1'
    PORT = 5000
    AUTHKEY = b'secret'

    task_queue = Queue()
    result_queue = Queue()
    server = QueueClient(HOST, PORT, AUTHKEY)
    print("[info] Starting server...")
    server.start_server(task_queue, result_queue)

    
    
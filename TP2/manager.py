
from multiprocessing.managers import BaseManager
from multiprocessing import Queue

class QueueManager(BaseManager):
    pass

class QueueClient():
    def __init__(self, host, port, authkey):
        self.host = host
        self.port = port
        self.authkey = authkey

        BaseManager.register("task_queue")
        QueueManager.register("result_queue")

        self.manager = QueueManager(address=(self.host, self.port), authkey=self.authkey)
        print(f"[info] Server started on {self.host}:{self.port}")

        self.manager.connect()
        print(f"[info] Connected to server on {self.host}:{self.port}")
        
        self.task_queue = self.manager.task_queue()
        self.result_queue = self.manager.result_queue()
        
if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 5000
    AUTHKEY = b'passkey'

    print(f"[info] Starting manager")

    task_queue = Queue()
    result_queue = Queue()

    manager = QueueManager(address=(HOST, PORT), authkey=AUTHKEY)

    QueueManager.register("task_queue", callable=lambda: task_queue)
    QueueManager.register("result_queue", callable=lambda: result_queue)

    server = manager.get_server()
    server.serve_forever()

    
    
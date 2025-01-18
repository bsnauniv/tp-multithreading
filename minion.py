from manager import QueueClient


class Minion(QueueClient):
    def __init__(self, host, port, authkey):
        super().__init__(host, port, authkey)

    def execute(self):
        print("Minion: Waiting for tasks...")
        while True:
            task = self.task_queue.get()
            if task is None:
                break
            print(f"Minion: Working on {task}")
            task.work()
            print(f"Minion: Completed {task}")
            self.result_queue.put(task)


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 5000
    AUTHKEY = b"passkey"

    client = Minion(HOST, PORT, AUTHKEY)
    client.execute()

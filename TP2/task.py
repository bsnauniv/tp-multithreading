import time
import numpy as np
import json

class Task:
    def __init__(self, identifier=0, size=None):
        self.identifier = identifier
        # choosee the size of the problem
        self.size = size or np.random.randint(300, 3_000)
        # Generate the input of the problem
        self.a = np.random.rand(self.size, self.size)
        self.b = np.random.rand(self.size)
        # prepare room for the results
        self.x = np.zeros((self.size))
        self.time = 0

    def work(self):
        start = time.perf_counter()
        self.x = np.linalg.solve(self.a, self.b)
        self.time = time.perf_counter() - start

    def __str__(self):
        return f"Task{self.identifier}"
    
    def to_json(self) -> str:
        data = {
            "identifier": self.identifier,
            "size": self.size,
            "a": self.a.tolist(),
            "b": self.b.tolist(),
            "x": self.x.tolist(),
            "time": self.time,
        }
        return json.dumps(data)

    
    @staticmethod
    def from_json(text: str) -> "Task":
        data = json.loads(text)
        task = Task(data["identifier"], data["size"])
        task.a = np.array(data["a"])
        task.b = np.array(data["b"])
        task.x = np.array(data["x"])
        task.time = data["time"]
        return task 

    def __eq__(self, other: "Task") -> bool:
        if not isinstance(other, Task):
            return False
        return (
            self.identifier == other.identifier
            and self.size == other.size
            and np.array_equal(self.a, other.a)
            and np.array_equal(self.b, other.b)
            and np.array_equal(self.x, other.x)
            and self.time == other.time
        )

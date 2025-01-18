import unittest
import numpy as np
from task import Task


class TestStringMethods(unittest.TestCase):
    def test_work(self):
        t = Task()

        t.work()

        np.testing.assert_allclose(np.dot(t.a, t.x), t.b, rtol=1e-5, atol=1e-8)

    def test_eq(self):
        task1 = Task(identifier=1, size=500)
        txt = task1.to_json()
        task2 = Task.from_json(txt)

        self.assertTrue(task1 == task2)


if __name__ == "__main__":
    unittest.main()

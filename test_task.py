import unittest
import numpy as np
from task import Task


class TestStringMethods(unittest.TestCase):
    def test_work(self):
        t = Task()

        t.work()

        np.testing.assert_allclose(np.dot(t.a, t.x), t.b, rtol=1e-5, atol=1e-8)


if __name__ == "__main__":
    unittest.main()

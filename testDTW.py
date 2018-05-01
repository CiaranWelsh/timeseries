import unittest
from dtw import DTW
import numpy, pandas
from StringIO import StringIO




class TestDTW(unittest.TestCase):
    def setUp(self):
        self.x = numpy.array([1, 1, 2, 3, 2, 0])
        self.y = numpy.array([0, 1, 1, 2, 3, 2, 1])


    def test_calculate(self):
        matrix = DTW(self.x, self.y).calculate_cost()
        acc_cost = [[1.,   1.,   1.,   2.,   6.,   7.,   7.],
                    [2.,   1.,   1.,   2.,   6.,   7.,   7.],
                    [6.,   2.,   2.,   1.,   2.,   2.,   3.],
                    [15.,   6.,   6.,   2.,   1.,   2.,   6.],
                    [19.,   7.,   7.,   2.,   2.,   1.,   2.],
                    [19.,   8.,   8.,   6.,  11.,   5.,   2.]]
        acc_cost = numpy.matrix(acc_cost)
        self.assertEqual(matrix.all(), acc_cost.all())

    def test_find_best_path(self):
        path, cost = DTW(self.x, self.y).find_best_path()
        path_answer = [[5, 6], [4, 5], [3, 4], [2, 3], [1, 2], [1, 1], [0, 1], [0, 0]]
        cost_ans = 2.0
        self.assertListEqual(path_answer, path)
        self.assertEqual(cost_ans, cost)








if __name__ == '__main__':
    unittest.main()


















import unittest
import os, glob, pandas, numpy
import sqlite3
from matplotlib.figure import Figure
import site
site.addsitedir(r'..')
from clust_old import *
from scipy.stats import ttest_ind
from sklearn.cluster import AgglomerativeClustering


## folder to the microarray clustering
dire = r'/home/b3053674/Documents/pytseries/Microarray'

class TestHClust(unittest.TestCase):
    def setUp(self):
        self.data_file = os.path.join(dire, 'MicroarrayDEGAgeravedData.xlsx')
        self.db_file = os.path.join(dire, 'microarray_dwt.db')

        self.data = pandas.read_excel(self.data_file, index_col=[0, 1]).transpose()
        self.data = self.data['TGFb'] / self.data['Control']

    def test_cluster(self):
        tsg = TimeSeriesGroup(self.data.iloc[:20])
        c = HClustWithSklearn(tsg, n_clusters=5)
        clusts = c.clusters
        figs = []
        for i in clusts:
            ci = clusts[i]
            figs.append(ci.plot_centroid(label=i))
        [self.assertTrue(isinstance(i, Figure)) for i in figs]


    # def test_initialize(self):
    #     tsg = TimeSeriesGroup(self.data.iloc[:20])
    #     c = HClustWithSklearn(tsg)
    #     self.assertEqual(len(c.monitor), 20)
    #

    # def test_kscan_obj1(self):
    #     tsg = TimeSeriesGroup(self.data.iloc[:20])
    #     c = HClustWithSklearn(tsg, kscan=True, ks=range(3, 6))
    #     obj1 = c.get_obj1()
    #     self.assertTrue(isinstance(float(obj1.loc[3]), float))

    # def test_kscan_obj2(self):
    #     tsg = TimeSeriesGroup(self.data.iloc[:20])
    #     c = HClustWithSklearn(tsg, kscan=True, ks=range(3, 6))
    #     obj2 = c.get_obj2()
    #     self.assertTrue(isinstance(float(obj2.loc[3]), float))




if __name__ == '__main__':
    unittest.main()



































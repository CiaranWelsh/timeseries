import unittest
import os, glob, pandas, numpy
import sqlite3
from matplotlib.figure import Figure
import site
site.addsitedir(r'..')
from clust import *
from scipy.stats import ttest_ind
from sklearn.cluster import AgglomerativeClustering


## folder to the microarray clustering
dire = r'/home/b3053674/Documents/timeseries/Microarray'

class TestHClust(unittest.TestCase):
    def setUp(self):
        self.data_file = os.path.join(dire, 'MicroarrayDEGAgeravedData.xlsx')
        self.db_file = os.path.join(dire, 'microarray_dwt.db')

        self.data = pandas.read_excel(self.data_file, index_col=[0, 1]).transpose()
        self.data = self.data['TGFb'] / self.data['Control']

    def tearDown(self):
        if os.path.isfile(self.db_file):
            os.remove(self.db_file)

    def test_distance_matrix(self):
        tsg = TimeSeriesGroup(self.data.iloc[:50])
        c = HClustDTW(tsg)
        self.assertTrue(isinstance(c.dist_matrix(c.clusters), pandas.DataFrame))

    def test_initial_cluster(self):
        tsg = TimeSeriesGroup(self.data.iloc[:50])
        c = HClustDTW(tsg)
        self.assertTrue(isinstance(c.clusters, dict))

    def test_get_pair_to_merge(self):
        tsg = TimeSeriesGroup(self.data.iloc[:6])
        c = HClustDTW(tsg)
        dist = c.dist_matrix(c.clusters)
        self.assertEqual(c.get_pair_to_merge(dist), (0, 1))

    def test_fit(self):
        tsg = TimeSeriesGroup(self.data.iloc[:6])
        c = HClustDTW(tsg)
        clusters, merge_pairs = c.fit()
        # print(clusters, merge_pairs)

    def test_full(self):
        tsg = TimeSeriesGroup(self.data.iloc[:6])
        tsg.norm(inplace=True)
        c = HClustDTW(tsg, db_file=self.db_file)
        c.fit()
        print(self.db_file)
        self.assertTrue(os.path.isfile(self.db_file))

    def test_db(self):
        tsg = TimeSeriesGroup(self.data.iloc[:4])
        tsg.norm(inplace=True)
        c = HClustDTW(tsg, db_file=self.db_file)
        c.fit()
        with DB(self.db_file) as db:
            table3 = db.read_table('"3"')

        self.assertEqual(table3['cluster'].unique()[0], 0)

    def test_full_run(self):
        fname = os.path.join(dire, 'full_dataset.db')
        # if os.path.isfile(fname):
        #     os.remove(fname)
        #
        # tsg = TimeSeriesGroup(self.data)
        # tsg.norm(inplace=True)
        # c = HClustDTW(tsg, db_file=fname)
        # c.fit()

        table_id = 215
        with DB(fname) as db:
            print(db.tables())
            table = db.read_table(table_id)

        for label, df in table.groupby('cluster'):
            df = df[df['cluster'] == label]
            df = df.drop('cluster', axis=1)
            tsg = TimeSeriesGroup(df)
            if len(tsg) < 20:
                fig = tsg.plot(tsg.features, legend=True)
            else:
                fig = tsg.plot(tsg.features, legend=False)

            d = os.path.join(dire, str(table_id))
            if not os.path.isdir(d):
                os.makedirs(d)
            fname = os.path.join(d, str(label) + '.png')
            print (fname )
            fig.savefig(fname, dpi=300, bbox_inches='tight')

        # plt.show()

        # self.assertEqual(table3['cluster'].unique()[0], 0)



if '__main__' == __name__:
    unittest.main()


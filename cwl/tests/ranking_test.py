import unittest
import sys
import numpy as np
sys.path.insert(0,'./')

from cwl.ruler.ranking import Ranking
from cwl.ruler.ranking import RankingMaker
from cwl.seeker.trec_qrel_handler import TrecQrelHandler

class TestRanking(unittest.TestCase):

    def setUp(self):
        self.ranking1 = Ranking("T1", [1., 0., 0.5, 1., 0.0], [1., 1., 1., 1., 1.])
        self.ranking2 = Ranking("T2", [1., np.nan, 0.5, 1., np.nan], [1., 1., 1., 1., 1.])
        self.ranking3 = Ranking("T3",
                                [1., np.nan, 0.5, 1., np.nan, 0.0, 0.0, 0.0, 0.0, 0.0],
                                [1., 1., 1., 1., 1., 2., 2., 2., 2., 2.],
                                max_gain=2.0, max_cost=5.0)

        self.ranking4 = Ranking("T4",
                                [1., np.nan, 0.5, 1., np.nan, 0.0, 0.0, 0.0, 0.0, 0.0],
                                [],
                                max_gain=2.0, max_cost=3.0, min_cost=2.0)

        self.ranking5 = Ranking("T5",
                                [1., 0., 1., 1., 1., 0.0, 0.0, 0.0, 0.0, 0.0],
                                [])

    def test_ranking1_total_rels(self):
        """
        Test whether the tail is filled with min gain (worse case), and max gain (best case)
        Assumes that MAX_N = 1000
        """
        min_total = self.ranking1.get_total_rels()
        max_total = self.ranking1.get_total_rels(worse_case=False)

        self.assertEqual(min_total, 3.0)
        self.assertEqual(max_total, 998.0)


    def test_ranking1_total_gain(self):
        """
        Test whether the tail is filled with min gain (worse case), and max gain (best case)
        """
        min_total = self.ranking1.get_total_gain()
        max_total = self.ranking1.get_total_gain(worse_case=False)
        # print(self.ranking1.get_gain_vector(worse_case=False))
        # print(max_total)
        self.assertEqual(min_total, 2.5)
        self.assertEqual(max_total, 997.5)

    def test_ranking2_total_rels(self):
        """
        Test whether the tail is filled with min gain (worse case), and max gain (best case)
        and that the np.nans are converted to min and max gain.
        """
        min_total = self.ranking2.get_total_rels()
        max_total = self.ranking2.get_total_rels(worse_case=False)
        # print(self.ranking1.get_gain_vector(worse_case=False))
        # print(max_total)
        self.assertEqual(min_total, 3.0)
        self.assertEqual(max_total, 1000.0)

    def test_ranking2_total_gain(self):
        """
        Test whether the tail is filled with min gain (worse case), and max gain (best case)
        and that the np.nans are converted to min and max gain.
        """
        min_total = self.ranking2.get_total_gain()
        max_total = self.ranking2.get_total_gain(worse_case=False)
        # print(self.ranking1.get_gain_vector(worse_case=False))
        # print(max_total)
        self.assertEqual(min_total, 2.5)
        self.assertEqual(max_total, 999.5)

    def test_ranking3_total_rels(self):
        """
        Test whether the tail is filled with min gain (worse case), and max gain (best case)
        and that the np.nans are converted to min and max gain.
        """
        min_total = self.ranking3.get_total_rels()
        max_total = self.ranking3.get_total_rels(worse_case=False)
        # print(self.ranking1.get_gain_vector(worse_case=False))
        # print(max_total)
        self.assertEqual(min_total, 3.0)
        self.assertEqual(max_total, 995.0)

    def test_ranking3_total_gain(self):
        """
        Test whether the tail is filled with min gain (worse case), and max gain (best case)
        and that the np.nans are converted to min and max gain.
        """
        min_total = self.ranking3.get_total_gain()
        max_total = self.ranking3.get_total_gain(worse_case=False)
        # print(self.ranking1.get_gain_vector(worse_case=False))
        # print(max_total)
        self.assertEqual(min_total, 2.5)
        self.assertEqual(max_total, 1986.5)


    def test_ranking3_total_cost(self):
        """
        Test whether the tail is filled with max_cost (worse case)
        and min cost (best case)
        """
        max_total = np.sum(self.ranking3.get_cost_vector())
        min_total = np.sum(self.ranking3.get_cost_vector(worse_case=False))
        self.assertEqual(max_total, 4965.0)
        self.assertEqual(min_total, 1005.0)

    def test_ranking4_total_cost_when_no_cost_vector_is_supplied(self):
        """
        Test whether the tail is filled with max_cost (worse case)
        and min cost (best case)
        Note this is the reverse
        """
        max_total = self.ranking4.get_total_cost()
        min_total = self.ranking4.get_total_cost(worse_case=False)
        self.assertEqual(max_total, 3000.0)
        self.assertEqual(min_total, 2000.0)

    def test_ranking5_sum_over_top_ranks(self):
        min_gains = self.ranking5.get_gain_vector()
        max_gains = self.ranking5.get_gain_vector(worse_case=False)
        # print(min_gains[0:5])
        self.assertEqual(np.sum(min_gains[0:5]), 4)
        self.assertEqual(np.sum(max_gains[0:5]), 4)

class TestRankingMaker(unittest.TestCase):

    def setUp(self):
        gh = TrecQrelHandler("qrel_file")
        gh.put_value("T1", "D1", 1.0)
        gh.put_value("T1", "D2", 0.0)
        gh.put_value("T1", "D3", 1.0)
        gh.put_value("T1", "D4", 0.0)
        gh.put_value("T1", "D5", 1.0)
        gh.put_value("T1", "D6", 0.0)
        gh.put_value("T1", "D7", 1.0)
        gh.put_value("T1", "D8", 0.0)
        gh.put_value("T1", "D9", 0.0)
        gh.put_value("T1", "D10", 1.0)

        self.rm = RankingMaker(topic_id="T1", gain_handler=gh, cost_dict=None)
        docs = ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10"]
        for d in docs:
            self.rm.add(d, "")

    def test_ranking(self):
        ranking = self.rm.get_ranking()
        #print(ranking.)
        min_gains = ranking.get_gain_vector()
        max_gains = ranking.get_gain_vector(worse_case=False)
        #print(min_gains[0:20])
        # print(np.cumsum(gains)[0:20])
        # print(gains[0:10])
        self.assertEqual(np.sum(min_gains[0:20]), 5.0)
        self.assertEqual(np.sum(max_gains[0:20]), 15.0)


if __name__ == '__main__':
    unittest.main()
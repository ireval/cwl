import unittest
import sys
#sys.path.insert(0, '../')

from cwl.ruler.measures.cwl_precision import PrecisionCWLMetric
from cwl.ruler.ranking import Ranking


class TestPrecision(unittest.TestCase):

    def setUp(self):
        self.p1 = PrecisionCWLMetric(k=1)
        self.p5 = PrecisionCWLMetric(k=5)

    def test_patone_ranking1(self):
        """
        Test that Precision at one is correct for each ranking.
        """

        ranking1 = Ranking("T1", [1], [1])
        self.p1.measure(ranking1)
        self.assertEqual(self.p1.expected_utility, 1.0)
        self.assertEqual(self.p1.expected_total_utility, 1.0)


    def test_patone_ranking2(self):
        """
        Test that Precision at one is correct for each ranking.
        """
        ranking2 = Ranking("T2", [1, 0], [1, 1])
        self.p1.measure(ranking2)
        self.assertEqual(self.p1.expected_utility, 1.0)
        self.assertEqual(self.p1.expected_total_utility, 1.0)


    def test_patone_ranking3(self):
        """
        Test that Precision at one is correct for each ranking.
        """
        ranking3 = Ranking("T3", [0, 1], [1, 1])
        self.p1.measure(ranking3)
        self.assertEqual(self.p1.expected_utility, 0.0)
        self.assertEqual(self.p1.expected_total_utility, 0.0)



    def test_padding(self):
        """
        Test that Precision at one is correct for each ranking.
        """
        ranking3 = Ranking("T3", [0, 1], [1, 1])
        self.p5.measure(ranking3)
        self.assertEqual(self.p5.expected_utility, 0.2)
        self.assertEqual(self.p5.expected_total_utility, 1.0)






if __name__ == '__main__':
    unittest.main()
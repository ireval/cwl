import numpy as np
from cwl.ruler.measures.cwl_metrics import CWLMetric

"""
Rank Biased Precision by Moffat and Zobel

theta denotes the patience of a user - higher thetas means that they are more likely to continue down the ranked list

A very simple user model where theta is the continuation probability.

RBP is directly related to Net Present Value ( see cwl_npv.NPCWLmetric)
and RBP is also related to Time Biased Gain (see cwl_tbg.TBGCWLMetric)

"""


class RBPCWLMetric(CWLMetric):

    def __init__(self, theta=0.9):
        #CWLMetric.__init__(self)
        super().__init__()
        self.metric_name = "RBP@{0}".format(theta)
        self.theta = theta
        self.bibtex = """
        @article{Moffat:2008:RPM:1416950.1416952,
        author = {Moffat, Alistair and Zobel, Justin},
        title = {Rank-biased Precision for Measurement of Retrieval Effectiveness},
        journal = {ACM Trans. Inf. Syst.},
        volume = {27},
        number = {1},
        year = {2008},
        pages = {2:1--2:27},
        articleno = {2},
        numpages = {27},
        url = {http://doi.acm.org/10.1145/1416950.1416952},
        } 
        """

    def name(self):
        return "RBP@{0}".format(self.theta)

    def c_vector(self, ranking, worse_case=True):
        cvec = np.dot(np.ones(ranking.n), self.theta)
        return cvec

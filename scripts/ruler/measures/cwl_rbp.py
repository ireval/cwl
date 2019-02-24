import numpy as np
from ruler.measures.cwl_metrics import CWLMetric


'''
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
'''

class RBPCWLMetric(CWLMetric):

    def __init__(self, theta=0.9):
        super(CWLMetric, self).__init__()
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

    def c_vector(self, ranking):
        cvec = np.dot(np.ones(len(ranking.gains)), self.theta)
        return cvec

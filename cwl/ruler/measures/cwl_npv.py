import numpy as np
from cwl.ruler.measures.cwl_metrics import CWLMetric

"""
An economic metric derived directly from computing the Net Present Value of a given list.
r is the rate by how much the user discounts the future interaction

Note that NPV is equivalent to RBP where theta = 1/(1+rate).

This means that patience (theta) can be expressed 
as a how much searchers discount the future value for an alternative perspective.

"""


class NPVCWLMetric(CWLMetric):

    def __init__(self, rate=0.1):
        super().__init__()
        self.metric_name = "NPV-r@{0}".format(rate)
        self.rate = rate
        self.bibtex = """
        @inproceedings{azzopardi2019cwl,
        author = {Azzopardi, Leif and Thomas, Paul and Moffat, Alistair}
        title = {cwl\_eval: An Evaluation Tool for Information Retrieval},
        booktitle = {Proc. of the 42nd International ACM SIGIR Conference},
        series = {SIGIR '19},
        year = {2019} 
        }
        """

    def name(self):
        return "NPV-r@{0}".format(self.rate)

    def c_vector(self, ranking, worse_case=True):
        gains = ranking.get_gain_vector(worse_case)
        cvec = np.dot(np.ones(len(gains)), (1.0/(1.0+self.rate)))
        return cvec

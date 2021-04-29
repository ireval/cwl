import numpy as np
from cwl.ruler.measures.cwl_metrics import CWLMetric

"""
TODO
"""

class GRRINSQCWLMetric(CWLMetric):

    def __init__(self, k, T=1.0):
        #CWLMetric.__init__(self)
        super().__init__()
        self.metric_name = "GRRINSQ-T={0}@{1}".format(T, k)
        self.T = T
        self.k = k
        self.bibtex = """
        TODO
        """

    def c_vector(self, ranking, worse_case=True):
        gains = ranking.get_gain_vector(worse_case)
        cvec = np.zeros(len(gains))
        i = 0
        while i < len(gains) and i < self.k - 1: #XXX: To get the same results as the spreadsheet, I have to use k-1 here...
          rank = i + 1
          cvec[i] = (((rank + (2.0 * self.T)-1.0) / (rank + (2.0 * self.T)))**2.0) * (1.0-gains[i])
          i = i + 1
        return np.array(cvec)


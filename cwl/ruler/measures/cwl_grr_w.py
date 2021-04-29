import numpy as np
from cwl.ruler.measures.cwl_metrics import CWLMetric

"""
TODO
"""

class GRRWCWLMetric(CWLMetric):

    def __init__(self, k):
        #CWLMetric.__init__(self)
        super().__init__()
        self.metric_name = "GRRW@{0}".format(k)
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
          cvec[i] = (1.0*rank/(rank+1.0)) * (1.0-gains[i])
          i = i + 1
        return np.array(cvec)
 

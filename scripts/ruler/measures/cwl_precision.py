import numpy as np
from ruler.measures.cwl_metrics import CWLMetric

'''
(Graded) Precision at k, where k is assumed to be the number of items to be examined.

if the gains are set to (0 or 1) then binary precision is calculated,
if the gains are set to 0..1.0 then graded precision is calculated

Note that CG@k / R@k and P@k are essentially related.
where the EU/Doc is P@k, while the EU/Serp (ETU) is CG@k or R@k

#TODO(leifos): Reference for Precision Measures...


'''


class PrecisionCWLMetric(CWLMetric):

    def __init__(self, k=10):
        super(CWLMetric, self).__init__()
        self.metric_name = "P@{0}".format(k)
        self.k = k
        self.bibtex = ""

    def name(self):
        return "P@{0}".format(self.k)

    def c_vector(self, ranking):
        cvec = np.ones(self.k-1)
        cvec = self.pad_vector_zeros(cvec, len(ranking.gains))
        return cvec

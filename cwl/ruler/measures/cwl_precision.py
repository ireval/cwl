import numpy as np
from cwl.ruler.measures.cwl_metrics import CWLMetric

'''
(Graded) Precision at k, where k is assumed to be the number of items to be examined.

if the gains are set to (0 or 1) then binary precision is calculated,
if the gains are set to 0..1.0 then graded precision is calculated

Note that CG@k / R@k and P@k are essentially related.
where the EU/Doc is P@k, while the EU/Serp (ETU) is CG@k or R@k

Van Rijsbergen (and Salton) both mention calculating precision at k - though in the context of computing the PR curve.
P@k was used much later more widely in the 1990s through TREC.
'''


class PrecisionCWLMetric(CWLMetric):

    def __init__(self, k=10):
        super().__init__()
        self.metric_name = "P@{0}".format(k)
        self.k = k
        self.bibtex = """
        @misc{rijsbergen:1979:ir,
        title={Information Retrieval.},
        author={Van Rijsbergen, Cornelis J},
        year={1979},
        publisher={USA: Butterworth-Heinemann}
        }
        """

    def name(self):
        return "P@{0}".format(self.k)

    def c_vector(self, ranking, worse_case=True):
        cvec = np.ones(self.k-1)
        cvec = self._pad_vector(cvec, ranking.n, 0.0)
        return cvec

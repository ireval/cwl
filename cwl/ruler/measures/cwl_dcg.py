import numpy as np
import math
from cwl.ruler.measures.cwl_metrics import CWLMetric


"""
Discounted Cumulative Gain by Jarvelin and Kekalainen (2002)
The discount is scaled so that forms a proper probability distribution

k is the rank cut off i.e number of items to be examined
base is the base of the log for the discounting, which is set to 2 by default as per the original paper.
"""

class NDCGCWLMetric(CWLMetric):
    def __init__(self, k):
        super().__init__()
        self.metric_name = "NDCG-k@{0}".format(k)
        self.k = k
        self.base = 2.0
        self.bibtex = """
        @article{Jarvelin:2002:CGE:582415.582418,
        author = {J\"{a}rvelin, Kalervo and Kek\"{a}l\"{a}inen, Jaana},
        title = {Cumulated Gain-based Evaluation of IR Techniques},
        journal = {ACM Trans. Inf. Syst.},
        volume = {20},
        number = {4},
        year = {2002},
        pages = {422--446},
        numpages = {25},
        url = {http://doi.acm.org/10.1145/582415.582418},
        }
        """

    def name(self):
        return "NDCG-k@{0}".format(self.k)

    def c_vector(self, ranking, worse_case=True):

        cvec = []
        for i in range(1, ranking.n+1):
            if i < self.k:
                cvec.append(math.log(i+1, self.base)/math.log(i+2, self.base))
            else:
                cvec.append(0.0)

        cvec = np.array(cvec)

        return cvec

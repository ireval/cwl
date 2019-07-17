import numpy as np
import math
from cwl.ruler.measures.cwl_metrics import CWLMetric

"""
Search Economic Metric based on Azzopardi (2014)'s economic model of search.

Given the total gain function g(i) = i^beta
where i is the rank of the item, and beta controls the amount of discount. 
There is no explicit reference to a relevance vector in the paper as it makes 
an assumption about how much, on average, a user would get by going to the next rank.
So essentially, there is an implicit assumption that each item provides one unit of gain.
But here the implementation will use the same discounting scheme - but the observed relevance/gain vector.

Note that for each k, the expected total utility (ETU from CWL) @k = g(k) when all items are relevant.

0 <= beta <= 1.0 - and is the amount of diminishing returns that the user experiences
k = 1...n up to 1000 - is the cut-off which the user will stop.

note that when beta = 1.0 and k = k, then user model is equivalent to the P@k user model.

"""


class SETCWLMetric(CWLMetric):

    def __init__(self, beta=0.5, k=10):
        super().__init__()
        self.k = k
        self.beta = beta
        self.metric_name = self.name()
        self.bibtex = """
        @inproceedings{Azzopardi:2014:MIE:2600428.2609574,
        author = {Azzopardi, Leif},
        title = {Modelling Interaction with Economic Models of Search},
        booktitle = {Proceedings of the 37th International ACM SIGIR Conference 
                on Research \&\#38; Development in Information Retrieval},
        year = {2014},
        location = {Gold Coast, Queensland, Australia},
        pages = {3--12},
        numpages = {10},
        url = {http://doi.acm.org/10.1145/2600428.2609574},
        } 
        """

    def name(self):
        return "SET-k@{0}-b@{1}".format(self.k, self.beta)

    def _weight(self, i):
        return math.pow(i + 1, self.beta) - math.pow(i, self.beta)

    def c_vector(self, ranking, worse_case=True):

        cvec = []
        for i in range(1, ranking.n + 1):
            if i < self.k:
                cvec.append(self._weight(i+1)/self._weight(i))
            else:
                cvec.append(0.0)

        cvec = np.array(cvec)

        return cvec

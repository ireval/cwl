import numpy as np
import math
from cwl.ruler.measures.cwl_metrics import CWLMetric


"""
U-Measure by Saka and Dou (2013)

The metric assumes that as searchers read more and more text they are less likely to continue.

L expresses the half-life associated with reading text. A higher L means the searcher is more likely to continue.

The cost used should be expressed in characters - but as this is porportional to time - time could be used as well.
Note that if costs are in terms of characters - then the EC and ETC will then be in units based on characters (obviously)

"""

class UMeasureCWLMetric(CWLMetric):
    def __init__(self, L=1000):
        super().__init__()
        self.metric_name = "U-L@{0} ".format(L)
        self.L = L
        self.bibtex = """
        @inproceedings{Sakai:2013:SRR:2484028.2484031,
        author = {Sakai, Tetsuya and Dou, Zhicheng},
        title = {Summaries, Ranked Retrieval and Sessions: A Unified Framework for Information Access Evaluation}
        booktitle = {Proceedings of the 36th International ACM SIGIR Conference on Research and Development in Information Retrieval},
        series = {SIGIR '13},
        year = {2013},
        location = {Dublin, Ireland},
        pages = {473--482},
        numpages = {10},
        url = {http://doi.acm.org/10.1145/2484028.2484031}
        } 
        """

    def name(self):
        return "U-L@{0} ".format(self.L)

    def c_vector(self, ranking, worse_case=True):
        wvec = self.w_vector(ranking, worse_case)
        cvec = []
        for i in range(0, len(wvec)-1):
            if wvec[i] > 0.0:
                cvec.append(wvec[i+1] / wvec[i])
            else:
                cvec.append(0.0)

        cvec.append(0.0)
        cvec = np.array(cvec)
        return cvec

    def w_vector(self, ranking, worse_case=True):
        wvec = []
        # to get the positions, cumulative sum the costs..
        # costs are assumed to length of each document
        costs = ranking.get_cost_vector(worse_case)
        c_costs = np.cumsum(costs)
        start = 0
        norm = 0.0
        for i in range(0, len(c_costs)-1):
            weight_i = self.pos_decay(start)
            start = c_costs[i]
            wvec.append(weight_i)
            norm = norm + weight_i
        wvec.append(0.0)

        # now normalize the wvec to sum to one.
        wvec = np.divide(np.array(wvec), norm)
        return wvec


    def pos_decay(self, pos):
        return max(0.0, (1.0 - (pos / self.L)))

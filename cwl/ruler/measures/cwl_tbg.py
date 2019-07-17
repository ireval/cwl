import numpy as np
import math
from cwl.ruler.measures.cwl_metrics import CWLMetric


"""
Time Biased Gain by Smucker and Clarke

H is the halflife which stipulates how quickly the gain decays over time

TBG is equivalent to RBP if the cost of items is equal.

Note in the formulation below the weight is normalized so that a probability vector is formed for W (i.e. it sums to one).
I.e. the weights are re-scaled.

Also note that the costs vectors should pre-compute apriori the cost of each element, 
and if no gain is assigned to duplicate/similar items, then qrel file used should be pre-processed to zero out duplicate 
items see subsequently.

TODO(): Consider implementing duplicate sensitive qrel handler that would be duplicate aware.

"""

class TBGCWLMetric(CWLMetric):
    def __init__(self, halflife=224):
        super().__init__()
        self.metric_name = "TBG-H@{0} ".format(halflife)
        self.halflife = halflife
        self.bibtex = """
        @inproceedings{Smucker:2012:TCE:2348283.2348300,
        author = {Smucker, Mark D. and Clarke, Charles L.A.},
        title = {Time-based Calibration of Effectiveness Measures},
        booktitle = {Proceedings of the 35th International ACM SIGIR Conference
         on Research and Development in Information Retrieval},
        series = {SIGIR '12},
        year = {2012},
        location = {Portland, Oregon, USA},
        pages = {95--104},
        numpages = {10},
        url = {http://doi.acm.org/10.1145/2348283.2348300},
        } 
        """

    def name(self):
        return "TBG-H@{0} ".format(self.halflife)

    def c_vector(self, ranking, worse_case=True):
        wvec = self.w_vector(ranking, worse_case)
        cvec = []
        for i in range(0, len(wvec)-1):
            if wvec[i] > 0.0:
                cvec.append( wvec[i+1]/ wvec[i])
            else:
                cvec.append(0.0)

        cvec.append(0.0)
        cvec = np.array(cvec)

        return cvec

    def w_vector(self, ranking, worse_case=True):
        costs = ranking.get_cost_vector(worse_case)
        wvec = []
        c_costs = np.cumsum(costs)
        start = 0.0

        norm = self.integral_decay(0.0)
        wvec.append(norm)

        for i in range(0, len(c_costs)-1):
            weight_i = self.integral_decay(c_costs[i])
            norm = norm + weight_i
            wvec.append(weight_i)

        wvec = np.divide(np.array(wvec), norm)
        return wvec

    def integral_decay(self, x):
        h = self.halflife
        return (h * (2.0 ** (-x/h))) / math.log(2.0, math.e)

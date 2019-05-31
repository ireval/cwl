import numpy as np
import math
from ruler.measures.cwl_metrics import CWLMetric

'''
(Graded) Average Precision

@inproceedings{Robertson:2010:EAP:1835449.1835550,
 author = {Robertson, Stephen E. and Kanoulas, Evangelos and Yilmaz, Emine},
 title = {Extending Average Precision to Graded Relevance Judgments},
 booktitle = {Proceedings of the 33rd International ACM SIGIR Conference on Research and Development in Information Retrieval},
 series = {SIGIR '10},
 year = {2010},
 location = {Geneva, Switzerland},
 pages = {603--610},
 numpages = {8},
 url = {http://doi.acm.org/10.1145/1835449.1835550}
} 

'''

class APCWLMetric(CWLMetric):
    def __init__(self):
        CWLMetric.__init__(self)
        # super(CWLMetric, self).__init__()
        self.metric_name = "AP"
        self.bibtex = ""

    def name(self):
        return self.metric_name

    def c_vector(self, ranking, worse_case=True):
        gains = ranking.get_gain_vector(worse_case)
        rels = 0
        for g in gains:
            if g > 0.0:
                rels += 1
        rm = int(ranking.get_total_rels(worse_case)) - rels

        n = len(gains)
        rii = []
        cvec = []
        for i in range(0, n):
            rii.append(gains[i]/(i+1))

        for i in range(0, n-1):
            bot = np.sum(rii[i:n])
            top = np.sum(rii[i+1:n])

            if top > 0.0:
                cvec.append(top/bot)
            else:
                cvec.append(0.0)

        cvec.append(0.0)
        cvec = np.array(cvec)
        return cvec


class TrueAPCWLMetric(CWLMetric):
    def __init__(self):
        super(CWLMetric, self).__init__()
        self.metric_name = "TrAP"
        self.bibtex = ""

    def name(self):
        return self.metric_name

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
        c_costs = np.cumsum(ranking.get_cost_vector(worse_case))
        c_gains = np.cumsum(ranking.get_gain_vector(worse_case))

        i = 0
        while (c_gains[i] == 0) and (i < len(c_gains)-1):
            c_gains[i] = 1.0
            i += 1

        total_rels = ranking.get_total_rels(worse_case)
        wvec = np.divide(c_gains, c_costs)
        if total_rels > 0:
            wvec = wvec / total_rels

        return np.array(wvec)

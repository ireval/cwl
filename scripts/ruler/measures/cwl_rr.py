import numpy as np
from ruler.measures.cwl_metrics import CWLMetric

'''
Reciprocal Rank

and 

ERR

@inproceedings{Chapelle:2009:ERR:1645953.1646033,
 author = {Chapelle, Olivier and Metlzer, Donald and Zhang, Ya and Grinspan, Pierre},
 title = {Expected Reciprocal Rank for Graded Relevance},
 booktitle = {Proceedings of the 18th ACM Conference on Information and Knowledge Management},
 series = {CIKM '09},
 year = {2009},
 location = {Hong Kong, China},
 pages = {621--630},
 numpages = {10},
 url = {http://doi.acm.org/10.1145/1645953.1646033}
} 

'''

class RRCWLMetric(CWLMetric):

    def __init__(self):
        super().__init__()
        self.metric_name = "RR"
        self.bibtex = ""

    def name(self):
        return "RR"

    def c_vector(self, ranking, worse_case=True):
        gains = ranking.get_gain_vector(worse_case)
        cvec = np.zeros(len(gains))
        i = 0
        found_gain = False
        while i < len(gains) and not found_gain:
            if (gains[i] > 0):
                found_gain = True
            else:
                cvec[i] = 1.0
            i = i + 1

        return cvec


class ERRCWLMetric(CWLMetric):

    def __init__(self):
        super().__init__()
        self.metric_name = "ERR"
        self.bibtex = """
        @inproceedings{Chapelle:2009:ERR:1645953.1646033,
        author = {Chapelle, Olivier and Metlzer, Donald and Zhang, Ya and Grinspan, Pierre},
        title = {Expected Reciprocal Rank for Graded Relevance},
        booktitle = {Proceedings of the 18th ACM Conference on Information and Knowledge Management},
        series = {CIKM '09},
        year = {2009},
        location = {Hong Kong, China},
        pages = {621--630},
        numpages = {10},
        url = {http://doi.acm.org/10.1145/1645953.1646033}
        } 
        """

    def name(self):
        return "ERR"

    def c_vector(self, ranking, worse_case=True):
        gains = ranking.get_gain_vector(worse_case)
        cvec = np.subtract(np.ones(len(gains)-gains))

        return cvec

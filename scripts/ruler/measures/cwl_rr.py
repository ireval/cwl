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
        super(CWLMetric, self).__init__()
        self.metric_name = "RR"
        self.bibtex = ""

    def name(self):
        return "RR"

    def c_vector(self, ranking):

        cvec = np.zeros(len(ranking.gains))
        i = 0
        found_gain = False
        while i < len(ranking.gains) and not found_gain:

            if (ranking.gains[i] > 0):
                found_gain = True
            else:
                cvec[i] = 1.0
            i = i + 1

        return cvec


class ERRCWLMetric(CWLMetric):

    def __init__(self):
        super(CWLMetric, self).__init__()
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

    def c_vector(self, ranking):
        '''
        :param gains: all gains must be between one and zero
        :param costs: cost vectors can be any real value, i.e. can be greater than one, but is not used for ERR.
        :return: the continuation vector for ERR
        '''

        cvec = np.subtract(np.ones(len(ranking.gains))-ranking.gains)

        return cvec

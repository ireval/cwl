import numpy as np
from cwl.ruler.measures.cwl_metrics import CWLMetric

"""
Reciprocal Rank (RR) - From TREC-5 in 1996 by Kantor and Voorhees
"""


class RRCWLMetric(CWLMetric):

    def __init__(self):
        super().__init__()
        self.metric_name = "RR"
        self.bibtex = """
        @article{kantor2000trec,
        title={The TREC-5 Confusion Track},
        author={Kantor, Paul and Voorhees, Ellen},
        journal={Information Retrieval},
        volume={2},
        number={2-3},
        pages={165--176},
        year={2000}
        }
        """

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


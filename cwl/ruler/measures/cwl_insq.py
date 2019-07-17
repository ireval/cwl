import numpy as np
import math
from cwl.ruler.measures.cwl_metrics import CWLMetric

"""
INSQ by Moffat et al (is a variant on INST)

T denotes the desired amount of gain.
"""


class INSQCWLMetric(CWLMetric):

    def __init__(self, T=1.0):
        super().__init__()
        self.metric_name = "INSQ-T={0}    ".format(T)
        self.T = T
        self.bibtex = """
        @inproceedings{Moffat:2012:MMI:2407085.2407092,
        author = {Moffat, Alistair and Scholer, Falk and Thomas, Paul},
        title = {Models and Metrics: IR Evaluation As a User Process},
        booktitle = {Proceedings of the Seventeenth Australasian Document Computing Symposium},
        series = {ADCS '12},
        year = {2012},
        location = {Dunedin, New Zealand},
        pages = {47--54},
        url = {http://doi.acm.org/10.1145/2407085.2407092},
        } 
        """

    def name(self):
        return "INSQ-T={0}".format(self.T)

    def c_vector(self, ranking, worse_case=True):
        gains = ranking.get_gain_vector(worse_case)
        cg = np.cumsum(gains)
        cvec = []
        for i in range(0, len(cg)):
            ci = (((i+1.0) + (2.0 * self.T)-1.0) / ((i+1.0) + (2.0 * self.T)))**2.0
            cvec.append(ci)

        cvec = np.array(cvec)
        return cvec

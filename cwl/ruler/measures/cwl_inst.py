import numpy as np
import math
from cwl.ruler.measures.cwl_metrics import CWLMetric

"""
INST is from Moffat et al., Australasian Document Computing Symposium 2015

T: Is the desired amount of relevant items or gain, 
depending on whether gain is binary (0,1) or graded (0..1.0)
"""

class INSTCWLMetric(CWLMetric):

    # INST requires gains to be in range [0, 1]
    MINGAIN = 0.0
    MAXGAIN = 1.0

    def __init__(self, T=1.0):
        super().__init__()
        self.metric_name = "INST-T={0}    ".format(T)
        self.T = T
        self.bibtex = """
        @inproceedings{Moffat:2015:IAM:2838931.2838938,
        author = {Moffat, Alistair and Bailey, Peter and Scholer, Falk and Thomas, Paul},
        title = {INST: An Adaptive Metric for Information Retrieval Evaluation},
        booktitle = {Proceedings of the 20th Australasian Document Computing Symposium},
        series = {ADCS '15},
        year = {2015},
        location = {Parramatta, NSW, Australia},
        pages = {5:1--5:4},
        articleno = {5},
        numpages = {4},
        url = {http://doi.acm.org/10.1145/2838931.2838938}
        } 
        """

    def name(self):
        return "INST-T={0}".format(self.T)

    def c_vector(self, ranking, worse_case=True):
        gains = ranking.get_gain_vector(worse_case)
        self.validate_gain_range(self.MINGAIN, self.MAXGAIN, gains)
        c_gains = np.cumsum(gains)
        cvec = []
        for i in range(0, len(c_gains)):
            Ti = self.T - c_gains[i]
            ci = (((i+1.0)+self.T+Ti-1.0) / ((i+1.0)+self.T+Ti))**2.0
            cvec.append(ci)

        cvec = np.array(cvec)
        return cvec

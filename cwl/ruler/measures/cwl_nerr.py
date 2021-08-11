import numpy as np
from cwl.ruler.measures.cwl_metrics import CWLMetric

'''
The suite of Not (but Nearly) ERR metrics (NERR) from the Azzopardi et al. in
ICTIR 2021 ("ERR is not C/W/L...").

There are four specific instances of NERR metrics which correspond to equations
presented in the aforementioned research paper: NERReq{8, 9, 10, 11}.

Note that NERReq8 and NERReq9 are designed to be truncated at k, whereas
NRReq10 runs to full depth according to the parameter phi (akin to RBP) and
NRReq11 runs to full depth according to the parameter T (akin to INST).
'''


# Option One (Equation 8)
class NERReq8CWLMetric(CWLMetric):

    # NERReq8 requires gains to be in range [0, 1]
    MINGAIN = 0.0
    MAXGAIN = 1.0

    def __init__(self, k):
        super().__init__()
        self.metric_name = "NERR-EQ8@k={0}".format(k)
        self.k = k
        self.bibtex = """
        @inproceedings{Azzopardi:2021:ECE:3471158.3472239,
        author = {Azzopardi, Leif and Mackenzie, Joel and Moffat, Alistair},
        title = {{ERR} is not {C/W/L}: Exploring the Relationship Between Expected Reciprocal Rank and Other Metrics},
        booktitle = {Proceedings of the 2021 ACM SIGIR on International Conference on Theory of Information Retrieval},
        series = {ICTIR '21},
        location = {Virtual Event, Canada},
        url = {https://doi.org/10.1145/3471158.3472239},
        doi = {3471158.3472239},
        }
        """

    def c_vector(self, ranking, worse_case=True):
        gains = ranking.get_gain_vector(worse_case)
        self.validate_gain_range(self.MINGAIN, self.MAXGAIN, gains)
        cvec = np.zeros(len(gains))
        i = 0
        while i < len(gains) and i < self.k - 1: 
          cvec[i] = 1 - gains[i]
          i = i + 1
        return np.array(cvec)


# Option Two (Equation 9)
class NERReq9CWLMetric(CWLMetric):

    # NERReq9 requires gains to be in range [0, 1]
    MINGAIN = 0.0
    MAXGAIN = 1.0

    def __init__(self, k):
        super().__init__()
        self.metric_name = "NERR-EQ9@k={0}".format(k)
        self.k = k
        self.bibtex = """
        @inproceedings{Azzopardi:2021:ECE:3471158.3472239,
        author = {Azzopardi, Leif and Mackenzie, Joel and Moffat, Alistair},
        title = {{ERR} is not {C/W/L}: Exploring the Relationship Between Expected Reciprocal Rank and Other Metrics},
        booktitle = {Proceedings of the 2021 ACM SIGIR on International Conference on Theory of Information Retrieval},
        series = {ICTIR '21},
        location = {Virtual Event, Canada},
        url = {https://doi.org/10.1145/3471158.3472239},
        doi = {3471158.3472239},
        }
        """

    def c_vector(self, ranking, worse_case=True):
        gains = ranking.get_gain_vector(worse_case)
        self.validate_gain_range(self.MINGAIN, self.MAXGAIN, gains)
        cvec = np.zeros(len(gains))
        i = 0
        while i < len(gains) and i < self.k - 1: 
          rank = i + 1
          cvec[i] = (1.0*rank/(rank+1.0)) * (1.0-gains[i])
          i = i + 1
        return np.array(cvec)


# Option Three (Equation 10)
class NERReq10CWLMetric(CWLMetric):

    # NERReq10 requires gains to be in range [0, 1]
    MINGAIN = 0.0
    MAXGAIN = 1.0

    def __init__(self, phi=0.9):
        super().__init__()
        self.metric_name = "NERR-EQ10@phi={0}".format(phi)
        self.phi = phi
        self.bibtex = """
        @inproceedings{Azzopardi:2021:ECE:3471158.3472239,
        author = {Azzopardi, Leif and Mackenzie, Joel and Moffat, Alistair},
        title = {{ERR} is not {C/W/L}: Exploring the Relationship Between Expected Reciprocal Rank and Other Metrics},
        booktitle = {Proceedings of the 2021 ACM SIGIR on International Conference on Theory of Information Retrieval},
        series = {ICTIR '21},
        location = {Virtual Event, Canada},
        url = {https://doi.org/10.1145/3471158.3472239},
        doi = {3471158.3472239},
        }
        """

    def c_vector(self, ranking, worse_case=True):
        gains = ranking.get_gain_vector(worse_case)
        self.validate_gain_range(self.MINGAIN, self.MAXGAIN, gains)
        cvec = np.zeros(len(gains))
        i = 0
        while i < len(gains):
          cvec[i] = self.phi * (1 - gains[i])
          i = i + 1
        return np.array(cvec)


# Option Four (Equation 11)
class NERReq11CWLMetric(CWLMetric):

    # NERReq11 requires gains to be in range [0, 1]
    MINGAIN = 0.0
    MAXGAIN = 1.0

    def __init__(self, T=1.0):
        super().__init__()
        self.metric_name = "NERR-EQ11@T={0}".format(T)
        self.T = T
        self.bibtex = """
        @inproceedings{Azzopardi:2021:ECE:3471158.3472239,
        author = {Azzopardi, Leif and Mackenzie, Joel and Moffat, Alistair},
        title = {{ERR} is not {C/W/L}: Exploring the Relationship Between Expected Reciprocal Rank and Other Metrics},
        booktitle = {Proceedings of the 2021 ACM SIGIR on International Conference on Theory of Information Retrieval},
        series = {ICTIR '21},
        location = {Virtual Event, Canada},
        url = {https://doi.org/10.1145/3471158.3472239},
        doi = {3471158.3472239},
        }
        """
 
    def c_vector(self, ranking, worse_case=True):
        gains = ranking.get_gain_vector(worse_case)
        self.validate_gain_range(self.MINGAIN, self.MAXGAIN, gains)
        cvec = np.zeros(len(gains))
        i = 0
        while i < len(gains):
          rank = i + 1
          cvec[i] = (((rank + (2.0 * self.T)-1.0) / (rank + (2.0 * self.T)))**2.0) * (1.0-gains[i])
          i = i + 1
        return np.array(cvec)

import numpy as np
import math
from ruler.measures.cwl_metrics import CWLMetric

'''
Information Foraging Based Measure


@inproceedings{Azzopardi:2018:MUS:3209978.3210027,
 author = {Azzopardi, Leif and Thomas, Paul and Craswell, Nick},
 title = {Measuring the Utility of Search Engine Result Pages: An Information Foraging Based Measure},
 booktitle = {The 41st International ACM SIGIR Conference on Research \&\#38; Development in Information Retrieval},
 series = {SIGIR '18},
 year = {2018},
 location = {Ann Arbor, MI, USA},
 pages = {605--614},
 numpages = {10},
 } 

'''

class IFTGoalCWLMetric(CWLMetric):
    def __init__(self, T, b1, R1):
        super(CWLMetric, self).__init__()
        self.metric_name = "IFT-C1-T={0}-b1={1}-R1={2}".format(T,b1,R1)
        self.b1 = b1
        self.T = T
        self.R1 = R1
        self.bibtex = "@inproceedings{Azzopardi:2018:MUS:3209978.3210027," \
                      "author = {Azzopardi, Leif and Thomas, Paul and Craswell, Nick}," \
                      "title = {Measuring the Utility of Search Engine Result Pages: An Information Foraging Based Measure}," \
                      "booktitle = {The 41st International ACM SIGIR Conference on Research \&\#38; Development in Information Retrieval}," \
                      "series = {SIGIR '18}," \
                      "year = {2018}," \
                      "location = {Ann Arbor, MI, USA}," \
                      "pages = {605--614}," \
                      "numpages = {10}," \
                      "} "

    def name(self):
        return "IFT-C1-T={0}-b1={1}-R1={2}".format(self.T, self.b1, self.R1)

    def c_vector(self, ranking):
        cgains = np.cumsum(ranking.gains)
        cvec = []
        for i in range(0,len(ranking.gains)):
            c1 = self.c1_func(cgains[i])
            cvec.append(c1)

        cvec = np.array(cvec)

        return cvec

    def c1_func(self, yi):
        ex = (1.0 + self.b1 * math.pow(math.e, ((self.T-yi)* self.R1)))
        return 1.0 - math.pow(ex,-1.0)


class IFTRateCWLMetric(CWLMetric):
    def __init__(self, A, b2,  R2):
        super(CWLMetric, self).__init__()
        self.metric_name = "IFT-C2-A={0}-b2={1}-R2={2}".format(A, b2, R2)
        self.b2 = b2
        self.A = A
        self.R2 = R2
        self.bibtex = "@inproceedings{Azzopardi:2018:MUS:3209978.3210027," \
                      "author = {Azzopardi, Leif and Thomas, Paul and Craswell, Nick}," \
                      "title = {Measuring the Utility of Search Engine Result Pages: An Information Foraging Based Measure}," \
                      "booktitle = {The 41st International ACM SIGIR Conference on Research \&\#38; Development in Information Retrieval}," \
                      "series = {SIGIR '18}," \
                      "year = {2018}," \
                      "location = {Ann Arbor, MI, USA}," \
                      "pages = {605--614}," \
                      "numpages = {10}," \
                      "} "

    def name(self):
        return "IFT-C2-A={0}-b2={1}-R2={2}".format(self.A, self.b2, self.R2)

    def c_vector(self, ranking):
        cgains = np.cumsum(ranking.gains)
        ccosts = np.cumsum(ranking.costs)
        cvec = []
        for i in range(0,len(ranking.gains)):
            c2 = self.c2_func(cgains[i],ccosts[i])
            cvec.append(c2)

        cvec = np.array(cvec)

        return cvec

    def c2_func(self, yi,ki):
        ex = (1.0 + self.b2 * math.pow(math.e, ((self.A - (yi/ki))* self.R2)))
        return math.pow(ex,-1.0)


class IFTGoalRateCWLMetric(CWLMetric):
    def __init__(self, T, b1, R1, A, b2,  R2):
        super(CWLMetric, self).__init__()
        self.metric_name = "IFT-C1-C2-T={0}-b1={1}-R1={2}-A={3}-b2={4}-R2={5}".format(T, b1, R1, A, b2, R2)
        self.b1 = b1
        self.T = T
        self.R1 = R1
        self.b2 = b2
        self.A = A
        self.R2 = R2
        self.bibtex = """
        @inproceedings{Azzopardi:2018:MUS:3209978.3210027,
        author = {Azzopardi, Leif and Thomas, Paul and Craswell, Nick},
        title = {Measuring the Utility of Search Engine Result Pages: An Information Foraging Based Measure},
        booktitle = {The 41st International ACM SIGIR Conference on Research \&\#38; Development in Information Retrieval},
        series = {SIGIR '18},
        year = {2018},
        location = {Ann Arbor, MI, USA},
        pages = {605--614},
        numpages = {10},
        } 
        """

    def name(self):
        return "IFT-C1-C2-T={0}-b1={1}-R1={2}-A={3}-b2={4}-R2={5}".format(self.T, self.b1, self.R1, self.A, self.b2, self.R2)

    def c_vector(self, ranking):
        cgains = np.cumsum(ranking.gains)
        ccosts = np.cumsum(ranking.costs)
        cvec = []
        for i in range(0,len(ranking.gains)):

            c1 = self.c1_func(cgains[i])
            c2 = self.c2_func(cgains[i],ccosts[i])
            cvec.append(c1*c2)

        cvec = np.array(cvec)

        return cvec

    def c2_func(self, yi,ki):
        ex = (1.0 + self.b2 * math.pow(math.e, ((self.A - (yi/ki))* self.R2)))
        return math.pow(ex,-1.0)


    def c1_func(self, yi):
        ex = (1.0 + self.b1 * math.pow(math.e, ((self.T-yi)* self.R1)))
        return 1.0 - math.pow(ex,-1.0)

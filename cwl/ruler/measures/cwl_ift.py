import numpy as np
import math
from cwl.ruler.measures.cwl_metrics import CWLMetric

"""
Information Foraging Based Measure by Azzopardi et al (2018)

T is the target gain (i.e. how much is desired)
A is the average rate of gain that expected
b1/b2 are intercept parameters
R1/R2 are 'rationality' parameters, as R1/R2 are increased to infinity then the searcher becomes increasingly rational, 
and will stop if T is met, or A is not met. but as R1/R2 are decreased to zero, the the searcher will become ambivalent
towards T or A respectively, and fall back to the default b1/b2 intercepts. i.e. T or A will not influence the decision
 to continue.
 
 As a result, if R1/R2 are set to zero, then the metric becomes akin to RBP.
 If R1 is set to inf, then once T gain is acquired, the searcher will stop - which is akin or RR (where T would equal 1)
 If R1/R2 are set inbetween, then it suggests that as the user approaches T, they become more likely to stop, as they 
 are getting closer to their goal, and once they reach their goal, they are still likely to continue (but to a lesser 
 and lesser degree).  Similiarly, if the user is experiencing a rate of gain higher than A, then they are much more likely to continue, 
 but as the rate of gain decreases and gets further from A, then user is less likely to continue.

IFTGoalCWLMetric implements the Goal only variant
IFTRateCWLMetric implements the Rate only variant
IFTGoalRateCWLMetric implements the Goal and Rate variant - which was shown to be the most accurate in Azzopardi et al.
"""


class IFTGoalCWLMetric(CWLMetric):
    def __init__(self, T, b1, R1):
        super().__init__()
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

    def c_vector(self, ranking, worse_case=True):
        gains = ranking.get_gain_vector(worse_case)
        c_gains = np.cumsum(gains)
        cvec = []
        for i in range(0, len(gains)):
            c1 = self.c1_func(c_gains[i])
            cvec.append(c1)
        cvec = np.array(cvec)
        return cvec

    def c1_func(self, yi):
        ex = (1.0 + self.b1 * math.pow(math.e, ((self.T-yi) * self.R1)))
        return 1.0 - math.pow(ex, -1.0)


class IFTRateCWLMetric(CWLMetric):
    def __init__(self, A, b2,  R2):
        super().__init__()
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

    def c_vector(self, ranking, worse_case=True):
        gains = ranking.get_gain_vector(worse_case)
        costs = ranking.get_cost_vector(worse_case)

        c_gains = np.cumsum(gains)
        c_costs = np.cumsum(costs)
        cvec = []
        for i in range(0, len(gains)):
            c2 = self.c2_func(c_gains[i], c_costs[i])
            cvec.append(c2)

        cvec = np.array(cvec)

        return cvec

    def c2_func(self, yi, ki):
        ex = (1.0 + self.b2 * math.pow(math.e, ((self.A - (yi/ki)) * self.R2)))
        return math.pow(ex, -1.0)


class IFTGoalRateCWLMetric(CWLMetric):
    def __init__(self, T, b1, R1, A, b2,  R2):
        super().__init__()
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

    def c_vector(self, ranking, worse_case=True):
        gains = ranking.get_gain_vector(worse_case)
        costs = ranking.get_cost_vector(worse_case)
        c_gains = np.cumsum(gains)
        c_costs = np.cumsum(costs)
        cvec = []
        for i in range(0, len(gains)):

            c1 = self.c1_func(c_gains[i])
            c2 = self.c2_func(c_gains[i], c_costs[i])
            cvec.append(c1*c2)

        cvec = np.array(cvec)

        return cvec

    def c2_func(self, yi, ki):
        ex = (1.0 + self.b2 * math.pow(math.e, ((self.A - (yi/ki)) * self.R2)))
        return math.pow(ex, -1.0)

    def c1_func(self, yi):
        ex = (1.0 + self.b1 * math.pow(math.e, ((self.T-yi) * self.R1)))
        return 1.0 - math.pow(ex, -1.0)

import numpy as np
from cwl.ruler.measures.cwl_metrics import CWLMetric

"""
Bejewelled Player Model (BPM) by Zhang et al 2017

Gains are assumed to be scaled to be between: 0.0 - 1.0
thus rel_max is assumed to be 1.0. 

In Zhang et al (2017), rel_max is an integer i.e. 0,1,2,3 (for a 4 levels of grades)
and the rel level is raised to the power of 2. To encode this within the C/W/L BPM, 
the rel levels would need to be re-scaled to be between one and zero. 

Static: takes T (i.e. E_b) and K (i.e. E_c) in Zhang et al (2017)
T is the total amount of gain desired - similar to T in INST and IFT

K is the total amout of cost willing to be spent, similar to k in precision,
however K can be any unit of cost (depending on the costs file),
while k in P@k, is the number of documents.
In Zhang et al (2017), K is k the number of documents, 
but here we provide the generalized verison, 
such that K can be set based on the costs specified for each doc (as per the cost file)


Dynamic: Also takes: hb, hc and gain_med ( i.e. rel_med in Zhang et al (2017)
hb 

gain_med is the median gain (i.e. value between 0 and 1.0)
if gain observed at position i is higher than gain_med,
than T is increased, while K is increased

if gain observed at position i is lower than gain_med,
than T is decreased, while K is decreased

The change in gain is: T <- T + hb * (gain[i] - gain_med)
The change in cost is: K <- K + hc * (gain[i] - gain_med)

hb and hc are therefore scaling parameters.

"""

class BPMCWLMetric(CWLMetric):

    def __init__(self, T=1.0, K=10):
        CWLMetric.__init__(self)
        # super(CWLMetric, self).__init__()
        self.metric_name = "BPM-Static-T={0}-K={1}".format(T, K)
        self.T = T # E_b the total amount of benefit desired
        self.K = K # E_c the total amount of cost or documents willing to be examined
        self.bibtex = """
        @inproceedings{Zhang:2017:EWS:3077136.3080841,
        author = {Zhang, Fan and Liu, Yiqun and Li, Xin and Zhang, Min and Xu, Yinghui and Ma, Shaoping},
        title = {Evaluating Web Search with a Bejeweled Player Model},
        booktitle = {Proceedings of the 40th International ACM SIGIR Conference on Research and Development in Information Retrieval},
        series = {SIGIR '17},
        year = {2017},
        location = {Shinjuku, Tokyo, Japan},
        pages = {425--434},
        url = {http://doi.acm.org/10.1145/3077136.3080841},
        } 
        """

    def name(self):
        return "BPM-Static-T={0}-K={1}".format(self.T,self.K)


    def c_vector(self, ranking, worse_case=True):
        gains = ranking.get_gain_vector(worse_case)
        costs = ranking.get_cost_vector(worse_case)

        c_gain = np.cumsum(gains)
        c_cost = np.cumsum(costs)

        # GAIN Constraint
        rr_cvec = np.zeros(len(gains))
        i = 0
        # continue until the gain accumulated exceeds T
        while i < len(gains) and (c_gain[i] < self.T):
            rr_cvec[i] = 1.0
            i = i + 1

        # COST Constraint
        p_cvec = np.zeros(len(costs))
        i = 0
        # continue until the costs accumulated exceeds K
        while i < len(costs) and (c_cost[i] < self.K):
            p_cvec[i] = 1.0
            i = i + 1

        # combine the two continuation vectors
        bpm_cvec = np.zeros(len(costs))
        i = 0
        while i < len(costs):
            if (rr_cvec[i] == 1.0) and (p_cvec[i] == 1.0):
                bpm_cvec[i] = 1.0
            i = i + 1

        return bpm_cvec




class BPMDCWLMetric(CWLMetric):

    def __init__(self, T=1, K=10, hb=1.0, hc=1.0, gain_med=0.5):
        super().__init__()
        self.metric_name = "BPM-Dynamic-T={0}-K={1}-hb={2}-hc={3}".format(T,K,hb,hc)
        self.T = T # E_b the total amount of benefit desired
        self.K = K # E_c the total amount of cost or documents willing to be examined
        self.hb = hb # the scaling factor to adjust the T constraint by
        self.hc = hc # the scaling factor to adjust the K constraint by
        self.gain_med = gain_med # i.e. rel_med to adjust the T and K by
        self.bibtex = """
        @inproceedings{Zhang:2017:EWS:3077136.3080841,
        author = {Zhang, Fan and Liu, Yiqun and Li, Xin and Zhang, Min and Xu, Yinghui and Ma, Shaoping},
        title = {Evaluating Web Search with a Bejeweled Player Model},
        booktitle = {Proceedings of the 40th International ACM SIGIR Conference on Research and Development in Information Retrieval},
        series = {SIGIR '17},
        year = {2017},
        location = {Shinjuku, Tokyo, Japan},
        pages = {425--434},
        url = {http://doi.acm.org/10.1145/3077136.3080841},
        } 
        """

    def name(self):
        return "BPM-Dynamic-T={0}-K={1}-hb={2}-hc={3}".format(self.T,self.K, self.hb, self.hc)

    def c_vector(self, ranking, worse_case=True):
        gains = ranking.get_gain_vector(worse_case)
        costs = ranking.get_cost_vector(worse_case)
        c_gain = np.cumsum(gains)
        c_cost = np.cumsum(costs)

        # GAIN Constraint
        rr_cvec = np.zeros(len(gains))
        i = 0
        T = self.T
        # continue until the gain accumulated exceeds T
        while i < len(gains) and (c_gain[i] < T):
            rr_cvec[i] = 1.0
            # Now Update T, depending on gain[i]
            T = T + self.hb * (gains[i] - self.gain_med)

            i = i + 1
        # COST Constraint
        p_cvec = np.zeros(len(costs))
        i = 0
        K = self.K
        # continue until the costs accumulated exceeds K
        while i < len(costs) and (c_cost[i] < K):
            p_cvec[i] = 1.0
            # Now Update K, depending on gain[i]
            T = T + self.hc * (gains[i] - self.gain_med)
            i = i + 1

        # combine the two continuation vectors
        bpm_cvec = np.zeros(len(costs))
        i = 0
        while i < len(costs):
            if (rr_cvec[i] == 1.0) and (p_cvec[i] == 1.0):
                bpm_cvec[i] = 1.0
            i = i + 1

        return bpm_cvec

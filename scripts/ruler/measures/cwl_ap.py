import numpy as np
import math
from ruler.measures.cwl_metrics import CWLMetric


'''
(Graded) Average Precision

#todo(leifos): Add Reference to AP and GAP.

#todo(leifos): Still need to convert Paul's verision of AP from R to Python..


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
        super(CWLMetric, self).__init__()
        self.metric_name = "AP"
        self.bibtex = ""


    def name(self):
        return self.metric_name


    def c_vector(self, ranking):
        '''
        Doesn't metric need to know all the relevant items??
        :param gains:
        :param costs:
        :return:
        '''
        rels = 0
        for g in ranking.gains:
            if g > 0.0:
                rels += 1
        rm = int(ranking.total_rels) - rels

        n = len(ranking.gains)
        rii = []
        cvec = []
        for i in range(0,n):
            rii.append(ranking.gains[i]/(i+1))


        for i in range(0,n-1):
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


    def c_vector(self, ranking):

        wvec = self.w_vector(ranking)

        cvec = []
        for i in range(0,len(wvec)-1):
            if(wvec[i]>0.0):
                cvec.append( wvec[i+1]/ wvec[i])
            else:
                cvec.append(0.0)

        cvec.append(0.0)
        cvec = np.array(cvec)

        return cvec


    def w_vector(self, ranking):

        wvec = []
        ccosts = np.cumsum(ranking.costs)
        ggains = np.cumsum(ranking.gains)

        i = 0
        while (ggains[i] == 0) and (i < len(ggains)-1):
            ggains[i] = 1.0
            i += 1

        print(ggains[0:10])

        wvec = np.divide(ggains,ccosts)
        #print(wvec[0:10])
        #print(ranking.total_rels)
        if ranking.total_rels > 0:
            wvec = wvec / ranking.total_rels
        #print(wvec[0:10])

        return np.array(wvec)

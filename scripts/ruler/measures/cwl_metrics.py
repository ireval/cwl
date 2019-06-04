import math
import numpy as np
import logging

logging.basicConfig(filename='cwl.log', level=logging.DEBUG)

MAXN = 1000


class CWLMetric(object):

    def __init__(self):
        self.expected_utility = 0.0
        self.expected_cost = 0.0
        self.expected_total_utility = 0.0
        self.expected_total_cost = 0.0
        self.expected_items = 0.0
        self.residual_expected_utility = None
        self.residual_expected_cost = None
        self.residual_expected_total_utility = None
        self.residual_expected_total_cost = None
        self.residual_expected_items = None
        self.residuals = False
        self.metric_name = "Def"
        self.ranking = None
        self.bibtex = ""

    def name(self):
        return self.metric_name

    def c_vector(self, ranking, worse_case=True):
        cvec = np.ones(len(ranking.get_gain_vector(worse_case)))
        return cvec

    def l_vector(self, ranking, worse_case=True):
        cvec = self.c_vector(ranking, worse_case)
        logging.debug("{0} {1} {2} {3}".format(ranking.topic_id, self.name(), "cvec", cvec[0:11]))
        cshift = np.append(np.array([1.0]), cvec[0:-1])
        lvec = np.cumprod(cshift)
        lvec = np.multiply(lvec, (np.subtract(np.ones(len(cvec)), cvec)))
        logging.debug("{0} {1} {2} {3}".format(ranking.topic_id, self.name(), "lvec", lvec[0:11]))
        return lvec

    def w_vector(self, ranking, worse_case=True):
        cvec = self.c_vector(ranking, worse_case)
        cvec = cvec[0:-1]
        cvec_prod = np.cumprod(cvec)
        cvec_prod = np.pad(cvec_prod, (1, 0), 'constant', constant_values=1.0)
        w1 = np.divide(1.0, np.sum(cvec_prod))
        w_tail = np.multiply(cvec_prod[1:len(cvec_prod)], w1)
        wvec = np.append(w1, w_tail)
        logging.debug("{0} {1} {2} {3}".format(ranking.topic_id, self.name(), "wvec", wvec[0:11]))
        return wvec

    def measure(self, ranking):
        self.ranking = ranking
        # score based on worse case - lower bounds
        (eu, etu, ec, etc, ei) = self._do_score(ranking, True)

        self.expected_utility = eu
        self.expected_total_utility = etu
        self.expected_cost = ec
        self.expected_total_cost = etc
        self.expected_items = ei

        if self.residuals:
            # score based on best case - upper bounds
            (eu, etu, ec, etc, ei) = self._do_score(ranking, False)

            # compute the residual i.e. the difference between the upper and lower bounds
            self.residual_expected_utility = eu - self.expected_utility
            self.residual_expected_total_utility = etu - self.expected_total_utility
            self.residual_expected_cost = ec - self.expected_cost
            self.residual_expected_total_cost = etc - self.expected_total_cost
            self.residual_expected_items = ei - self.expected_items

        # return the rate of gain per document
        return self.expected_utility

    def _do_score(self, ranking, worse_case=True):
        wvec = self.w_vector(ranking, worse_case)
        lvec = self.l_vector(ranking, worse_case)
        gain_vec = ranking.get_gain_vector(worse_case)
        cost_vec = ranking.get_cost_vector(worse_case)
        cum_gains = np.cumsum(gain_vec)
        cum_costs = np.cumsum(cost_vec)
        expected_utility = np.sum(np.dot(wvec, gain_vec))
        expected_total_utility = np.sum(np.dot(lvec, cum_gains))
        expected_cost = np.sum(np.dot(wvec, cost_vec))
        expected_total_cost = np.sum(np.dot(lvec, cum_costs))
        expected_items = 1.0 / wvec[0]
        return expected_utility, expected_total_utility, expected_cost, expected_total_cost, expected_items

    def report(self):
        if self.residuals:
            print("{0}\t{1}\t{2:.4f}\t{3:.4f}\t{4:.4f}\t{5:.4f}\t{6:.4f}\t{7:.4f}\t{8:.4f}\t{9:.4f}\t{10:.4f}\t{11:.4f}".format(
                self.ranking.topic_id, self.name(), self.expected_utility, self.expected_total_utility,
                self.expected_cost, self.expected_total_cost, self.expected_items,
                self.residual_expected_utility, self.residual_expected_total_utility,
                self.residual_expected_cost, self.residual_expected_total_cost, self.residual_expected_items
            ))
        else:
            print("{0}\t{1}\t{2:.4f}\t{3:.4f}\t{4:.4f}\t{5:.4f}\t{6:.4f}".format(
                self.ranking.topic_id, self.name(), self.expected_utility, self.expected_total_utility,
                self.expected_cost, self.expected_total_cost, self.expected_items,
            ))

    def csv(self):
        return ("{0},{1:.3f},{2:.3f},{3:.3f},{4:.3f},{5:.3f}".format(
            self.name(), self.expected_utility, self.expected_total_utility, self.expected_cost,
            self.expected_total_cost, self.expected_items))


    def get_scores(self):
        """
        :return: list with values of each measurement for the previously measured ranking
        """
        scores = [
         self.expected_utility,
         self.expected_total_utility,
         self.expected_cost,
         self.expected_total_cost,
         self.expected_items]
        return scores

    def _pad_vector(self, vec1, n, val):
        """
        Pads vector 1 up to size n, with the value val
        :param vec1: np array
        :param n: size of the desired array
        :param val: the value to be inserted if padding is required
        :return: the padded vector
        """
        if len(vec1) < n:
            vec1 = np.pad(vec1, (0, n-len(vec1)), 'constant', constant_values=val)
        return vec1

'''
http://dl.acm.org/citation.cfm?id=2838938
@inproceedings{moffat2015inst,
    title={INST: An Adaptive Metric for Information Retrieval Evaluation},
    author={Moffat, Alistair and Bailey, Peter and Scholer, Falk and Thomas, Paul},
    booktitle={Proceedings of the 20th Australasian Document Computing Symposium (ADCS'15)$\}$},
    year={2015},
    organization={ACM--Association for Computing Machinery$\}$}
'''
